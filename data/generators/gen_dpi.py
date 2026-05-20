#!/usr/bin/env python3
"""
T-04 DPI Data Generator
Generates application traffic and video experience data for 400 sites.
- Recent 7 days (5/13-5/19): hourly granularity (~67K records)
- Previous 23 days (4/20-5/12): daily aggregates (~9.2K records)
Total: ~76K records

Each record includes:
  - app_traffic: YouTube, Netflix, TikTok, WhatsApp, Instagram, Gaming, Other (with data volume, sessions, users)
  - video_experience: YouTube, Netflix (resolution distribution, HD ratio, rebuffer ratio, initial buffer)

Output:
  - data/dpi.json
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import math

# ============================================================================
# Configuration
# ============================================================================

# Hour-based traffic weight (0=night, 1=peak)
HOUR_WEIGHTS = {
    0: 0.15, 1: 0.10, 2: 0.08, 3: 0.07, 4: 0.07, 5: 0.10,
    6: 0.25, 7: 0.40, 8: 0.55, 9: 0.65, 10: 0.70, 11: 0.75,
    12: 0.80, 13: 0.72, 14: 0.65, 15: 0.60, 16: 0.65, 17: 0.72,
    18: 0.82, 19: 0.90, 20: 0.95, 21: 0.92, 22: 0.70, 23: 0.40,
}

# App traffic distribution by time of day
APP_TRAFFIC_PROFILE = {
    "daytime": {  # 6-18
        "YouTube": 0.12,
        "Netflix": 0.06,
        "TikTok": 0.18,
        "WhatsApp": 0.15,
        "Instagram": 0.14,
        "Gaming": 0.08,
        "Other": 0.27,
    },
    "evening": {  # 18-23
        "YouTube": 0.25,
        "Netflix": 0.16,
        "TikTok": 0.15,
        "WhatsApp": 0.08,
        "Instagram": 0.08,
        "Gaming": 0.10,
        "Other": 0.18,
    },
    "night": {  # 23-6
        "YouTube": 0.05,
        "Netflix": 0.04,
        "TikTok": 0.08,
        "WhatsApp": 0.02,
        "Instagram": 0.01,
        "Gaming": 0.15,
        "Other": 0.65,
    },
}

CITY_PROFILES = {
    "Bogota": {"base_users": 1200, "base_dl_gb": 80, "quality": "good", "hd_modifier": 1.0},
    "Medellin": {"base_users": 900, "base_dl_gb": 65, "quality": "good", "hd_modifier": 0.98},
    "Cali": {"base_users": 800, "base_dl_gb": 55, "quality": "medium", "hd_modifier": 0.80},
    "Barranquilla": {"base_users": 650, "base_dl_gb": 45, "quality": "poor", "hd_modifier": 0.85},
    "Cartagena": {"base_users": 550, "base_dl_gb": 40, "quality": "poor", "hd_modifier": 0.85},
    "Rural": {"base_users": 200, "base_dl_gb": 15, "quality": "medium", "hd_modifier": 0.75},
}

# ============================================================================
# Data Loading
# ============================================================================

def load_sites(sites_file):
    """Load sites from JSON."""
    with open(sites_file, 'r') as f:
        return json.load(f)

# ============================================================================
# Utility Functions
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

def get_app_profile(hour):
    """Get app traffic distribution profile for hour."""
    if 6 <= hour < 18:
        return APP_TRAFFIC_PROFILE["daytime"]
    elif 18 <= hour < 23:
        return APP_TRAFFIC_PROFILE["evening"]
    else:
        return APP_TRAFFIC_PROFILE["night"]

# ============================================================================
# DPI Data Generation
# ============================================================================

def generate_app_traffic(site, timestamp, city_profile):
    """
    Generate application traffic breakdown for a site at a timestamp.

    Returns dict with app names -> {dl_gb, sessions, users}
    """
    dt = datetime.fromisoformat(timestamp)
    is_weekend = dt.weekday() >= 5
    hour = dt.hour
    hour_weight = get_hour_weight(dt, is_weekend)

    # Base traffic values from city profile
    base_users = city_profile['base_users']
    base_dl_gb = city_profile['base_dl_gb']

    # Total users and traffic at this timestamp
    total_users = int(base_users * hour_weight * random.uniform(0.9, 1.1))
    total_dl_gb = base_dl_gb * hour_weight * random.uniform(0.85, 1.15)

    # Get app distribution for this hour
    app_profile = get_app_profile(hour)

    app_traffic = {}
    for app_name, traffic_share in app_profile.items():
        # Data volume
        dl_gb = total_dl_gb * traffic_share * random.uniform(0.9, 1.1)

        # Sessions (higher for social/messaging, lower for video)
        if app_name in ["WhatsApp", "Instagram", "TikTok"]:
            sessions = int(total_users * traffic_share * random.uniform(3, 6))
        elif app_name in ["YouTube", "Netflix"]:
            sessions = int(total_users * traffic_share * random.uniform(0.8, 2.0))
        elif app_name == "Gaming":
            sessions = int(total_users * traffic_share * random.uniform(0.3, 0.8))
        else:
            sessions = int(total_users * traffic_share * random.uniform(2, 4))

        # Users (subset of total users)
        users = int(total_users * traffic_share * random.uniform(0.6, 1.0))

        app_traffic[app_name] = {
            "dl_gb": round(dl_gb, 1),
            "sessions": max(1, sessions),
            "users": max(1, users),
        }

    return app_traffic

def generate_video_experience(site, timestamp, city_profile, app_traffic):
    """
    Generate video streaming experience metrics for YouTube and Netflix.

    Returns dict with app names -> {resolution_distribution, hd_ratio_pct, rebuffer_ratio_pct, avg_initial_buffer_ms}
    """
    dt = datetime.fromisoformat(timestamp)
    is_weekend = dt.weekday() >= 5
    hour = dt.hour

    # Base quality degradation factors
    hd_base_modifier = city_profile['hd_modifier']
    quality = city_profile['quality']

    # Peak hours (18-22): worse video quality
    is_peak = 18 <= hour <= 22

    video_experience = {}

    # YouTube
    if app_traffic.get("YouTube", {}).get("sessions", 0) > 0:
        total_yt_sessions = app_traffic["YouTube"]["sessions"]

        # HD ratio calculation
        if is_peak:
            # High peak: lower HD ratio
            hd_ratio = 0.25 * hd_base_modifier * random.uniform(0.9, 1.1)
            rebuffer_ratio = 0.045 * random.uniform(0.9, 1.15)
            avg_buffer_ms = 1200 * random.uniform(0.8, 1.3)
        else:
            # Low peak: higher HD ratio
            hd_ratio = 0.55 * hd_base_modifier * random.uniform(0.9, 1.1)
            rebuffer_ratio = 0.008 * random.uniform(0.7, 1.2)
            avg_buffer_ms = 800 * random.uniform(0.7, 1.2)

        # Quality degradation by city
        if quality == "poor":
            hd_ratio *= 0.65
            rebuffer_ratio *= 2.0
            avg_buffer_ms *= 1.4
        elif quality == "medium":
            hd_ratio *= 0.85
            rebuffer_ratio *= 1.5
            avg_buffer_ms *= 1.2

        hd_ratio = max(0.01, min(1.0, hd_ratio))
        rebuffer_ratio = max(0.0, min(0.15, rebuffer_ratio))
        avg_buffer_ms = max(100, min(3000, avg_buffer_ms))

        # Resolution distribution (2160p, 1080p, 720p, 480p, 360p_below)
        # Higher resolution when HD ratio is high
        if hd_ratio > 0.40:
            res_dist = {
                "2160p": hd_ratio * 0.15,
                "1080p": hd_ratio * 0.85,
                "720p": (1 - hd_ratio) * 0.50,
                "480p": (1 - hd_ratio) * 0.35,
                "360p_below": (1 - hd_ratio) * 0.15,
            }
        else:
            res_dist = {
                "2160p": hd_ratio * 0.10,
                "1080p": hd_ratio * 0.90,
                "720p": (1 - hd_ratio) * 0.45,
                "480p": (1 - hd_ratio) * 0.35,
                "360p_below": (1 - hd_ratio) * 0.20,
            }

        video_experience["YouTube"] = {
            "total_sessions": total_yt_sessions,
            "resolution_distribution": {k: round(v, 2) for k, v in res_dist.items()},
            "hd_ratio_pct": round(hd_ratio * 100, 1),
            "rebuffer_ratio_pct": round(rebuffer_ratio * 100, 1),
            "avg_initial_buffer_ms": round(avg_buffer_ms, 0),
        }

    # Netflix
    if app_traffic.get("Netflix", {}).get("sessions", 0) > 0:
        total_nf_sessions = app_traffic["Netflix"]["sessions"]

        # HD ratio calculation (Netflix typically better quality than YouTube)
        if is_peak:
            hd_ratio = 0.35 * hd_base_modifier * random.uniform(0.9, 1.1)
            rebuffer_ratio = 0.015 * random.uniform(0.8, 1.2)
            avg_buffer_ms = 950 * random.uniform(0.8, 1.2)
        else:
            hd_ratio = 0.65 * hd_base_modifier * random.uniform(0.9, 1.1)
            rebuffer_ratio = 0.005 * random.uniform(0.6, 1.1)
            avg_buffer_ms = 650 * random.uniform(0.7, 1.1)

        # Quality degradation by city
        if quality == "poor":
            hd_ratio *= 0.70
            rebuffer_ratio *= 2.5
            avg_buffer_ms *= 1.5
        elif quality == "medium":
            hd_ratio *= 0.90
            rebuffer_ratio *= 1.6
            avg_buffer_ms *= 1.2

        hd_ratio = max(0.01, min(1.0, hd_ratio))
        rebuffer_ratio = max(0.0, min(0.15, rebuffer_ratio))
        avg_buffer_ms = max(100, min(3000, avg_buffer_ms))

        # Resolution distribution (Netflix typically uses higher resolutions)
        if hd_ratio > 0.50:
            res_dist = {
                "2160p": hd_ratio * 0.20,
                "1080p": hd_ratio * 0.80,
                "720p": (1 - hd_ratio) * 0.45,
                "480p": (1 - hd_ratio) * 0.35,
                "360p_below": (1 - hd_ratio) * 0.20,
            }
        else:
            res_dist = {
                "2160p": hd_ratio * 0.12,
                "1080p": hd_ratio * 0.88,
                "720p": (1 - hd_ratio) * 0.40,
                "480p": (1 - hd_ratio) * 0.35,
                "360p_below": (1 - hd_ratio) * 0.25,
            }

        video_experience["Netflix"] = {
            "total_sessions": total_nf_sessions,
            "resolution_distribution": {k: round(v, 2) for k, v in res_dist.items()},
            "hd_ratio_pct": round(hd_ratio * 100, 1),
            "rebuffer_ratio_pct": round(rebuffer_ratio * 100, 1),
            "avg_initial_buffer_ms": round(avg_buffer_ms, 0),
        }

    return video_experience

def generate_dpi_record(site, timestamp, city_profile):
    """
    Generate a complete DPI record for a site at a timestamp.
    """
    # Generate app traffic first (needed for video experience)
    app_traffic = generate_app_traffic(site, timestamp, city_profile)

    # Generate video experience based on app traffic
    video_experience = generate_video_experience(site, timestamp, city_profile, app_traffic)

    dt = datetime.fromisoformat(timestamp)
    is_recent = dt >= datetime(2026, 5, 13)
    granularity = "hourly" if is_recent else "daily"

    return {
        "site_id": site['site_id'],
        "timestamp": timestamp,
        "granularity": granularity,
        "app_traffic": app_traffic,
        "video_experience": video_experience,
    }

# ============================================================================
# Main
# ============================================================================

def main():
    # Setup
    project_root = Path(__file__).parent.parent.parent
    sites_file = project_root / 'data' / 'sites.json'
    dpi_file = project_root / 'data' / 'dpi.json'

    print(f"Loading sites from {sites_file}...")
    sites = load_sites(sites_file)
    print(f"Loaded {len(sites)} sites")

    # Date ranges
    start_date = datetime(2026, 4, 20, 0, 0, 0)
    end_date = datetime(2026, 5, 19, 23, 0, 0)
    recent_start = datetime(2026, 5, 13, 0, 0, 0)  # Last 7 days

    print(f"Generating DPI data from {start_date} to {end_date}...")

    dpi_records = []

    # Generate data
    current = start_date

    while current <= end_date:
        if current >= recent_start:
            # Recent 7 days: hourly granularity
            for hour in range(24):
                ts = current.replace(hour=hour)
                timestamp_str = ts.isoformat()

                for site in sites:
                    city = site['city']
                    city_profile = CITY_PROFILES[city]

                    dpi_record = generate_dpi_record(site, timestamp_str, city_profile)
                    dpi_records.append(dpi_record)
        else:
            # Previous 23 days: daily aggregate (noon)
            ts = current.replace(hour=12)
            timestamp_str = ts.isoformat()

            for site in sites:
                city = site['city']
                city_profile = CITY_PROFILES[city]

                dpi_record = generate_dpi_record(site, timestamp_str, city_profile)
                dpi_records.append(dpi_record)

        current += timedelta(days=1)

    # Write output file
    print(f"Writing {len(dpi_records)} DPI records to {dpi_file}...")
    with open(dpi_file, 'w') as f:
        json.dump(dpi_records, f, indent=2)

    print(f"✓ DPI data generation complete: {dpi_file}")

    # Summary statistics
    hourly_count = len([r for r in dpi_records if r['granularity'] == 'hourly'])
    daily_count = len([r for r in dpi_records if r['granularity'] == 'daily'])
    print(f"  - Hourly records (recent 7 days): {hourly_count}")
    print(f"  - Daily records (previous 23 days): {daily_count}")
    print(f"  - Total records: {len(dpi_records)}")

if __name__ == "__main__":
    main()
