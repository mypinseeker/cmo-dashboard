"""Experience Score Calculation Engine

Computes a composite experience score (0-5) based on five network quality dimensions:
- Download throughput (30%)
- Latency (25%)
- PRB utilization (20%)
- RRC setup success rate (15%)
- Call drop rate (10%)
"""

import json
from typing import List, Dict
from pathlib import Path


def calculate_experience_score(
    dl_throughput_mbps: float,
    latency_ms: float,
    prb_pct: float,
    rrc_success_pct: float,
    call_drop_pct: float
) -> float:
    """
    Calculate experience score (0-5) from five network quality metrics.

    Args:
        dl_throughput_mbps: Download throughput in Mbps
        latency_ms: Latency in milliseconds
        prb_pct: PRB utilization percentage
        rrc_success_pct: RRC setup success rate percentage
        call_drop_pct: Call drop rate percentage

    Returns:
        float: Composite experience score rounded to 2 decimals (0-5)
    """
    # Download throughput score (30% weight)
    if dl_throughput_mbps >= 50:
        s1 = 5
    elif dl_throughput_mbps >= 30:
        s1 = 4
    elif dl_throughput_mbps >= 15:
        s1 = 3
    elif dl_throughput_mbps >= 5:
        s1 = 2
    else:
        s1 = 1

    # Latency score (25% weight)
    if latency_ms <= 20:
        s2 = 5
    elif latency_ms <= 30:
        s2 = 4
    elif latency_ms <= 50:
        s2 = 3
    elif latency_ms <= 100:
        s2 = 2
    else:
        s2 = 1

    # PRB utilization score (20% weight)
    if prb_pct <= 50:
        s3 = 5
    elif prb_pct <= 65:
        s3 = 4
    elif prb_pct <= 80:
        s3 = 3
    elif prb_pct <= 90:
        s3 = 2
    else:
        s3 = 1

    # RRC setup success score (15% weight)
    if rrc_success_pct >= 99.5:
        s4 = 5
    elif rrc_success_pct >= 99:
        s4 = 4
    elif rrc_success_pct >= 98:
        s4 = 3
    elif rrc_success_pct >= 95:
        s4 = 2
    else:
        s4 = 1

    # Call drop rate score (10% weight)
    if call_drop_pct <= 0.2:
        s5 = 5
    elif call_drop_pct <= 0.5:
        s5 = 4
    elif call_drop_pct <= 1.0:
        s5 = 3
    elif call_drop_pct <= 2.0:
        s5 = 2
    else:
        s5 = 1

    # Weighted average
    composite_score = s1 * 0.30 + s2 * 0.25 + s3 * 0.20 + s4 * 0.15 + s5 * 0.10
    return round(composite_score, 2)


def calculate_batch_experience_scores(
    radio_kpi_path: str,
    network_kpi_path: str,
    output_path: str = None
) -> List[Dict]:
    """
    Calculate experience scores for all records in radio_kpi and network_kpi.

    Args:
        radio_kpi_path: Path to radio_kpi.json
        network_kpi_path: Path to network_kpi.json
        output_path: Path to write experience_scores.json. If None, uses data/experience_scores.json

    Returns:
        List of dicts with site_id, timestamp, and experience_score
    """
    # Load source data
    with open(radio_kpi_path) as f:
        radio_data = json.load(f)

    with open(network_kpi_path) as f:
        network_data = json.load(f)

    # Index network data by site_id for fast lookup
    network_by_site = {}
    for record in network_data:
        key = (record["site_id"], record["timestamp"])
        network_by_site[key] = record

    # Calculate scores
    scores = []
    for radio_record in radio_data:
        site_id = radio_record["site_id"]
        timestamp = radio_record["timestamp"]

        # Find matching network record
        network_record = network_by_site.get((site_id, timestamp))
        if not network_record:
            continue

        # Extract metrics
        dl_throughput = network_record.get("dl_throughput_mbps_avg", 0)
        latency = network_record.get("latency_ms_avg", 100)
        prb_util = radio_record.get("prb_utilization_dl_pct", 80)
        rrc_success = radio_record.get("rrc_setup_success_rate_pct", 98)
        call_drop = radio_record.get("call_drop_rate_pct", 1.0)

        # Calculate score
        score = calculate_experience_score(
            dl_throughput, latency, prb_util, rrc_success, call_drop
        )

        scores.append({
            "site_id": site_id,
            "timestamp": timestamp,
            "experience_score": score,
            "dl_throughput_mbps_avg": dl_throughput,
            "latency_ms_avg": latency,
            "prb_utilization_dl_pct": prb_util,
            "rrc_setup_success_rate_pct": rrc_success,
            "call_drop_rate_pct": call_drop
        })

    # Write output
    if output_path is None:
        output_path = Path(radio_kpi_path).parent / "experience_scores.json"

    with open(output_path, "w") as f:
        json.dump(scores, f, indent=2)

    return scores


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        radio_kpi = sys.argv[1]
        network_kpi = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        # Default paths
        radio_kpi = "data/radio_kpi.json"
        network_kpi = "data/network_kpi.json"
        output = None

    scores = calculate_batch_experience_scores(radio_kpi, network_kpi, output)
    print(f"Generated {len(scores)} experience scores")
