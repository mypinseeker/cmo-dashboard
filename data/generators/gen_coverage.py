#!/usr/bin/env python3
"""
Coverage Data Generator for CMO Dashboard
Generates MR RSRP distribution data by coverage zones (core, mid, edge).
"""

import json
import random
from pathlib import Path
from collections import defaultdict

random.seed(42)

# Coverage zone characteristics by city
# Edge zone percentage, and speed degradation relative to core
CITY_COVERAGE = {
    "Bogota": {
        "edge_pct": 15.0,
        "mid_pct": 36.4,
        "core_pct": 48.6,
    },
    "Medellin": {
        "edge_pct": 18.0,
        "mid_pct": 35.6,
        "core_pct": 46.4,
    },
    "Cali": {
        "edge_pct": 22.0,
        "mid_pct": 32.4,
        "core_pct": 45.6,
    },
    "Barranquilla": {
        "edge_pct": 32.0,
        "mid_pct": 28.6,
        "core_pct": 39.4,
    },
    "Cartagena": {
        "edge_pct": 28.0,
        "mid_pct": 30.6,
        "core_pct": 41.4,
    },
    "Rural": {
        "edge_pct": 25.0,
        "mid_pct": 35.0,
        "core_pct": 40.0,
    },
}

# Speed characteristics for each zone
ZONE_CHARACTERISTICS = {
    "core": {
        "avg_dl_mbps": 52.0,
        "std_dev_mbps": 8.0,
    },
    "mid": {
        "avg_dl_mbps": 28.5,
        "std_dev_mbps": 6.0,
    },
    "edge": {
        "avg_dl_mbps": 8.2,
        "std_dev_mbps": 3.0,
    },
}


def load_sites():
    """Load sites from sites.json and return organized by city"""
    sites_path = Path(__file__).parent.parent / "sites.json"
    with open(sites_path, "r") as f:
        sites = json.load(f)

    # Organize by city
    sites_by_city = defaultdict(list)
    for site in sites:
        sites_by_city[site["city"]].append(site)

    return sites_by_city


def generate_speed_for_zone(zone_name):
    """Generate MR download speed for a coverage zone"""
    characteristics = ZONE_CHARACTERISTICS[zone_name]
    mean = characteristics["avg_dl_mbps"]
    std_dev = characteristics["std_dev_mbps"]

    # Normal distribution, but clamp to realistic range
    speed = random.gauss(mean, std_dev)
    speed = max(2.0, speed)  # Minimum 2 Mbps

    return round(speed, 1)


def generate_coverage_record(site_id, city):
    """Generate a single coverage zone distribution record for a site"""

    # Get city coverage distribution
    coverage_config = CITY_COVERAGE.get(city, CITY_COVERAGE["Rural"])

    # Total MR samples - varied by site type for realism
    total_mr_samples = random.randint(10000, 15000)

    # Calculate zone sample counts
    core_count = int(total_mr_samples * coverage_config["core_pct"] / 100)
    mid_count = int(total_mr_samples * coverage_config["mid_pct"] / 100)
    edge_count = total_mr_samples - core_count - mid_count  # Remainder

    # Generate average speeds for each zone
    core_speeds = [generate_speed_for_zone("core") for _ in range(max(1, core_count))]
    mid_speeds = [generate_speed_for_zone("mid") for _ in range(max(1, mid_count))]
    edge_speeds = [generate_speed_for_zone("edge") for _ in range(max(1, edge_count))]

    core_avg = sum(core_speeds) / len(core_speeds) if core_speeds else 0
    mid_avg = sum(mid_speeds) / len(mid_speeds) if mid_speeds else 0
    edge_avg = sum(edge_speeds) / len(edge_speeds) if edge_speeds else 0

    return {
        "site_id": site_id,
        "city": city,
        "total_mr_samples": total_mr_samples,
        "core_zone_pct": round(coverage_config["core_pct"], 1),
        "mid_zone_pct": round(coverage_config["mid_pct"], 1),
        "edge_zone_pct": round(coverage_config["edge_pct"], 1),
        "core_avg_dl_mbps": round(core_avg, 1),
        "mid_avg_dl_mbps": round(mid_avg, 1),
        "edge_avg_dl_mbps": round(edge_avg, 1),
    }


def generate_coverage_data():
    """Generate complete coverage dataset"""
    sites_by_city = load_sites()
    coverage_records = []

    # Generate one record per site
    for city, sites in sorted(sites_by_city.items()):
        for site in sites:
            record = generate_coverage_record(site["site_id"], city)
            coverage_records.append(record)

    return coverage_records


def main():
    """Main entry point"""
    print("Generating Coverage data...")

    # Generate data
    coverage_data = generate_coverage_data()

    print(f"Generated {len(coverage_data)} coverage records")

    # Statistics by city
    city_stats = defaultdict(lambda: {"count": 0, "edge_pcts": [], "speeds": []})

    for record in coverage_data:
        city = record["city"]
        city_stats[city]["count"] += 1
        city_stats[city]["edge_pcts"].append(record["edge_zone_pct"])
        city_stats[city]["speeds"].append(
            {
                "core": record["core_avg_dl_mbps"],
                "mid": record["mid_avg_dl_mbps"],
                "edge": record["edge_avg_dl_mbps"],
            }
        )

    print("\nCoverage distribution by city:")
    for city in sorted(city_stats.keys()):
        stats = city_stats[city]
        count = stats["count"]
        avg_edge_pct = sum(stats["edge_pcts"]) / len(stats["edge_pcts"])

        # Average speeds
        core_speeds = [s["core"] for s in stats["speeds"]]
        mid_speeds = [s["mid"] for s in stats["speeds"]]
        edge_speeds = [s["edge"] for s in stats["speeds"]]

        avg_core = sum(core_speeds) / len(core_speeds) if core_speeds else 0
        avg_mid = sum(mid_speeds) / len(mid_speeds) if mid_speeds else 0
        avg_edge = sum(edge_speeds) / len(edge_speeds) if edge_speeds else 0

        print(f"  {city}: {count} sites")
        print(f"    Edge zone: {avg_edge_pct:.1f}% (expected: {CITY_COVERAGE[city]['edge_pct']:.1f}%)")
        print(f"    Avg speeds (core/mid/edge): {avg_core:.1f} / {avg_mid:.1f} / {avg_edge:.1f} Mbps")

    # Verify negative correlation: higher edge% -> lower speeds
    print(f"\nEdge zone vs speed correlation:")
    high_edge = [r for r in coverage_data if r["edge_zone_pct"] > 25]
    low_edge = [r for r in coverage_data if r["edge_zone_pct"] < 20]

    if high_edge:
        high_edge_speeds = [r["edge_avg_dl_mbps"] for r in high_edge]
        high_edge_avg = sum(high_edge_speeds) / len(high_edge_speeds)
        print(f"  High edge zone (>25%): avg edge speed = {high_edge_avg:.1f} Mbps")

    if low_edge:
        low_edge_speeds = [r["edge_avg_dl_mbps"] for r in low_edge]
        low_edge_avg = sum(low_edge_speeds) / len(low_edge_speeds)
        print(f"  Low edge zone (<20%): avg edge speed = {low_edge_avg:.1f} Mbps")

    # Save to file
    output_path = Path(__file__).parent.parent / "coverage.json"
    with open(output_path, "w") as f:
        json.dump(coverage_data, f, indent=2)

    print(f"\nData saved to {output_path}")


if __name__ == "__main__":
    main()
