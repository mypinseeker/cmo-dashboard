"""Potential Score Engine

Analyzes grid-based population and coverage data to identify high-potential
expansion opportunities. Scores uncovered grids based on:
- Population density (35%)
- Coverage gap (30%)
- Competitor presence (20%)
- Estimated income tier (15%)
"""

import json
from typing import List, Dict
from pathlib import Path


def calculate_potential(
    population_data_path: str,
    output_path: str = None,
    min_score: float = 0.6
) -> List[Dict]:
    """
    Calculate expansion potential scores for uncovered grid cells.

    For each grid:
    - Identifies Tigo coverage status
    - Scores uncovered grids on population, coverage gap, competitor activity, income
    - Returns sorted list of high-potential expansion targets

    Args:
        population_data_path: Path to population.json
        output_path: Path to write potential_scores.json. If None, uses data/potential_scores.json
        min_score: Minimum score threshold to include (0-1). Default: 0.6

    Returns:
        List of potential expansion grids sorted by score (descending)
    """
    # Load population data
    with open(population_data_path) as f:
        population_data = json.load(f)

    potential_scores = []

    for grid in population_data:
        grid_id = grid.get("grid_id")
        city = grid.get("city")
        population = grid.get("population", 0)
        tigo_coverage = grid.get("tigo_coverage", False)
        nearest_tigo_site_km = grid.get("nearest_tigo_site_km", 10)

        # Skip if already covered by Tigo
        if tigo_coverage:
            continue

        # Population score (normalized to 0-1, 35% weight)
        # Assume max population per grid is ~5000
        population_score = min(population / 5000, 1.0)

        # Coverage gap score (30% weight)
        # Based on distance to nearest Tigo site
        # < 1 km = gap exists but close, > 5 km = significant gap
        if nearest_tigo_site_km <= 0.5:
            coverage_gap_score = 0.3
        elif nearest_tigo_site_km <= 1.0:
            coverage_gap_score = 0.5
        elif nearest_tigo_site_km <= 2.0:
            coverage_gap_score = 0.7
        elif nearest_tigo_site_km <= 5.0:
            coverage_gap_score = 0.85
        else:
            coverage_gap_score = 1.0

        # Competitor presence score (20% weight)
        # Higher Ookla samples = more competitor activity = better opportunity
        ookla_claro = grid.get("ookla_claro_samples", 0)
        ookla_tigo = grid.get("ookla_tigo_samples", 0)
        ookla_total = ookla_claro + ookla_tigo

        if ookla_total == 0:
            competitor_score = 0.5  # Unknown territory
        else:
            competitor_pct = ookla_claro / ookla_total
            competitor_score = competitor_pct  # Higher Claro activity = higher opportunity

        # Income tier score (15% weight)
        # Estimate from household count
        households = grid.get("households", 0)
        # Assume higher household density = higher income
        # Max ~600 households per grid
        income_score = min(households / 600, 1.0)

        # Composite score
        composite_score = (
            population_score * 0.35 +
            coverage_gap_score * 0.30 +
            competitor_score * 0.20 +
            income_score * 0.15
        )

        # Only include high-potential grids
        if composite_score >= min_score:
            potential_scores.append({
                "grid_id": grid_id,
                "city": city,
                "latitude": grid.get("lat_center"),
                "longitude": grid.get("lon_center"),
                "population": population,
                "households": households,
                "nearest_tigo_site_km": nearest_tigo_site_km,
                "potential_score": round(composite_score, 3),
                "population_score": round(population_score, 3),
                "coverage_gap_score": round(coverage_gap_score, 3),
                "competitor_score": round(competitor_score, 3),
                "income_score": round(income_score, 3),
                "ookla_claro_samples": ookla_claro,
                "ookla_tigo_samples": ookla_tigo
            })

    # Sort by potential score (highest first)
    potential_scores.sort(key=lambda x: x["potential_score"], reverse=True)

    # Write output
    if output_path is None:
        output_path = Path(population_data_path).parent / "potential_scores.json"

    with open(output_path, "w") as f:
        json.dump(potential_scores, f, indent=2)

    return potential_scores


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        population_path = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
        min_score = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    else:
        population_path = "data/population.json"
        output = None
        min_score = 0.6

    potential = calculate_potential(population_path, output, min_score)
    print(f"Generated potential scores for {len(potential)} expansion grids")
