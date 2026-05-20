import json
import random
import os

random.seed(42)

CITIES = {
    "Bogota": {
        "department": "Cundinamarca",
        "region": "Central",
        "lat_range": (4.55, 4.75),
        "lon_range": (-74.15, -74.00),
        "site_count": 100,
    },
    "Medellin": {
        "department": "Antioquia",
        "region": "Northwest",
        "lat_range": (6.18, 6.30),
        "lon_range": (-75.62, -75.52),
        "site_count": 80,
    },
    "Cali": {
        "department": "Valle del Cauca",
        "region": "Southwest",
        "lat_range": (3.38, 3.48),
        "lon_range": (-76.56, -76.48),
        "site_count": 70,
    },
    "Barranquilla": {
        "department": "Atlantico",
        "region": "North Coast",
        "lat_range": (10.95, 11.02),
        "lon_range": (-74.82, -74.76),
        "site_count": 60,
    },
    "Cartagena": {
        "department": "Bolivar",
        "region": "North Coast",
        "lat_range": (10.38, 10.44),
        "lon_range": (-75.55, -75.49),
        "site_count": 50,
    },
}

# 频段组合
BAND_CONFIGS = [
    ["B28 (700MHz)", "B2 (1900MHz)", "B4 (AWS)", "B7 (2600MHz)"],  # 全频段
    ["B2 (1900MHz)", "B4 (AWS)", "B7 (2600MHz)"],  # 无低频
    ["B28 (700MHz)", "B2 (1900MHz)", "B4 (AWS)"],   # 无高频
    ["B2 (1900MHz)", "B4 (AWS)"],                    # 基础配置
]

VENDORS = ["Ericsson", "Huawei", "Nokia"]
SITE_TYPES = ["macro", "micro", "small_cell"]

def generate_site(site_id, city_name, city_config, idx):
    lat = random.uniform(*city_config["lat_range"])
    lon = random.uniform(*city_config["lon_range"])

    # 大部分是 macro
    site_type = random.choices(SITE_TYPES, weights=[0.75, 0.15, 0.10])[0]
    bands = random.choice(BAND_CONFIGS)
    has_5g = random.random() < 0.15  # 15% 站点有 5G
    tech = ["4G", "5G"] if has_5g else ["4G"]
    if random.random() < 0.3:
        tech = ["3G"] + tech  # 30% 还有 3G

    vendor = random.choices(VENDORS, weights=[0.50, 0.30, 0.20])[0]

    return {
        "site_id": f"CO-{city_name[:3].upper()}-{idx:03d}",
        "site_name": f"{city_name} Site {idx}",
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "city": city_name,
        "department": city_config["department"],
        "region": city_config["region"],
        "site_type": site_type,
        "bands": bands,
        "technology": tech,
        "antenna_height_m": random.choice([25, 30, 35, 40, 45]),
        "azimuth_sectors": [0, 120, 240],
        "vendor": vendor,
        "status": "active",
        "commission_date": f"20{random.randint(15,25)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
    }

def main():
    sites = []
    for city_name, config in CITIES.items():
        for i in range(1, config["site_count"] + 1):
            site = generate_site(
                f"CO-{city_name[:3].upper()}-{i:03d}",
                city_name, config, i
            )
            sites.append(site)

    # Rural sites
    for i in range(1, 41):
        rural_config = {
            "department": "Rural",
            "region": "Rural",
            "lat_range": (4.0, 10.0),
            "lon_range": (-76.0, -74.0),
        }
        site = generate_site(f"CO-RUR-{i:03d}", "Rural", rural_config, i)
        site["site_type"] = "macro"
        site["bands"] = ["B28 (700MHz)", "B2 (1900MHz)"]  # 农村只有基础频段
        site["technology"] = ["4G"]
        sites.append(site)

    output_path = os.path.join(os.path.dirname(__file__), "..", "sites.json")
    with open(output_path, "w") as f:
        json.dump(sites, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(sites)} sites")

    # 按城市统计
    from collections import Counter
    city_counts = Counter(s["city"] for s in sites)
    for city, count in city_counts.most_common():
        print(f"  {city}: {count} sites")

if __name__ == "__main__":
    main()
