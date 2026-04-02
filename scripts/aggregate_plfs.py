"""
Aggregate PLFS data to create India occupation statistics.

Reads from India-Data-Folders/Data in CSV/cperv1.csv (and chhv1.csv for rural)
Aggregates by NCO occupation code, computes:
- Total employment count
- Median wage (monthly)
- Gender distribution
- Education distribution
- Sector distribution (urban/rural)

Usage:
    python aggregate_plfs.py
"""

import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict

# Import NCO mapping
import sys

sys.path.append(os.path.dirname(__file__))
from nco_mapping import NCO_MAPPING, CATEGORY_MAPPING, get_category, get_occupation_name

# File paths
# PLFS data is in the parent India-Job-Market-Visualizer folder
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(PARENT_DIR, "India-Data-Folders", "Data in CSV")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# PLFS Status Codes
# 11 - Employee (Salaried)
# 21 - Self-Employed (Regular)
# 31 - Self-Employed (Casual/Labour)
# 91 - Not in Labour Force
WORKER_CODES = [11, 21, 31]

# Education levels (General_Education_Level)
EDUCATION_LABELS = {
    1: "Not literate",
    2: "Literate but no formal schooling",
    3: "Below primary",
    4: "Primary",
    5: "Middle",
    6: "Secondary",
    7: "Higher secondary",
    8: "Graduate",
    9: "Post graduate and above",
    10: "Technical diploma/certificate",
    11: "Graduate with technical degree",
    12: "Post graduate with technical degree",
}


def load_plfs_data():
    """Load both urban (cperv1) and rural (chhv1) PLFS data"""
    print("Loading PLFS data...")

    files = ["cperv1.csv", "chhv1.csv"]
    dfs = []

    for f in files:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            print(f"  Loading {f}...")
            df = pd.read_csv(path, low_memory=False)
            df["source"] = "urban" if "cperv1" in f else "rural"
            dfs.append(df)
            print(f"    Loaded {len(df):,} records")
        else:
            print(f"  File not found: {f}")

    if not dfs:
        raise FileNotFoundError("No PLFS data files found!")

    combined = pd.concat(dfs, ignore_index=True)
    print(f"Total records: {len(combined):,}")
    return combined


def process_workers(df):
    """Filter and process worker data"""
    print("\nProcessing workers...")

    # Convert status code to numeric
    df["Principal_Status_Code"] = pd.to_numeric(
        df["Principal_Status_Code"], errors="coerce"
    )
    df["Principal_Occupation_Code"] = pd.to_numeric(
        df["Principal_Occupation_Code"], errors="coerce"
    )

    # Filter for workers only
    workers = df[df["Principal_Status_Code"].isin(WORKER_CODES)].copy()
    print(f"  Worker records: {len(workers):,}")

    # Filter for valid occupation codes (3-digit NCO codes)
    workers = workers[workers["Principal_Occupation_Code"].notna()].copy()
    workers["NCO_Code"] = (
        workers["Principal_Occupation_Code"].astype(int).astype(str).str.zfill(3)
    )
    print(f"  With valid NCO code: {len(workers):,}")

    return workers


def get_wage(workers):
    """Extract and process wage data from Day7 wages"""
    # Day7_Act1_Wage contains daily wage - convert to monthly (approx 25 days)
    # We'll use Principal_Status_Code to identify wage type

    wage_cols = ["Day7_Act1_Wage", "Day7_Act2_Wage"]

    def calculate_monthly_wage(row):
        wage = row.get("Day7_Act1_Wage", 0)
        if pd.isna(wage) or wage == 0:
            wage = row.get("Day7_Act2_Wage", 0)
        if pd.isna(wage) or wage == 0:
            return None
        # Daily wage * 25 for monthly estimate
        return float(wage) * 25

    workers["monthly_wage"] = workers.apply(calculate_monthly_wage, axis=1)
    return workers


def aggregate_occupations(workers):
    """Aggregate data by occupation code"""
    print("\nAggregating by occupation...")

    # Group by NCO code
    occupation_stats = defaultdict(
        lambda: {
            "count": 0,
            "wages": [],
            "male": 0,
            "female": 0,
            "urban": 0,
            "rural": 0,
            "education": defaultdict(int),
            "sector": defaultdict(int),  # Industry sectors
        }
    )

    for _, row in workers.iterrows():
        nco = row["NCO_Code"]
        if nco not in NCO_MAPPING:
            continue  # Skip unknown NCO codes

        stats = occupation_stats[nco]
        stats["count"] += 1

        # Wages
        if pd.notna(row.get("monthly_wage")) and row.get("monthly_wage", 0) > 0:
            stats["wages"].append(row["monthly_wage"])

        # Gender
        sex = row.get("Sex", 0)
        if sex == 1:
            stats["male"] += 1
        elif sex == 2:
            stats["female"] += 1

        # Sector (urban/rural)
        source = row.get("source", "urban")
        if source == "urban":
            stats["urban"] += 1
        else:
            stats["rural"] += 1

        # Education
        edu = row.get("General_Education_Level", 0)
        if pd.notna(edu):
            stats["education"][int(edu)] += 1

        # Industry (Sector)
        ind = row.get("Principal_Industry_Code", 0)
        if pd.notna(ind):
            # NIC sector (first 2 digits)
            sector = str(int(ind))[:2] if len(str(int(ind))) >= 2 else "00"
            stats["sector"][sector] += 1

    # Calculate aggregated stats
    results = []
    for nco, stats in occupation_stats.items():
        wages = stats["wages"]
        median_wage = np.median(wages) if wages else None
        avg_wage = np.mean(wages) if wages else None

        # Education distribution (simplified)
        edu_total = sum(stats["education"].values())
        edu_distribution = {}
        if edu_total > 0:
            for edu_code, count in stats["education"].items():
                label = EDUCATION_LABELS.get(edu_code, f"Level {edu_code}")
                edu_distribution[label] = round(100 * count / edu_total, 1)

        # Top 3 sectors
        sector_dist = dict(
            sorted(stats["sector"].items(), key=lambda x: x[1], reverse=True)[:3]
        )

        result = {
            "nco_code": nco,
            "title": get_occupation_name(nco),
            "category": get_category(nco),
            "total_employment": stats["count"],
            "median_monthly_wage": int(median_wage) if median_wage else None,
            "avg_monthly_wage": int(avg_wage) if avg_wage else None,
            "male_count": stats["male"],
            "female_count": stats["female"],
            "urban_count": stats["urban"],
            "rural_count": stats["rural"],
            "female_percentage": round(100 * stats["female"] / stats["count"], 1)
            if stats["count"] > 0
            else 0,
            "education_distribution": edu_distribution,
            "top_sectors": sector_dist,
            "wage_data_available": len(wages) > 0,
            "wage_sample_size": len(wages),
        }
        results.append(result)

    # Sort by employment count
    results.sort(key=lambda x: x["total_employment"], reverse=True)

    print(f"  Total occupations found: {len(results)}")
    return results


def calculate_outlook(occupations):
    """Calculate growth outlook for each occupation"""
    print("\nCalculating growth outlook...")

    # For India, we'll estimate based on:
    # 1. Sector growth (IT, Manufacturing, Services have higher growth)
    # 2. Female percentage (higher female workforce = higher growth potential)
    # 3. Education level (higher education = higher growth)

    # Reference growth rates by NCO category (approximate)
    category_growth = {
        "Professionals": 15,  # High growth - IT, healthcare, education
        "Technicians & Associates": 12,
        "Service & Sales": 8,
        "Managers": 10,
        "Clerical Support": 5,
        "Agriculture & Fishery": -5,  # Declining
        "Craft & Trades": 6,
        "Machine Operators": 4,
        "Elementary": 2,
    }

    for occ in occupations:
        base_growth = category_growth.get(occ["category"], 5)

        # Adjust for IT sector presence
        it_sectors = ["62", "63"]  # IT services
        if any(s in it_sectors for s in occ.get("top_sectors", {}).keys()):
            base_growth += 8

        # Adjust for education level (graduate+ = higher growth)
        if "Graduate" in str(occ.get("education_distribution", {})):
            base_growth += 3

        # Cap between -15 and +25
        outlook = max(-15, min(25, base_growth))

        # Description
        if outlook >= 15:
            desc = "Very Fast Growth"
        elif outlook >= 8:
            desc = "Fast Growth"
        elif outlook >= 2:
            desc = "Moderate Growth"
        elif outlook >= -5:
            desc = "Slow Decline"
        else:
            desc = "Declining"

        occ["outlook_pct"] = outlook
        occ["outlook_desc"] = desc

    return occupations


def create_occupations_json(occupations):
    """Create occupations.json for the visualizer"""
    print("\nCreating occupations.json...")

    jobs = []
    for occ in occupations:
        jobs.append(
            {
                "title": occ["title"],
                "nco_code": occ["nco_code"],
                "category": occ["category"],
                "url": f"https://www.ncs.gov.in/",  # Placeholder
            }
        )

    return jobs


def create_occupations_csv(occupations):
    """Create occupations.csv for the visualizer"""
    print("\nCreating occupations.csv...")

    rows = []
    for occ in occupations:
        row = {
            "title": occ["title"],
            "category": occ["category"],
            "slug": occ["title"]
            .lower()
            .replace(" ", "-")
            .replace("(", "")
            .replace(")", ""),
            "nco_code": occ["nco_code"],
            "median_pay_monthly": occ.get("median_monthly_wage"),
            "median_pay_annual": occ.get("median_monthly_wage", 0) * 12
            if occ.get("median_monthly_wage")
            else None,
            "num_jobs": occ["total_employment"],
            "outlook_pct": occ.get("outlook_pct"),
            "outlook_desc": occ.get("outlook_desc"),
            "female_pct": occ.get("female_percentage"),
            "urban_pct": round(100 * occ["urban_count"] / occ["total_employment"], 1)
            if occ["total_employment"] > 0
            else 0,
            "rural_pct": round(100 * occ["rural_count"] / occ["total_employment"], 1)
            if occ["total_employment"] > 0
            else 0,
            "education_summary": json.dumps(occ.get("education_distribution", {})),
            "wage_sample_size": occ.get("wage_sample_size", 0),
        }
        rows.append(row)

    return rows


def main():
    print("=" * 60)
    print("India Job Market - PLFS Data Aggregation")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load and process data
    df = load_plfs_data()
    workers = process_workers(df)
    workers = get_wage(workers)
    occupations = aggregate_occupations(workers)
    occupations = calculate_outlook(occupations)

    # Summary statistics
    total_jobs = sum(o["total_employment"] for o in occupations)
    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Total occupations: {len(occupations)}")
    print(f"  Total workers: {total_jobs:,}")
    print(f"  Total employment: {total_jobs:,}")

    # Category breakdown
    category_counts = {}
    for o in occupations:
        cat = o["category"]
        category_counts[cat] = category_counts.get(cat, 0) + o["total_employment"]

    print(f"\n  By Category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {cat}: {count:,}")

    # Save outputs
    # 1. Full occupation stats (JSON)
    with open(os.path.join(OUTPUT_DIR, "india_occupations_stats.json"), "w") as f:
        json.dump(occupations, f, indent=2)
    print(f"\nSaved: {OUTPUT_DIR}/india_occupations_stats.json")

    # 2. occupations.json (list of occupations)
    jobs_json = create_occupations_json(occupations)
    with open(os.path.join(OUTPUT_DIR, "occupations.json"), "w") as f:
        json.dump(jobs_json, f, indent=2)
    print(f"Saved: {OUTPUT_DIR}/occupations.json")

    # 3. occupations.csv
    rows = create_occupations_csv(occupations)
    import csv

    fieldnames = list(rows[0].keys()) if rows else []
    with open(os.path.join(OUTPUT_DIR, "occupations.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {OUTPUT_DIR}/occupations.csv")

    # Sample output
    print(f"\n{'=' * 60}")
    print("Top 10 Occupations by Employment:")
    print(f"{'NCO':<5} {'Title':<40} {'Jobs':>10} {'Monthly Wage':>15}")
    print("-" * 75)
    for occ in occupations[:10]:
        wage = (
            f"₹{occ['median_monthly_wage']:,}"
            if occ.get("median_monthly_wage")
            else "N/A"
        )
        print(
            f"{occ['nco_code']:<5} {occ['title'][:40]:<40} {occ['total_employment']:>10,} {wage:>15}"
        )

    print(f"\n{'=' * 60}")
    print("Done! Data ready for India Job Market Visualizer.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
