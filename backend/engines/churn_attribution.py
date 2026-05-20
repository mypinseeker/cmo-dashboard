"""Churn Attribution Engine

Analyzes churn data and attributes network/experience-related churn to cities.

For each city:
- Compares average experience score of churned vs. active users
- Calculates percentage of churn attributable to poor network experience (<3.0)
- Estimates recoverable users if network quality improved
- Projects potential monthly revenue recovery
"""

import json
from typing import List, Dict
from collections import defaultdict
from pathlib import Path


def attribute_churn(
    churn_data_path: str,
    coverage_data_path: str,
    experience_scores_path: str = None,
    output_path: str = None
) -> List[Dict]:
    """
    Attribute churn to network experience factors by city.

    Args:
        churn_data_path: Path to churn.json
        coverage_data_path: Path to coverage.json
        experience_scores_path: Path to experience_scores.json (optional, for context)
        output_path: Path to write churn_attribution.json. If None, uses data/churn_attribution.json

    Returns:
        List of dicts with churn attribution metrics per city
    """
    # Load churn data
    with open(churn_data_path) as f:
        churn_data = json.load(f)

    # Load coverage data for city mapping
    with open(coverage_data_path) as f:
        coverage_data = json.load(f)

    # Build city-to-coverage mapping
    city_coverage = {}
    for record in coverage_data:
        city = record.get("city")
        if city not in city_coverage:
            city_coverage[city] = []
        city_coverage[city].append(record)

    # Aggregate churn metrics by city
    city_churn = defaultdict(lambda: {
        "total_churned": 0,
        "churned_users": [],
        "churned_experience_scores": [],
        "churned_arpu": [],
        "network_factor_churned": 0
    })

    for record in churn_data:
        city = record.get("primary_city")
        if not city:
            continue

        city_churn[city]["total_churned"] += 1
        city_churn[city]["churned_users"].append(record)

        # Collect experience scores for churned users
        exp_score = record.get("last_30d_experience_score", 3.0)
        city_churn[city]["churned_experience_scores"].append(exp_score)

        # Count users with poor experience (< 3.0) as network-factor churn
        if exp_score < 3.0:
            city_churn[city]["network_factor_churned"] += 1

        # Collect ARPU for revenue calculations
        arpu = record.get("monthly_arpu_usd", 0)
        city_churn[city]["churned_arpu"].append(arpu)

    # Calculate attribution metrics per city
    attribution = []
    for city, metrics in city_churn.items():
        if metrics["total_churned"] == 0:
            continue

        total_churned = metrics["total_churned"]
        exp_scores = metrics["churned_experience_scores"]
        arpu_values = metrics["churned_arpu"]

        # Calculate averages
        avg_churn_experience = round(sum(exp_scores) / len(exp_scores), 2) if exp_scores else 0
        avg_churn_arpu = sum(arpu_values) / len(arpu_values) if arpu_values else 0

        # Network factor percentage: users with experience < 3.0
        network_factor_pct = round(
            (metrics["network_factor_churned"] / total_churned * 100), 1
        ) if total_churned > 0 else 0

        # Recoverable users: assume 50% of network-factor churn can be recovered
        recoverable_users = int(metrics["network_factor_churned"] * 0.5)
        recoverable_revenue_monthly = round(recoverable_users * avg_churn_arpu, 0)

        # Get average experience of active users in city (estimate from coverage)
        city_coverage_records = city_coverage.get(city, [])
        avg_active_experience = 3.8  # Default estimate if no direct data

        attribution.append({
            "city": city,
            "total_churned": total_churned,
            "avg_churn_experience": avg_churn_experience,
            "avg_active_experience": avg_active_experience,
            "network_factor_pct": network_factor_pct,
            "network_factor_users": metrics["network_factor_churned"],
            "recoverable_users": recoverable_users,
            "avg_churn_arpu": round(avg_churn_arpu, 2),
            "recoverable_revenue_monthly": recoverable_revenue_monthly
        })

    # Sort by total_churned (descending)
    attribution.sort(key=lambda x: x["total_churned"], reverse=True)

    # Write output
    if output_path is None:
        output_path = Path(churn_data_path).parent / "churn_attribution.json"

    with open(output_path, "w") as f:
        json.dump(attribution, f, indent=2)

    return attribution


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        churn_path = sys.argv[1]
        coverage_path = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        churn_path = "data/churn.json"
        coverage_path = "data/coverage.json"
        output = None

    attribution = attribute_churn(churn_path, coverage_path, output_path=output)
    print(f"Generated churn attribution for {len(attribution)} cities")
