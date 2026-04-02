"""
Score each occupation's AI exposure using an LLM via OpenRouter.
India-specific adaptation of Karpathy's score.py

Reads from india_occupations_stats.json, generates AI exposure scores.
Results are cached to india_scores.json.

Usage:
    python score.py
    python score.py --model google/gemini-3-flash-preview
    python score.py --start 0 --end 10   # test on first 10
"""

import argparse
import json
import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "google/gemini-3-flash-preview"
INPUT_FILE = "data/india_occupations_stats.json"
OUTPUT_FILE = "data/india_scores.json"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """\
You are an expert analyst evaluating how exposed different occupations in India 
are to AI (Artificial Intelligence). You will be given a detailed description 
of an occupation from India's labour market data.

Rate the occupation's overall **AI Exposure** on a scale from 0 to 10.

AI Exposure measures: how much will AI reshape this occupation in India? 
Consider both direct effects (AI automating tasks currently done by humans) 
and indirect effects (AI making each worker so productive that fewer are needed).

India-specific considerations:
- India's IT/BPO sector is a major employer - jobs with routine digital tasks are highly exposed
- Many jobs in India involve informal/unorganized sector work that has natural AI barriers
- English-language roles in India have higher exposure than Hindi/regional language roles
- Manufacturing and construction in India often involve physical work that is less AI-exposed
- Agricultural work in India has very low AI exposure due to seasonal/unpredictable nature

A key signal is whether the job's work product is fundamentally digital. If 
the job can be done entirely from a computer — writing, coding, analyzing, 
communicating — then AI exposure is inherently high (7+), because AI capabilities 
in digital domains are advancing rapidly. Conversely, jobs requiring physical 
presence, manual skill, or real-time human interaction in the physical world 
have a natural barrier to AI exposure.

Use these anchors to calibrate your score:

- **0–1: Minimal exposure.** The work is almost entirely physical, hands-on, 
or requires real-time human presence in unpredictable environments. AI has 
essentially no impact on daily work. \
Examples: agricultural labourer, construction worker, street vendor, domestic help.

- **2–3: Low exposure.** Mostly physical or interpersonal work. AI might help 
with minor peripheral tasks (scheduling, paperwork) but doesn't touch the 
core job. \
Examples: electrician, plumber, security guard, teacher (with practical subjects), nurse.

- **4–5: Moderate exposure.** A mix of physical/interpersonal work and 
knowledge work. AI can meaningfully assist with the information-processing 
parts but a substantial share of the job still requires human presence. \
Examples: accountant, sales manager, medical technician, primary teacher.

- **6–7: High exposure.** Predominantly knowledge work with some need for 
human judgment, relationships, or physical presence. AI tools are already 
useful and workers using AI may be substantially more productive. \
Examples: software developer, content writer, data analyst, financial analyst, 
digital marketing professional, call centre agent.

- **8–9: Very high exposure.** The job is almost entirely done on a computer. 
All core tasks — writing, coding, analyzing, designing, communicating — are 
in domains where AI is rapidly improving. The occupation faces major 
restructuring. \
Examples: software engineer, graphic designer, translator, legal assistant, 
back-office data processor, e-commerce specialist.

- **10: Maximum exposure.** Routine information processing, fully digital, 
with no physical component. AI can already do most of it today. \
Examples: data entry operator, tele-caller, basic content moderator.

Respond with ONLY a JSON object in this exact format, no other text:
{
  "exposure": <0-10>,
  "rationale": "<2-3 sentences explaining the key factors>"
}\
"""


def create_prompt_for_occupation(occupation):
    """Create a detailed prompt for each occupation"""
    title = occupation.get("title", "Unknown")
    category = occupation.get("category", "Unknown")
    total_jobs = occupation.get("total_employment", 0)
    median_wage = occupation.get("median_monthly_wage", 0)
    female_pct = occupation.get("female_percentage", 0)
    urban_pct = (
        100
        - occupation.get("rural_count", 50)
        / max(occupation.get("total_employment", 1), 1)
        * 100
    )

    # Get education distribution
    edu_dist = occupation.get("education_distribution", {})
    edu_str = (
        ", ".join([f"{k}: {v}%" for k, v in list(edu_dist.items())[:3]])
        if edu_dist
        else "Not available"
    )

    prompt = f"""Occupation: {title}
Category: {category}
Total Employment in India: {total_jobs:,}
Median Monthly Wage: ₹{median_wage:,} if available
Female Workforce: {female_pct}%
Urban Employment: {urban_pct:.0f}%
Education Distribution: {edu_str}

Please rate the AI exposure for this occupation considering India's specific 
labour market context."""

    return prompt


def score_occupation(client, occupation, model):
    """Send one occupation to the LLM and parse the structured response."""
    prompt = create_prompt_for_occupation(occupation)

    response = client.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]

    # Strip markdown code fences if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]  # remove first line
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    return json.loads(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument(
        "--force", action="store_true", help="Re-score even if already cached"
    )
    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not found in environment or .env file")
        print("Please add OPENROUTER_API_KEY to your .env file")
        return

    # Load occupation data
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found!")
        print("Please run aggregate_plfs.py first to generate occupation data")
        return

    with open(INPUT_FILE) as f:
        occupations = json.load(f)

    subset = occupations[args.start : args.end]

    # Load existing scores
    scores = {}
    if os.path.exists(OUTPUT_FILE) and not args.force:
        with open(OUTPUT_FILE) as f:
            for entry in json.load(f):
                scores[entry["nco_code"]] = entry

    print(f"Scoring {len(subset)} occupations with {args.model}")
    print(f"Already cached: {len(scores)}")

    errors = []
    client = httpx.Client()

    for i, occ in enumerate(subset):
        nco_code = occ["nco_code"]

        if nco_code in scores:
            continue

        print(
            f"  [{i + 1}/{len(subset)}] {occ['title']} (NCO {nco_code})...",
            end=" ",
            flush=True,
        )

        try:
            result = score_occupation(client, occ, args.model)
            scores[nco_code] = {
                "nco_code": nco_code,
                "title": occ["title"],
                "category": occ["category"],
                **result,
            }
            print(f"exposure={result['exposure']}")
        except Exception as e:
            print(f"ERROR: {e}")
            errors.append(nco_code)

        # Save after each one (incremental checkpoint)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(list(scores.values()), f, indent=2)

        if i < len(subset) - 1:
            time.sleep(args.delay)

    client.close()

    print(f"\nDone. Scored {len(scores)} occupations, {len(errors)} errors.")
    if errors:
        print(f"Errors: {errors}")

    # Summary stats
    vals = [s for s in scores.values() if "exposure" in s]
    if vals:
        avg = sum(s["exposure"] for s in vals) / len(vals)
        by_score = {}
        for s in vals:
            bucket = s["exposure"]
            by_score[bucket] = by_score.get(bucket, 0) + 1
        print(f"\nAverage AI exposure across {len(vals)} occupations: {avg:.1f}")
        print("Distribution:")
        for k in sorted(by_score):
            print(f"  {k}: {'█' * by_score[k]} ({by_score[k]})")

        # Category-wise average
        print("\nAverage by Category:")
        cat_scores = {}
        for s in vals:
            cat = s.get("category", "Unknown")
            if cat not in cat_scores:
                cat_scores[cat] = []
            cat_scores[cat].append(s["exposure"])

        for cat in sorted(cat_scores.keys()):
            avg_cat = sum(cat_scores[cat]) / len(cat_scores[cat])
            print(f"  {cat}: {avg_cat:.1f}")


if __name__ == "__main__":
    main()
