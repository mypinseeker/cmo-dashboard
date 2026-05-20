#!/usr/bin/env python3
"""
Ookla Speedtest Data Generator for CMO Dashboard
Generates realistic speedtest data with operator-specific characteristics.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Operator profiles with network characteristics
OPERATORS = {
    "Tigo": {
        "base_dl_mbps": 38,
        "base_ul_mbps": 8.5,
        "base_latency_ms": 32,
        "strong_cities": ["Bogota", "Medellin"],
        "weak_cities": ["Barranquilla", "Cartagena"],
        "city_multiplier": {
            "Bogota": 1.15,
            "Medellin": 1.10,
            "Cali": 1.0,
            "Barranquilla": 0.50,
            "Cartagena": 0.60,
        },
        "test_count": 4000,  # Per quarter
    },
    "Claro": {
        "base_dl_mbps": 42,
        "base_ul_mbps": 9.2,
        "base_latency_ms": 28,
        "strong_cities": ["Bogota", "Cali", "Barranquilla"],
        "weak_cities": ["Medellin"],
        "city_multiplier": {
            "Bogota": 1.10,
            "Medellin": 0.85,
            "Cali": 1.05,
            "Barranquilla": 1.10,
            "Cartagena": 1.0,
        },
        "test_count": 4500,  # Per quarter
    },
    "Movistar": {
        "base_dl_mbps": 28,
        "base_ul_mbps": 6.8,
        "base_latency_ms": 45,
        "strong_cities": ["Cali"],
        "weak_cities": ["Bogota", "Barranquilla", "Cartagena"],
        "city_multiplier": {
            "Bogota": 0.90,
            "Medellin": 0.95,
            "Cali": 1.15,
            "Barranquilla": 0.80,
            "Cartagena": 0.85,
        },
        "test_count": 2500,  # Per quarter
    },
}

# Device profiles
DEVICE_PROFILES = {
    "flagship": {"models": ["iPhone 16", "Samsung Galaxy S25"], "weight": 0.15},
    "premium": {"models": ["iPhone 15", "Samsung Galaxy S24", "OnePlus 13"], "weight": 0.20},
    "midrange": {"models": ["Samsung Galaxy A55", "Motorola G85", "Xiaomi Redmi Note 14"], "weight": 0.35},
    "budget": {"models": ["Samsung Galaxy A15", "Xiaomi Redmi 13", "Poco M6"], "weight": 0.30},
}

QUARTERS = [
    {"period": "2025-Q4", "start": datetime(2025, 10, 1), "end": datetime(2025, 12, 31)},
    {"period": "2026-Q1", "start": datetime(2026, 1, 1), "end": datetime(2026, 3, 31)},
]


def load_sites():
    """Load sites from sites.json"""
    sites_path = Path(__file__).parent.parent / "sites.json"
    with open(sites_path, "r") as f:
        return json.load(f)


def get_device_info():
    """Select device based on category distribution"""
    rand = random.random()
    cumulative = 0

    for category, profile in DEVICE_PROFILES.items():
        cumulative += profile["weight"]
        if rand <= cumulative:
            return {
                "model": random.choice(profile["models"]),
                "category": category,
            }

    # Fallback (shouldn't happen)
    return {"model": "Samsung Galaxy A55", "category": "midrange"}


def generate_signal_strength():
    """
    Generate signal strength (RSRP) following normal distribution.
    Range: -70 to -130 dBm, mean: -90 dBm
    """
    mean, std_dev = -90, 12
    signal = random.gauss(mean, std_dev)
    # Clamp to realistic range (note: -70 is stronger than -130)
    return max(-130, min(-70, signal))


def apply_signal_impact_on_speed(base_speed, signal_strength):
    """
    Apply signal strength impact on speed performance.
    Strong signal (-85 dBm and above): maintain/exceed base
    Weak signal (-105 dBm and below): sharp degradation
    """
    if signal_strength > -85:
        # Strong signal: boost speed by 5-15%
        multiplier = 1.0 + random.uniform(0.05, 0.15)
    elif signal_strength < -105:
        # Weak signal: degradation to 40-70% of base
        multiplier = random.uniform(0.40, 0.70)
    else:
        # Moderate signal: small variation ±10%
        multiplier = random.uniform(0.90, 1.10)

    return base_speed * multiplier


def generate_test_record(test_id, site, operator, quarter_info):
    """Generate a single speedtest record"""
    operator_config = OPERATORS[operator]

    # Random timestamp within quarter
    start_dt = quarter_info["start"]
    end_dt = quarter_info["end"]
    random_days = random.randint(0, (end_dt - start_dt).days)
    random_seconds = random.randint(0, 86399)
    timestamp = start_dt + timedelta(days=random_days, seconds=random_seconds)

    # Location: add small random offset to site location (0-2km)
    lat_offset = random.gauss(0, 0.01)  # ~1.1km per 0.01 degrees
    lon_offset = random.gauss(0, 0.01)
    latitude = site["latitude"] + lat_offset
    longitude = site["longitude"] + lon_offset

    # City and apply city multiplier
    city = site["city"]
    city_mult = operator_config["city_multiplier"].get(city, 1.0)

    # Apply Q1-2026 improvement (Tigo +5%)
    if quarter_info["period"] == "2026-Q1" and operator == "Tigo":
        q1_boost = 1.05
    else:
        q1_boost = 1.0

    # Generate signal strength first
    signal_strength = generate_signal_strength()

    # Base speeds with city multiplier and quarter improvement
    base_dl = operator_config["base_dl_mbps"] * city_mult * q1_boost
    base_ul = operator_config["base_ul_mbps"] * city_mult * q1_boost
    base_latency = operator_config["base_latency_ms"]

    # Apply signal strength impact on download speed
    download_mbps = apply_signal_impact_on_speed(base_dl, signal_strength)
    download_mbps = max(2.0, download_mbps)  # Minimum realistic speed

    # Apply signal strength impact on upload speed (less sensitive)
    upload_signal_impact = apply_signal_impact_on_speed(base_ul, signal_strength + 5)
    upload_mbps = max(1.0, upload_signal_impact)

    # Latency varies inversely with signal strength
    if signal_strength > -85:
        latency_ms = base_latency * random.uniform(0.8, 1.0)
    elif signal_strength < -105:
        latency_ms = base_latency * random.uniform(1.3, 1.8)
    else:
        latency_ms = base_latency * random.uniform(0.95, 1.15)

    # Jitter (typically 2-8ms, more on weak signals)
    if signal_strength < -105:
        jitter_ms = random.uniform(8, 15)
    else:
        jitter_ms = random.uniform(2, 8)

    # Device info
    device_info = get_device_info()

    # Technology type
    technology = random.choice(site.get("technology", ["4G", "5G"]))

    return {
        "test_id": test_id,
        "timestamp": timestamp.isoformat(),
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "city": city,
        "operator": operator,
        "technology": technology,
        "download_mbps": round(download_mbps, 1),
        "upload_mbps": round(upload_mbps, 1),
        "latency_ms": round(latency_ms, 1),
        "jitter_ms": round(jitter_ms, 1),
        "signal_strength_dbm": round(signal_strength, 1),
        "device_model": device_info["model"],
        "device_category": device_info["category"],
        "period": quarter_info["period"],
    }


def generate_ookla_data():
    """Generate complete Ookla dataset"""
    sites = load_sites()
    ookla_records = []
    test_counter = 1

    # For each quarter
    for quarter_info in QUARTERS:
        # For each operator
        for operator, config in OPERATORS.items():
            test_count = config["test_count"]

            # Generate test_count records
            for _ in range(test_count):
                # Pick a random site
                site = random.choice(sites)

                # Generate test_id
                test_id = f"ookla-co-{quarter_info['start'].strftime('%Y%m%d')}-{test_counter:05d}"

                # Generate record
                record = generate_test_record(test_id, site, operator, quarter_info)
                ookla_records.append(record)

                test_counter += 1

    # Shuffle to mix quarters and operators
    random.shuffle(ookla_records)

    return ookla_records


def main():
    """Main entry point"""
    print("Generating Ookla Speedtest data...")

    # Generate data
    ookla_data = generate_ookla_data()

    print(f"Generated {len(ookla_data)} test records")

    # Output statistics
    operator_counts = {}
    period_counts = {}
    for record in ookla_data:
        op = record["operator"]
        period = record["period"]
        operator_counts[op] = operator_counts.get(op, 0) + 1
        period_counts[period] = period_counts.get(period, 0) + 1

    print("\nOperator distribution:")
    for op, count in sorted(operator_counts.items()):
        print(f"  {op}: {count} tests")

    print("\nPeriod distribution:")
    for period, count in sorted(period_counts.items()):
        print(f"  {period}: {count} tests")

    # Calculate signal strength stats
    signals = [r["signal_strength_dbm"] for r in ookla_data]
    downloads = [r["download_mbps"] for r in ookla_data]
    print(f"\nSignal strength range: {min(signals):.1f} to {max(signals):.1f} dBm")
    print(f"Signal strength mean: {sum(signals)/len(signals):.1f} dBm")
    print(f"Download speed range: {min(downloads):.1f} to {max(downloads):.1f} Mbps")
    print(f"Download speed mean: {sum(downloads)/len(downloads):.1f} Mbps")

    # Verify signal-speed correlation
    weak_signal = [r["download_mbps"] for r in ookla_data if r["signal_strength_dbm"] < -105]
    strong_signal = [r["download_mbps"] for r in ookla_data if r["signal_strength_dbm"] > -85]
    if weak_signal and strong_signal:
        weak_avg = sum(weak_signal) / len(weak_signal)
        strong_avg = sum(strong_signal) / len(strong_signal)
        print(f"\nSignal correlation verification:")
        print(f"  Weak signal (<-105dBm) avg speed: {weak_avg:.1f} Mbps ({len(weak_signal)} tests)")
        print(f"  Strong signal (>-85dBm) avg speed: {strong_avg:.1f} Mbps ({len(strong_signal)} tests)")
        print(f"  Correlation: {strong_avg/weak_avg:.2f}x faster")

    # Save to file
    output_path = Path(__file__).parent.parent / "ookla.json"
    with open(output_path, "w") as f:
        json.dump(ookla_data, f, indent=2)

    print(f"\nData saved to {output_path}")


if __name__ == "__main__":
    main()
