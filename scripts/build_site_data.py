"""
Build a compact JSON for the website by merging India occupation stats with AI exposure scores.

Reads india_occupations_stats.json (for stats) and india_scores.json (for AI exposure).
Writes site/data.json.

Usage:
    python build_site_data.py
"""

import json
import os


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    site_dir = os.path.join(base_dir, "site")

    # Load AI exposure scores
    scores_file = os.path.join(data_dir, "india_scores.json")
    if os.path.exists(scores_file):
        with open(scores_file) as f:
            scores_list = json.load(f)
        scores = {s["nco_code"]: s for s in scores_list}
    else:
        print("Warning: india_scores.json not found. AI exposure will be empty.")
        scores = {}

    # Load occupation stats
    stats_file = os.path.join(data_dir, "india_occupations_stats.json")
    with open(stats_file) as f:
        occupations = json.load(f)

    # Merge data for the visualizer
    data = []
    for occ in occupations:
        nco_code = occ["nco_code"]
        score = scores.get(nco_code, {})

        # Create slug from title
        slug = (
            occ["title"]
            .lower()
            .replace(" ", "-")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "-")
        )

        item = {
            "title": occ["title"],
            "slug": slug,
            "category": occ["category"],
            "nco_code": nco_code,
            "jobs": occ.get("total_employment"),
            "pay_monthly": occ.get("median_monthly_wage"),
            "pay_annual": occ.get("median_monthly_wage", 0) * 12
            if occ.get("median_monthly_wage")
            else None,
            "outlook": occ.get("outlook_pct"),
            "outlook_desc": occ.get("outlook_desc"),
            "female_pct": occ.get("female_percentage"),
            "urban_pct": round(
                100
                * occ.get("urban_count", 0)
                / max(occ.get("total_employment", 1), 1),
                1,
            ),
            "education": occ.get("education_distribution", {}),
            "exposure": score.get("exposure"),
            "exposure_rationale": score.get("rationale"),
            "url": "https://www.ncs.gov.in/",  # Placeholder
        }
        data.append(item)

    # Sort by employment count (largest first)
    data.sort(key=lambda x: x.get("jobs", 0), reverse=True)

    # Ensure site directory exists
    os.makedirs(site_dir, exist_ok=True)

    # Write the data file
    output_file = os.path.join(site_dir, "data.json")
    with open(output_file, "w") as f:
        json.dump(data, f)

    print(f"Wrote {len(data)} occupations to {output_file}")
    total_jobs = sum(d.get("jobs", 0) for d in data if d.get("jobs"))
    print(f"Total jobs represented: {total_jobs:,}")

    # Category summary
    print("\nBy Category:")
    categories = {}
    for d in data:
        cat = d.get("category", "Unknown")
        if cat not in categories:
            categories[cat] = {"count": 0, "jobs": 0}
        categories[cat]["count"] += 1
        categories[cat]["jobs"] += d.get("jobs", 0)

    for cat in sorted(
        categories.keys(), key=lambda x: categories[x]["jobs"], reverse=True
    ):
        print(
            f"  {cat}: {categories[cat]['count']} occupations, {categories[cat]['jobs']:,} jobs"
        )

    # Exposure distribution
    if scores:
        exposures = [d.get("exposure") for d in data if d.get("exposure") is not None]
        if exposures:
            avg_exp = sum(exposures) / len(exposures)
            print(f"\nAverage AI Exposure: {avg_exp:.1f}")
            high_exp = len([e for e in exposures if e >= 7])
            print(f"High exposure (7+): {high_exp} occupations")


if __name__ == "__main__":
    main()
