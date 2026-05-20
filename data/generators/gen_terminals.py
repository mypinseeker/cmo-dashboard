#!/usr/bin/env python3
"""
Terminals Data Generator for CMO Dashboard
Generates device segmentation and ARPU distribution by site.
"""

import json
import random
from pathlib import Path
from collections import defaultdict

random.seed(42)

# Device tier configuration by city
# Percentages for flagship, high_end, mid_range, entry_level
CITY_DEVICE_MIX = {
    "Bogota": {
        "flagship_pct": 18.0,
        "high_end_pct": 22.0,
        "mid_range_pct": 35.0,
        "entry_level_pct": 25.0,
    },
    "Medellin": {
        "flagship_pct": 14.0,
        "high_end_pct": 20.0,
        "mid_range_pct": 36.0,
        "entry_level_pct": 30.0,
    },
    "Cali": {
        "flagship_pct": 10.0,
        "high_end_pct": 18.0,
        "mid_range_pct": 37.0,
        "entry_level_pct": 35.0,
    },
    "Barranquilla": {
        "flagship_pct": 8.0,
        "high_end_pct": 15.0,
        "mid_range_pct": 38.0,
        "entry_level_pct": 39.0,
    },
    "Cartagena": {
        "flagship_pct": 9.0,
        "high_end_pct": 16.0,
        "mid_range_pct": 37.0,
        "entry_level_pct": 38.0,
    },
    "Rural": {
        "flagship_pct": 5.0,
        "high_end_pct": 10.0,
        "mid_range_pct": 38.0,
        "entry_level_pct": 47.0,
    },
}

# Device tier characteristics: ARPU and edge zone ratio
DEVICE_TIERS = {
    "flagship": {
        "avg_arpu": 35.0,
        "arpu_std_dev": 8.0,
        "avg_edge_ratio": 0.12,  # Fewer in edge zone
    },
    "high_end": {
        "avg_arpu": 22.0,
        "arpu_std_dev": 5.0,
        "avg_edge_ratio": 0.18,
    },
    "mid_range": {
        "avg_arpu": 12.0,
        "arpu_std_dev": 3.0,
        "avg_edge_ratio": 0.22,
    },
    "entry_level": {
        "avg_arpu": 6.0,
        "arpu_std_dev": 2.0,
        "avg_edge_ratio": 0.28,  # More in edge zone
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


def generate_arpu_for_tier(tier_name):
    """Generate ARPU for a device tier"""
    tier_config = DEVICE_TIERS[tier_name]
    arpu = random.gauss(tier_config["avg_arpu"], tier_config["arpu_std_dev"])
    return max(0.5, arpu)  # Minimum $0.50


def generate_edge_ratio_for_tier(tier_name):
    """Generate edge zone ratio for a device tier (with variation)"""
    tier_config = DEVICE_TIERS[tier_name]
    base_ratio = tier_config["avg_edge_ratio"]
    # Add ±20% variation
    ratio = base_ratio * random.uniform(0.80, 1.20)
    return max(0.05, min(0.45, ratio))  # Clamp between 5% and 45%


def generate_terminals_record(site_id, city):
    """Generate a single terminals distribution record for a site"""

    # Get city device mix
    device_mix = CITY_DEVICE_MIX.get(city, CITY_DEVICE_MIX["Rural"])

    # Total users at site - varies by site type
    total_users = random.randint(800, 2000)

    # Calculate user counts per tier
    flagship_count = int(total_users * device_mix["flagship_pct"] / 100)
    high_end_count = int(total_users * device_mix["high_end_pct"] / 100)
    mid_range_count = int(total_users * device_mix["mid_range_pct"] / 100)
    entry_level_count = total_users - flagship_count - high_end_count - mid_range_count

    # Generate ARPU distributions
    flagship_arpus = [generate_arpu_for_tier("flagship") for _ in range(flagship_count)]
    high_end_arpus = [generate_arpu_for_tier("high_end") for _ in range(high_end_count)]
    mid_range_arpus = [generate_arpu_for_tier("mid_range") for _ in range(mid_range_count)]
    entry_level_arpus = [generate_arpu_for_tier("entry_level") for _ in range(entry_level_count)]

    # Calculate averages
    flagship_arpu_avg = (
        sum(flagship_arpus) / len(flagship_arpus) if flagship_arpus else 35.0
    )
    high_end_arpu_avg = (
        sum(high_end_arpus) / len(high_end_arpus) if high_end_arpus else 22.0
    )
    mid_range_arpu_avg = (
        sum(mid_range_arpus) / len(mid_range_arpus) if mid_range_arpus else 12.0
    )
    entry_level_arpu_avg = (
        sum(entry_level_arpus) / len(entry_level_arpus) if entry_level_arpus else 6.0
    )

    # Generate edge ratios
    flagship_edge_ratio = generate_edge_ratio_for_tier("flagship")
    high_end_edge_ratio = generate_edge_ratio_for_tier("high_end")
    mid_range_edge_ratio = generate_edge_ratio_for_tier("mid_range")
    entry_level_edge_ratio = generate_edge_ratio_for_tier("entry_level")

    return {
        "site_id": site_id,
        "city": city,
        "total_users": total_users,
        "flagship": {
            "count": flagship_count,
            "pct": round(100 * flagship_count / total_users, 1),
            "avg_arpu": round(flagship_arpu_avg, 1),
            "edge_ratio": round(flagship_edge_ratio, 2),
        },
        "high_end": {
            "count": high_end_count,
            "pct": round(100 * high_end_count / total_users, 1),
            "avg_arpu": round(high_end_arpu_avg, 1),
            "edge_ratio": round(high_end_edge_ratio, 2),
        },
        "mid_range": {
            "count": mid_range_count,
            "pct": round(100 * mid_range_count / total_users, 1),
            "avg_arpu": round(mid_range_arpu_avg, 1),
            "edge_ratio": round(mid_range_edge_ratio, 2),
        },
        "entry_level": {
            "count": entry_level_count,
            "pct": round(100 * entry_level_count / total_users, 1),
            "avg_arpu": round(entry_level_arpu_avg, 1),
            "edge_ratio": round(entry_level_edge_ratio, 2),
        },
    }


def generate_terminals_data():
    """Generate complete terminals dataset"""
    sites_by_city = load_sites()
    terminals_records = []

    # Generate one record per site
    for city, sites in sorted(sites_by_city.items()):
        for site in sites:
            record = generate_terminals_record(site["site_id"], city)
            terminals_records.append(record)

    return terminals_records


def main():
    """Main entry point"""
    print("Generating Terminals data...")

    # Generate data
    terminals_data = generate_terminals_data()

    print(f"Generated {len(terminals_data)} terminals records")

    # Statistics by city
    city_stats = defaultdict(
        lambda: {
            "count": 0,
            "flagship_pcts": [],
            "entry_level_pcts": [],
            "flagship_edge_ratios": [],
            "entry_level_edge_ratios": [],
            "arpu_by_tier": defaultdict(list),
        }
    )

    for record in terminals_data:
        city = record["city"]
        city_stats[city]["count"] += 1
        city_stats[city]["flagship_pcts"].append(record["flagship"]["pct"])
        city_stats[city]["entry_level_pcts"].append(record["entry_level"]["pct"])
        city_stats[city]["flagship_edge_ratios"].append(record["flagship"]["edge_ratio"])
        city_stats[city]["entry_level_edge_ratios"].append(record["entry_level"]["edge_ratio"])

        for tier in ["flagship", "high_end", "mid_range", "entry_level"]:
            city_stats[city]["arpu_by_tier"][tier].append(record[tier]["avg_arpu"])

    print("\nTerminals distribution by city:")
    for city in sorted(city_stats.keys()):
        stats = city_stats[city]
        count = stats["count"]
        avg_flagship_pct = sum(stats["flagship_pcts"]) / len(stats["flagship_pcts"])
        avg_entry_pct = sum(stats["entry_level_pcts"]) / len(stats["entry_level_pcts"])

        avg_flagship_edge = sum(stats["flagship_edge_ratios"]) / len(
            stats["flagship_edge_ratios"]
        )
        avg_entry_edge = sum(stats["entry_level_edge_ratios"]) / len(
            stats["entry_level_edge_ratios"]
        )

        print(f"  {city}: {count} sites")
        print(f"    Flagship: {avg_flagship_pct:.1f}% (edge ratio: {avg_flagship_edge:.2f})")
        print(f"    Entry-level: {avg_entry_pct:.1f}% (edge ratio: {avg_entry_edge:.2f})")

    # Verify ARPU hierarchy
    print(f"\nARPU hierarchy verification:")
    all_arpus = defaultdict(list)
    for record in terminals_data:
        for tier in ["flagship", "high_end", "mid_range", "entry_level"]:
            all_arpus[tier].append(record[tier]["avg_arpu"])

    for tier in ["flagship", "high_end", "mid_range", "entry_level"]:
        avg = sum(all_arpus[tier]) / len(all_arpus[tier])
        print(f"  {tier}: avg ${avg:.2f}")

    # Verify edge ratio hierarchy: flagship < entry_level
    print(f"\nEdge zone distribution hierarchy:")
    flagship_edges = [r["flagship"]["edge_ratio"] for r in terminals_data]
    entry_edges = [r["entry_level"]["edge_ratio"] for r in terminals_data]
    print(
        f"  Flagship avg edge ratio: {sum(flagship_edges)/len(flagship_edges):.2f}"
    )
    print(f"  Entry-level avg edge ratio: {sum(entry_edges)/len(entry_edges):.2f}")

    # Save to file
    output_path = Path(__file__).parent.parent / "terminals.json"
    with open(output_path, "w") as f:
        json.dump(terminals_data, f, indent=2)

    print(f"\nData saved to {output_path}")


if __name__ == "__main__":
    main()
