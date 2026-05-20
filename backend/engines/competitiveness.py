"""Competitiveness Engine

Analyzes Ookla speed test data to compare Tigo's network performance
against competitors (Claro, Movistar) across cities.

Computes competitiveness ratios and identifies performance gaps.
"""

import json
from typing import List, Dict
from collections import defaultdict
from pathlib import Path


def calculate_competitiveness(
    ookla_data_path: str,
    output_path: str = None
) -> List[Dict]:
    """
    Calculate competitiveness metrics by city and operator.

    For each city, computes:
    - Average download speed by operator
    - Average latency by operator
    - Tigo's competitiveness ratio (Tigo speed / max competitor speed)
    - Gap direction (Tigo closing/widening gap)

    Args:
        ookla_data_path: Path to ookla.json
        output_path: Path to write competitiveness.json. If None, uses data/competitiveness.json

    Returns:
        List of competitiveness records per city
    """
    # Load Ookla data
    with open(ookla_data_path) as f:
        ookla_data = json.load(f)

    # Aggregate metrics by city and operator
    city_operator_metrics = defaultdict(lambda: defaultdict(lambda: {
        "download_speeds": [],
        "upload_speeds": [],
        "latencies": [],
        "count": 0
    }))

    for record in ookla_data:
        city = record.get("city")
        operator = record.get("operator", "Unknown")
        if not city:
            continue

        metrics = city_operator_metrics[city][operator]
        metrics["download_speeds"].append(record.get("download_mbps", 0))
        metrics["upload_speeds"].append(record.get("upload_mbps", 0))
        metrics["latencies"].append(record.get("latency_ms", 50))
        metrics["count"] += 1

    # Calculate competitiveness per city
    competitiveness = []

    for city in sorted(city_operator_metrics.keys()):
        operators = city_operator_metrics[city]

        # Skip cities without Tigo data
        if "Tigo" not in operators:
            continue

        # Calculate operator averages
        tigo_dl = sum(operators["Tigo"]["download_speeds"]) / len(operators["Tigo"]["download_speeds"]) if operators["Tigo"]["download_speeds"] else 0
        tigo_ul = sum(operators["Tigo"]["upload_speeds"]) / len(operators["Tigo"]["upload_speeds"]) if operators["Tigo"]["upload_speeds"] else 0
        tigo_lat = sum(operators["Tigo"]["latencies"]) / len(operators["Tigo"]["latencies"]) if operators["Tigo"]["latencies"] else 50

        # Get competitor metrics
        claro_dl = 0
        claro_lat = 50
        movistar_dl = 0
        movistar_lat = 50

        if "Claro" in operators:
            claro_dl = sum(operators["Claro"]["download_speeds"]) / len(operators["Claro"]["download_speeds"]) if operators["Claro"]["download_speeds"] else 0
            claro_lat = sum(operators["Claro"]["latencies"]) / len(operators["Claro"]["latencies"]) if operators["Claro"]["latencies"] else 50

        if "Movistar" in operators:
            movistar_dl = sum(operators["Movistar"]["download_speeds"]) / len(operators["Movistar"]["download_speeds"]) if operators["Movistar"]["download_speeds"] else 0
            movistar_lat = sum(operators["Movistar"]["latencies"]) / len(operators["Movistar"]["latencies"]) if operators["Movistar"]["latencies"] else 50

        # Calculate competitiveness ratio
        max_competitor_dl = max(claro_dl, movistar_dl)
        if max_competitor_dl > 0:
            competitiveness_ratio = round(tigo_dl / max_competitor_dl, 3)
        else:
            competitiveness_ratio = 1.0

        # Determine gap direction
        if tigo_dl >= max_competitor_dl:
            gap_direction = "leading"
        elif competitiveness_ratio >= 0.95:
            gap_direction = "closing"
        elif competitiveness_ratio >= 0.85:
            gap_direction = "stable"
        else:
            gap_direction = "widening"

        competitiveness.append({
            "city": city,
            "tigo_dl_mbps": round(tigo_dl, 2),
            "tigo_ul_mbps": round(tigo_ul, 2),
            "claro_dl_mbps": round(claro_dl, 2),
            "movistar_dl_mbps": round(movistar_dl, 2),
            "competitiveness_ratio": competitiveness_ratio,
            "gap_direction": gap_direction,
            "tigo_latency_ms": round(tigo_lat, 1),
            "claro_latency_ms": round(claro_lat, 1),
            "movistar_latency_ms": round(movistar_lat, 1),
            "tigo_samples": operators["Tigo"]["count"],
            "claro_samples": operators["Claro"]["count"] if "Claro" in operators else 0,
            "movistar_samples": operators["Movistar"]["count"] if "Movistar" in operators else 0
        })

    # Sort by competitiveness ratio (best first)
    competitiveness.sort(key=lambda x: x["competitiveness_ratio"], reverse=True)

    # Write output
    if output_path is None:
        output_path = Path(ookla_data_path).parent / "competitiveness.json"

    with open(output_path, "w") as f:
        json.dump(competitiveness, f, indent=2)

    return competitiveness


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ookla_path = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        ookla_path = "data/ookla.json"
        output = None

    competitiveness = calculate_competitiveness(ookla_path, output)
    print(f"Generated competitiveness analysis for {len(competitiveness)} cities")
