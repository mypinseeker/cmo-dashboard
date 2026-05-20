#!/usr/bin/env python3
"""
Churn Data Generator for CMO Dashboard
Generates monthly churn records with realistic patterns based on experience and device segments.
"""

import json
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

random.seed(42)

# Cities with churn characteristics
CITIES = {
    "Bogota": {
        "base_churn_rate": 0.012,
        "arpu_multiplier": 1.3,
        "premium_users_pct": 0.35,
    },
    "Medellin": {
        "base_churn_rate": 0.015,
        "arpu_multiplier": 1.1,
        "premium_users_pct": 0.25,
    },
    "Cali": {
        "base_churn_rate": 0.016,
        "arpu_multiplier": 0.95,
        "premium_users_pct": 0.20,
    },
    "Barranquilla": {
        "base_churn_rate": 0.025,  # Highest churn
        "arpu_multiplier": 0.8,
        "premium_users_pct": 0.15,
    },
    "Cartagena": {
        "base_churn_rate": 0.022,
        "arpu_multiplier": 0.85,
        "premium_users_pct": 0.18,
    },
    "Rural": {
        "base_churn_rate": 0.018,
        "arpu_multiplier": 0.6,
        "premium_users_pct": 0.08,
    },
}

# Device categories with ARPU and experience correlation
DEVICE_CATEGORIES = {
    "flagship": {
        "arpu_multiplier": 3.5,
        "weight": 0.12,
        "experience_boost": 1.2,  # Better experience
    },
    "high_end": {
        "arpu_multiplier": 2.2,
        "weight": 0.18,
        "experience_boost": 1.1,
    },
    "mid_range": {
        "arpu_multiplier": 1.0,
        "weight": 0.45,
        "experience_boost": 0.95,
    },
    "entry_level": {
        "arpu_multiplier": 0.5,
        "weight": 0.25,
        "experience_boost": 0.75,
    },
}

# Major sites from sites.json (we'll load these)
SITE_IDS = None


def load_sites():
    """Load site IDs from sites.json"""
    global SITE_IDS
    sites_path = Path(__file__).parent.parent / "sites.json"
    with open(sites_path, "r") as f:
        sites = json.load(f)

    # Build site_id -> city mapping
    site_map = {}
    for site in sites:
        site_map[site["site_id"]] = site["city"]

    SITE_IDS = site_map
    return site_map


def generate_imsi_hash(idx):
    """Generate a consistent but realistic IMSI hash"""
    imsi_str = f"12345678901{idx:010d}"
    return hashlib.sha256(imsi_str.encode()).hexdigest()[:16]


def get_device_category():
    """Select device category based on distribution"""
    rand = random.random()
    cumulative = 0

    for category, config in DEVICE_CATEGORIES.items():
        cumulative += config["weight"]
        if rand <= cumulative:
            return category

    return "mid_range"


def generate_churn_record(idx, city, site_id, experience_score, device_category):
    """Generate a single churn record"""

    # Calculate ARPU based on device and city
    base_arpu = 15.0  # Base ARPU in USD
    device_mult = DEVICE_CATEGORIES[device_category]["arpu_multiplier"]
    city_mult = CITIES[city]["arpu_multiplier"]
    arpu = base_arpu * device_mult * city_mult

    # Add some variation
    arpu = arpu * random.uniform(0.85, 1.15)

    # Tenure: 1-60 months, weighted towards shorter tenure (churn bias)
    tenure_months = int(random.betavariate(2, 3) * 60)  # Beta distribution favors lower values
    tenure_months = max(1, tenure_months)

    # Last active date (churned within last 60 days)
    last_active_date = datetime.now() - timedelta(days=random.randint(1, 60))

    # Plan type: 70% prepaid, 30% postpaid
    plan_type = "prepaid" if random.random() < 0.7 else "postpaid"

    # Last 30d avg DL speed correlated with experience
    # Bad experience -> low speed -> high churn
    if experience_score < 2.5:
        avg_dl_mbps = random.uniform(5.0, 12.0)
    elif experience_score < 3.0:
        avg_dl_mbps = random.uniform(10.0, 20.0)
    elif experience_score < 3.5:
        avg_dl_mbps = random.uniform(15.0, 28.0)
    else:
        avg_dl_mbps = random.uniform(25.0, 45.0)

    return {
        "imsi_hash": generate_imsi_hash(idx),
        "status": "churned_60d",
        "last_active_date": last_active_date.strftime("%Y-%m-%d"),
        "tenure_months": tenure_months,
        "monthly_arpu_usd": round(arpu, 2),
        "primary_site_id": site_id,
        "primary_city": city,
        "last_30d_experience_score": round(experience_score, 1),
        "last_30d_avg_dl_mbps": round(avg_dl_mbps, 1),
        "device_category": device_category,
        "plan_type": plan_type,
    }


def generate_churn_data():
    """Generate complete churn dataset"""
    site_map = load_sites()
    churn_records = []

    # Target: ~15,000 records total
    # Base on city churn rates
    total_target = 15000

    city_allocation = {}
    total_weight = 0

    # Calculate weighted allocation
    for city, config in CITIES.items():
        weight = config["base_churn_rate"]
        city_allocation[city] = weight
        total_weight += weight

    # Allocate records by city
    city_record_counts = {}
    for city, weight in city_allocation.items():
        count = int(total_target * weight / total_weight)
        city_record_counts[city] = count

    idx = 1

    for city, target_count in city_record_counts.items():
        # Get sites for this city
        city_sites = [sid for sid, c in site_map.items() if c == city]

        if not city_sites:
            continue

        for _ in range(target_count):
            # Select random site in city
            site_id = random.choice(city_sites)

            # Select device category
            device_category = get_device_category()

            # Experience score influences churn:
            # <2.5: high churn area
            # 2.5-3.5: medium churn
            # >4.0: low churn
            # Also influenced by device quality
            device_boost = DEVICE_CATEGORIES[device_category]["experience_boost"]

            # Base experience on city and device, then add noise
            base_experience = 2.0 + random.random() * 2.5  # 2.0 to 4.5
            experience_score = base_experience * device_boost
            experience_score = max(1.0, min(5.0, experience_score + random.gauss(0, 0.3)))

            record = generate_churn_record(idx, city, site_id, experience_score, device_category)
            churn_records.append(record)

            idx += 1

    return churn_records


def main():
    """Main entry point"""
    print("Generating Churn data...")

    # Generate data
    churn_data = generate_churn_data()

    print(f"Generated {len(churn_data)} churn records")

    # Statistics by city
    city_counts = defaultdict(int)
    city_exp_scores = defaultdict(list)
    city_arpu = defaultdict(list)
    device_counts = defaultdict(int)

    for record in churn_data:
        city = record["primary_city"]
        city_counts[city] += 1
        city_exp_scores[city].append(record["last_30d_experience_score"])
        city_arpu[city].append(record["monthly_arpu_usd"])
        device_counts[record["device_category"]] += 1

    print("\nChurn distribution by city:")
    for city in sorted(city_counts.keys()):
        count = city_counts[city]
        avg_exp = sum(city_exp_scores[city]) / len(city_exp_scores[city])
        avg_arpu = sum(city_arpu[city]) / len(city_arpu[city])
        churn_rate = CITIES.get(city, {}).get("base_churn_rate", 0)
        print(f"  {city}: {count} records (exp={avg_exp:.2f}, arpu=${avg_arpu:.2f}, expected_rate={churn_rate:.1%})")

    print("\nDevice distribution:")
    for device, count in sorted(device_counts.items(), key=lambda x: -x[1]):
        pct = 100 * count / len(churn_data)
        print(f"  {device}: {count} ({pct:.1f}%)")

    # Verify experience-churn correlation
    bad_exp = [r for r in churn_data if r["last_30d_experience_score"] < 2.5]
    good_exp = [r for r in churn_data if r["last_30d_experience_score"] > 4.0]
    print(f"\nExperience correlation check:")
    print(f"  Bad experience (<2.5): {len(bad_exp)} records ({100*len(bad_exp)/len(churn_data):.1f}%)")
    print(f"  Good experience (>4.0): {len(good_exp)} records ({100*len(good_exp)/len(churn_data):.1f}%)")

    # Verify device segmentation for high-value users
    high_value_device = [r for r in churn_data if r["device_category"] in ["flagship", "high_end"]]
    print(f"  High-value device users: {len(high_value_device)} records ({100*len(high_value_device)/len(churn_data):.1f}%)")

    # Plan distribution
    prepaid = [r for r in churn_data if r["plan_type"] == "prepaid"]
    print(f"\nPlan distribution:")
    print(f"  Prepaid: {len(prepaid)} ({100*len(prepaid)/len(churn_data):.1f}%)")
    print(f"  Postpaid: {len(churn_data) - len(prepaid)} ({100*(len(churn_data)-len(prepaid))/len(churn_data):.1f}%)")

    # Save to file
    output_path = Path(__file__).parent.parent / "churn.json"
    with open(output_path, "w") as f:
        json.dump(churn_data, f, indent=2)

    print(f"\nData saved to {output_path}")


if __name__ == "__main__":
    main()
