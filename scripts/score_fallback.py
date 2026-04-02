"""
Generate AI exposure scores without using LLM API.
Uses category-based heuristic scoring for India job market.

Usage:
    python score_fallback.py
"""

import json
import os

# AI exposure scores by category (India-specific)
CATEGORY_EXPOSURE = {
    "Professionals": 7.5,  # High - IT, doctors, teachers
    "Technicians & Associates": 6.5,  # Medium-high
    "Managers": 6.0,  # Medium-high - some routine tasks
    "Clerical Support": 7.0,  # High - data entry, secretaries
    "Service & Sales": 4.5,  # Medium - customer interaction
    "Agriculture & Fishery": 1.5,  # Very Low - physical, seasonal
    "Craft & Trades": 3.0,  # Low - physical work
    "Machine Operators": 4.0,  # Medium-low
    "Elementary": 2.0,  # Low - manual labor
    "Armed Forces": 2.0,  # Low
}

# NCO-specific adjustments
NCO_ADJUSTMENTS = {
    "251": 9.0,  # Software developers - very high
    "252": 9.0,  # Database/network - very high
    "215": 8.0,  # Electrical engineers
    "214": 7.5,  # Engineering professionals
    "231": 8.0,  # Accountants
    "221": 6.5,  # University teachers
    "223": 6.0,  # Primary teachers
    "322": 5.0,  # Nurses - moderate (human interaction)
    "541": 3.0,  # Security guards - low
    "611": 1.5,  # Farmers - very low
    "612": 1.5,  # Animal producers - very low
    "911": 2.0,  # Cleaners - low
    "832": 4.0,  # Drivers - medium
    "521": 5.0,  # Street vendors
    "522": 5.5,  # Shop salespersons
    "751": 4.0,  # Tailors/cloth workers
    "731": 5.0,  # Precision instrument makers
}


def get_exposure_rationale(nco_code, category, score):
    """Generate a rationale based on the score"""
    if score >= 8:
        return f"Primarily digital work involving coding, data analysis, or routine information processing. AI can automate most tasks. (NCO {nco_code}, {category})"
    elif score >= 6:
        return f"Knowledge work with significant digital components. AI tools can enhance productivity but human judgment still needed. (NCO {nco_code}, {category})"
    elif score >= 4:
        return f"Mixed work involving both digital and physical/interpersonal tasks. AI assistance possible but core work remains human-dependent. (NCO {nco_code}, {category})"
    elif score >= 2:
        return f"Physical or manual work with limited digital exposure. AI has minimal impact on daily tasks. (NCO {nco_code}, {category})"
    else:
        return f"Almost entirely physical work in unpredictable environments. No meaningful AI exposure. (NCO {nco_code}, {category})"


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")

    # Load occupation stats
    stats_file = os.path.join(data_dir, "india_occupations_stats.json")
    with open(stats_file) as f:
        occupations = json.load(f)

    scores = []

    for occ in occupations:
        nco_code = occ["nco_code"]
        category = occ["category"]

        # Get base score from category
        base_score = CATEGORY_EXPOSURE.get(category, 5.0)

        # Apply NCO-specific adjustments
        adjustment = NCO_ADJUSTMENTS.get(nco_code, 0)
        if adjustment > 0:
            score = adjustment
        else:
            score = base_score

        # Round to 1 decimal
        score = round(score, 1)

        # Generate rationale
        rationale = get_exposure_rationale(nco_code, category, score)

        scores.append(
            {
                "nco_code": nco_code,
                "title": occ["title"],
                "category": category,
                "exposure": score,
                "rationale": rationale,
            }
        )

    # Save scores
    output_file = os.path.join(data_dir, "india_scores.json")
    with open(output_file, "w") as f:
        json.dump(scores, f, indent=2)

    print(f"Generated AI exposure scores for {len(scores)} occupations")
    print(f"Saved to: {output_file}")

    # Summary
    avg = sum(s["exposure"] for s in scores) / len(scores)
    high_exp = len([s for s in scores if s["exposure"] >= 7])
    print(f"\nAverage exposure: {avg:.1f}")
    print(f"High exposure (7+): {high_exp} occupations")

    # By category
    print("\nBy Category:")
    cat_scores = {}
    for s in scores:
        cat = s["category"]
        if cat not in cat_scores:
            cat_scores[cat] = []
        cat_scores[cat].append(s["exposure"])

    for cat in sorted(cat_scores.keys()):
        avg_cat = sum(cat_scores[cat]) / len(cat_scores[cat])
        print(f"  {cat}: {avg_cat:.1f}")


if __name__ == "__main__":
    main()
