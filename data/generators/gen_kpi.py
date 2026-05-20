#!/usr/bin/env python3
"""
T-02 KPI Data Generator
Generates 30-day hourly-level wireless and network KPI data for 400 sites.
- Recent 7 days (5/13-5/19): hourly granularity (~67K records)
- Previous 23 days (4/20-5/12): daily aggregates (~9.2K records)
Total: ~76K records

Output:
  - data/radio_kpi.json
  - data/network_kpi.json
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import math

# ============================================================================
# Configuration
# ============================================================================

HOUR_WEIGHTS = {
    0: 0.15, 1: 0.10, 2: 0.08, 3: 0.07, 4: 0.07, 5: 0.10,
    6: 0.25, 7: 0.40, 8: 0.55, 9: 0.65, 10: 0.70, 11: 0.75,
    12: 0.80, 13: 0.72, 14: 0.65, 15: 0.60, 16: 0.65, 17: 0.72,
    18: 0.82, 19: 0.90, 20: 0.95, 21: 0.92, 22: 0.70, 23: 0.40,
}

CITY_PROFILES = {
    "Bogota": {"base_prb": 55, "base_users": 1200, "base_dl_gb": 80, "quality": "good"},
    "Medellin": {"base_prb": 50, "base_users": 900, "base_dl_gb": 65, "quality": "good"},
    "Cali": {"base_prb": 58, "base_users": 800, "base_dl_gb": 55, "quality": "medium"},
    "Barranquilla": {"base_prb": 72, "base_users": 650, "base_dl_gb": 45, "quality": "poor"},
    "Cartagena": {"base_prb": 68, "base_users": 550, "base_dl_gb": 40, "quality": "poor"},
    "Rural": {"base_prb": 35, "base_users": 200, "base_dl_gb": 15, "quality": "medium"},
}

# ============================================================================
# Data Loading
# ============================================================================

def load_sites(sites_file):
    """Load sites from JSON."""
    with open(sites_file, 'r') as f:
        return json.load(f)

# ============================================================================
# Trending Sites (Alarm Demo)
# ============================================================================

def select_trending_sites(sites):
    """
    Select 5-8 sites for PRB uptrend (alarm demo).
    - Barranquilla: 3 sites
    - Cartagena: 2 sites
    - Other: 0-2 random sites
    """
    barranquilla_sites = [s for s in sites if s['city'] == 'Barranquilla']
    cartagena_sites = [s for s in sites if s['city'] == 'Cartagena']
    other_sites = [s for s in sites if s['city'] not in ['Barranquilla', 'Cartagena']]

    trending = []
    trending.extend(random.sample(barranquilla_sites, min(3, len(barranquilla_sites))))
    trending.extend(random.sample(cartagena_sites, min(2, len(cartagena_sites))))
    trending.extend(random.sample(other_sites, min(2, len(other_sites))))

    return {s['site_id'] for s in trending}

# ============================================================================
# KPI Generation
# ============================================================================

def gauss_noise(mean, std_pct=5.0):
    """Add Gaussian noise as percentage of mean."""
    noise = random.gauss(0, mean * std_pct / 100.0)
    return mean + noise

def get_hour_weight(dt, is_weekend):
    """Get traffic weight for hour, with weekend adjustment."""
    hour = dt.hour
    base_weight = HOUR_WEIGHTS[hour]

    # Weekend: slight reduction daytime, slight increase evening
    if is_weekend:
        if 6 <= hour <= 18:
            base_weight *= 0.92
        else:
            base_weight *= 1.05

    return base_weight

def generate_radio_kpi(site, timestamp, city_profile, is_trending, day_of_month):
    """Generate radio KPI for a site at a timestamp."""

    dt = datetime.fromisoformat(timestamp)
    is_weekend = dt.weekday() >= 5
    hour_weight = get_hour_weight(dt, is_weekend)

    # Base PRB utilization
    base_prb_dl = city_profile['base_prb']
    base_prb_ul = base_prb_dl * 0.6  # UL typically lower

    # Trending sites: linear increase from 65% to 92% over 30 days (absolute, not relative)
    if is_trending:
        # Linear progression: day 1 = 65%, day 30 = 92%
        base_prb_dl = 65 + (27 * (day_of_month - 1) / 29)
        base_prb_ul = base_prb_dl * 0.6
        # Slight hour weight for trending sites too (don't let it swing too much)
        prb_dl = base_prb_dl + (base_prb_dl * (hour_weight - 0.5) * 0.3)
        prb_ul = base_prb_ul + (base_prb_ul * (hour_weight - 0.5) * 0.3)
    else:
        prb_dl = base_prb_dl + gauss_noise(0, 8.0)
        prb_ul = base_prb_ul + gauss_noise(0, 8.0)
        # Hour weight modulation for normal sites
        prb_dl = prb_dl * hour_weight
        prb_ul = prb_ul * hour_weight

    # Clamp to [0, 100]
    prb_dl = max(0, min(100, prb_dl))
    prb_ul = max(0, min(100, prb_ul))

    # Quality metrics degraded for high-PRB sites
    prb_factor = (prb_dl / 100.0) ** 2  # Quadratic degradation

    if city_profile['quality'] == 'good':
        rsrp = -82 + gauss_noise(0, 3.0) - (prb_factor * 8)
        sinr = 14 + gauss_noise(0, 2.0) - (prb_factor * 5)
        rrc_success = 99.5 - (prb_factor * 1.5)
        erab_success = 99.2 - (prb_factor * 1.2)
        ho_success = 98.5 - (prb_factor * 2.0)
        drop_rate = 0.2 + (prb_factor * 0.8)
    elif city_profile['quality'] == 'medium':
        rsrp = -87 + gauss_noise(0, 4.0) - (prb_factor * 8)
        sinr = 11 + gauss_noise(0, 2.5) - (prb_factor * 4)
        rrc_success = 98.5 - (prb_factor * 2.0)
        erab_success = 98.0 - (prb_factor * 1.5)
        ho_success = 97.0 - (prb_factor * 2.5)
        drop_rate = 0.4 + (prb_factor * 1.0)
    else:  # poor
        rsrp = -92 + gauss_noise(0, 5.0) - (prb_factor * 10)
        sinr = 9 + gauss_noise(0, 3.0) - (prb_factor * 3)
        rrc_success = 97.5 - (prb_factor * 2.5)
        erab_success = 97.0 - (prb_factor * 2.0)
        ho_success = 96.0 - (prb_factor * 3.0)
        drop_rate = 0.8 + (prb_factor * 1.2)

    # Clamp success rates and drop rate
    rrc_success = max(95, min(100, rrc_success))
    erab_success = max(94, min(100, erab_success))
    ho_success = max(93, min(100, ho_success))
    drop_rate = max(0, min(5, drop_rate))

    return {
        "site_id": site['site_id'],
        "timestamp": timestamp,
        "prb_utilization_dl_pct": round(prb_dl, 1),
        "prb_utilization_ul_pct": round(prb_ul, 1),
        "avg_rsrp_dbm": round(rsrp, 1),
        "avg_sinr_db": round(sinr, 1),
        "rrc_setup_success_rate_pct": round(rrc_success, 2),
        "erab_setup_success_rate_pct": round(erab_success, 2),
        "handover_success_rate_pct": round(ho_success, 2),
        "call_drop_rate_pct": round(drop_rate, 2),
    }

def generate_network_kpi(site, timestamp, city_profile, is_trending, day_of_month):
    """Generate network KPI for a site at a timestamp."""

    dt = datetime.fromisoformat(timestamp)
    is_weekend = dt.weekday() >= 5
    hour_weight = get_hour_weight(dt, is_weekend)

    # Base traffic metrics
    base_users = city_profile['base_users']
    base_dl_gb = city_profile['base_dl_gb']

    # User count (connected and active are subsets)
    connected_users = int(base_users * hour_weight * random.uniform(0.9, 1.1))
    active_users = int(connected_users * random.uniform(0.3, 0.5))

    # DL/UL traffic (GB)
    dl_traffic = base_dl_gb * hour_weight * random.uniform(0.85, 1.15)
    ul_traffic = dl_traffic * random.uniform(0.12, 0.18)  # UL ~12-18% of DL

    # Trending sites: slightly lower throughput due to congestion
    throughput_factor = 1.0
    if is_trending:
        trend_degradation = 0.65 + (0.27 * day_of_month / 30)
        throughput_factor = 1.5 - trend_degradation  # Linear decrease

    # DL/UL throughput (Mbps avg)
    if city_profile['quality'] == 'good':
        dl_throughput = 50 * hour_weight * throughput_factor * random.uniform(0.8, 1.2)
        ul_throughput = 12 * hour_weight * throughput_factor * random.uniform(0.8, 1.2)
        latency = 25 + gauss_noise(0, 30)
    elif city_profile['quality'] == 'medium':
        dl_throughput = 35 * hour_weight * throughput_factor * random.uniform(0.8, 1.2)
        ul_throughput = 8 * hour_weight * throughput_factor * random.uniform(0.8, 1.2)
        latency = 40 + gauss_noise(0, 40)
    else:  # poor
        dl_throughput = 20 * hour_weight * throughput_factor * random.uniform(0.7, 1.1)
        ul_throughput = 5 * hour_weight * throughput_factor * random.uniform(0.7, 1.1)
        latency = 65 + gauss_noise(0, 50)

    # Clamp metrics
    connected_users = max(0, connected_users)
    active_users = max(0, min(connected_users, active_users))
    dl_traffic = max(0, dl_traffic)
    ul_traffic = max(0, ul_traffic)
    dl_throughput = max(0, dl_throughput)
    ul_throughput = max(0, ul_throughput)
    latency = max(0, latency)

    return {
        "site_id": site['site_id'],
        "timestamp": timestamp,
        "connected_users": int(connected_users),
        "active_users": int(active_users),
        "dl_traffic_gb": round(dl_traffic, 1),
        "ul_traffic_gb": round(ul_traffic, 1),
        "dl_throughput_mbps_avg": round(dl_throughput, 1),
        "ul_throughput_mbps_avg": round(ul_throughput, 1),
        "latency_ms_avg": round(latency, 1),
    }

# ============================================================================
# Main
# ============================================================================

def main():
    # Setup
    project_root = Path(__file__).parent.parent.parent
    sites_file = project_root / 'data' / 'sites.json'
    radio_kpi_file = project_root / 'data' / 'radio_kpi.json'
    network_kpi_file = project_root / 'data' / 'network_kpi.json'

    print(f"Loading sites from {sites_file}...")
    sites = load_sites(sites_file)
    print(f"Loaded {len(sites)} sites")

    # Select trending sites for alarm demo
    trending_sites = select_trending_sites(sites)
    print(f"Selected {len(trending_sites)} sites for PRB uptrend demo")

    # Date ranges
    start_date = datetime(2026, 4, 20, 0, 0, 0)
    end_date = datetime(2026, 5, 19, 23, 0, 0)
    recent_start = datetime(2026, 5, 13, 0, 0, 0)  # Last 7 days

    print(f"Generating KPI data from {start_date} to {end_date}...")

    radio_kpis = []
    network_kpis = []

    # Generate data
    current = start_date
    day_count = 0

    while current <= end_date:
        day_count += 1
        day_of_month = (current - start_date).days + 1

        if current >= recent_start:
            # Recent 7 days: hourly granularity
            for hour in range(24):
                ts = current.replace(hour=hour)
                timestamp_str = ts.isoformat()

                for site in sites:
                    city = site['city']
                    city_profile = CITY_PROFILES[city]
                    is_trending = site['site_id'] in trending_sites

                    radio_kpi = generate_radio_kpi(site, timestamp_str, city_profile, is_trending, day_of_month)
                    network_kpi = generate_network_kpi(site, timestamp_str, city_profile, is_trending, day_of_month)

                    radio_kpis.append(radio_kpi)
                    network_kpis.append(network_kpi)
        else:
            # Previous 23 days: daily aggregate (noon)
            ts = current.replace(hour=12)
            timestamp_str = ts.isoformat()

            for site in sites:
                city = site['city']
                city_profile = CITY_PROFILES[city]
                is_trending = site['site_id'] in trending_sites

                radio_kpi = generate_radio_kpi(site, timestamp_str, city_profile, is_trending, day_of_month)
                network_kpi = generate_network_kpi(site, timestamp_str, city_profile, is_trending, day_of_month)

                radio_kpis.append(radio_kpi)
                network_kpis.append(network_kpi)

        current += timedelta(days=1)

    # Write output files
    print(f"Writing {len(radio_kpis)} radio KPI records...")
    with open(radio_kpi_file, 'w') as f:
        json.dump(radio_kpis, f, indent=2)

    print(f"Writing {len(network_kpis)} network KPI records...")
    with open(network_kpi_file, 'w') as f:
        json.dump(network_kpis, f, indent=2)

    print(f"\nGeneration complete!")
    print(f"  Radio KPI: {radio_kpi_file}")
    print(f"  Network KPI: {network_kpi_file}")
    print(f"  Total records: {len(radio_kpis) + len(network_kpis)}")

if __name__ == '__main__':
    main()
