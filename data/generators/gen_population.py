#!/usr/bin/env python3
"""
Population Grid Data Generator for CMO Dashboard
Generates 500m×500m population grids with coverage and Ookla data availability.
"""

import json
import random
import math
from pathlib import Path
from collections import defaultdict

random.seed(42)

# City boundaries and grid parameters
CITY_GRIDS = {
    "Bogota": {
        "lat_center": 4.610,
        "lon_center": -74.080,
        "lat_range": (4.55, 4.75),
        "lon_range": (-74.15, -74.00),
        "grid_count": 350,
        "population_mean": 8500,
        "population_std_dev": 4000,
        "coverage_probability": 0.85,  # 85% covered
    },
    "Medellin": {
        "lat_center": 6.252,
        "lon_center": -75.563,
        "lat_range": (6.18, 6.30),
        "lon_range": (-75.62, -75.52),
        "grid_count": 280,
        "population_mean": 7200,
        "population_std_dev": 3500,
        "coverage_probability": 0.80,
    },
    "Cali": {
        "lat_center": 3.437,
        "lon_center": -76.521,
        "lat_range": (3.38, 3.48),
        "lon_range": (-76.56, -76.48),
        "grid_count": 250,
        "population_mean": 6800,
        "population_std_dev": 3200,
        "coverage_probability": 0.78,
    },
    "Barranquilla": {
        "lat_center": 10.980,
        "lon_center": -74.797,
        "lat_range": (10.95, 11.02),
        "lon_range": (-74.82, -74.76),
        "grid_count": 220,
        "population_mean": 5500,
        "population_std_dev": 2800,
        "coverage_probability": 0.75,
    },
    "Cartagena": {
        "lat_center": 10.413,
        "lon_center": -75.531,
        "lat_range": (10.38, 10.44),
        "lon_range": (-75.55, -75.49),
        "grid_count": 200,
        "population_mean": 4800,
        "population_std_dev": 2400,
        "coverage_probability": 0.77,
    },
}

# Average household size
HOUSEHOLD_SIZE = 4.1


def load_sites():
    """Load sites and build location index for coverage calculation"""
    sites_path = Path(__file__).parent.parent / "sites.json"
    with open(sites_path, "r") as f:
        sites = json.load(f)

    # Build city -> sites mapping with coordinates
    sites_by_city = defaultdict(list)
    for site in sites:
        sites_by_city[site["city"]].append(
            {
                "site_id": site["site_id"],
                "lat": site["latitude"],
                "lon": site["longitude"],
            }
        )

    return sites_by_city


def distance_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km using Haversine formula"""
    R = 6371  # Earth radius in km
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def find_nearest_site_distance(lat, lon, city_sites):
    """Find distance to nearest Tigo site"""
    if not city_sites:
        return 99.0

    nearest_distance = 99.0
    for site in city_sites:
        dist = distance_km(lat, lon, site["lat"], site["lon"])
        nearest_distance = min(nearest_distance, dist)

    return nearest_distance


def generate_population_grid(grid_id, city, city_config, sites_by_city):
    """Generate a single population grid cell"""

    # Random location within city bounds
    lat = random.uniform(city_config["lat_range"][0], city_config["lat_range"][1])
    lon = random.uniform(city_config["lon_range"][0], city_config["lon_range"][1])

    # Population: normal distribution, but higher density near city center
    dist_to_center = distance_km(
        lat, lon, city_config["lat_center"], city_config["lon_center"]
    )

    # Decay population with distance (closer = higher density)
    distance_decay = math.exp(-dist_to_center / 2.5)  # Exponential decay
    population_base = city_config["population_mean"] * distance_decay
    population_std_dev = city_config["population_std_dev"] * distance_decay

    population = int(random.gauss(population_base, population_std_dev))
    population = max(500, population)  # Minimum 500 people per grid

    # Households
    households = int(population / HOUSEHOLD_SIZE)

    # Tigo coverage decision
    tigo_coverage = random.random() < city_config["coverage_probability"]

    # Calculate nearest site distance
    city_sites = sites_by_city.get(city, [])
    nearest_site_km = (
        find_nearest_site_distance(lat, lon, city_sites) if city_sites else 5.0
    )

    # Claro Ookla samples: always present (competitor samples)
    claro_samples = random.randint(5, 40)

    # Tigo Ookla samples: only if covered
    if tigo_coverage:
        # Closer to site = more samples
        if nearest_site_km < 1.0:
            tigo_samples = random.randint(15, 50)
        elif nearest_site_km < 2.5:
            tigo_samples = random.randint(8, 25)
        else:
            tigo_samples = random.randint(1, 10)
    else:
        tigo_samples = 0

    return {
        "grid_id": grid_id,
        "city": city,
        "lat_center": round(lat, 4),
        "lon_center": round(lon, 4),
        "population": population,
        "households": households,
        "tigo_coverage": tigo_coverage,
        "nearest_tigo_site_km": round(nearest_site_km, 2),
        "ookla_claro_samples": claro_samples,
        "ookla_tigo_samples": tigo_samples,
    }


def generate_population_data(sites_by_city):
    """Generate complete population grid dataset"""
    population_records = []
    grid_counter = 1

    for city, city_config in sorted(CITY_GRIDS.items()):
        grid_count = city_config["grid_count"]

        for _ in range(grid_count):
            grid_id = f"GR-{city[:3].upper()}-{grid_counter:03d}"
            record = generate_population_grid(grid_id, city, city_config, sites_by_city)
            population_records.append(record)
            grid_counter += 1

    return population_records


def main():
    """Main entry point"""
    print("Generating Population grid data...")

    # Load sites for coverage calculation
    sites_by_city = load_sites()

    # Generate data
    population_data = generate_population_data(sites_by_city)

    print(f"Generated {len(population_data)} population grids")

    # Statistics by city
    city_stats = defaultdict(
        lambda: {
            "count": 0,
            "total_population": 0,
            "total_households": 0,
            "covered_grids": 0,
            "coverage_pct_list": [],
            "nearest_site_distances": [],
            "tigo_sample_counts": [],
        }
    )

    for record in population_data:
        city = record["city"]
        stats = city_stats[city]

        stats["count"] += 1
        stats["total_population"] += record["population"]
        stats["total_households"] += record["households"]

        if record["tigo_coverage"]:
            stats["covered_grids"] += 1

        stats["coverage_pct_list"].append(1 if record["tigo_coverage"] else 0)
        stats["nearest_site_distances"].append(record["nearest_tigo_site_km"])
        stats["tigo_sample_counts"].append(record["ookla_tigo_samples"])

    print("\nPopulation distribution by city:")
    for city in sorted(city_stats.keys()):
        stats = city_stats[city]
        coverage_pct = (
            100 * sum(stats["coverage_pct_list"]) / len(stats["coverage_pct_list"])
        )
        avg_distance = sum(stats["nearest_site_distances"]) / len(
            stats["nearest_site_distances"]
        )
        total_samples = sum(stats["tigo_sample_counts"])

        print(f"  {city}: {stats['count']} grids")
        print(f"    Population: {stats['total_population']:,} ({stats['total_households']:,} households)")
        print(f"    Tigo coverage: {coverage_pct:.1f}% ({stats['covered_grids']}/{stats['count']} grids)")
        print(f"    Avg distance to nearest site: {avg_distance:.2f} km")
        print(f"    Total Tigo Ookla samples: {total_samples}")

    # Overall statistics
    total_population = sum(r["population"] for r in population_data)
    total_households = sum(r["households"] for r in population_data)
    covered_grids = sum(1 for r in population_data if r["tigo_coverage"])
    coverage_pct = 100 * covered_grids / len(population_data)
    uncovered_grids = len(population_data) - covered_grids
    uncovered_pct = 100 * uncovered_grids / len(population_data)

    print(f"\nOverall Statistics:")
    print(f"  Total grids: {len(population_data)}")
    print(f"  Total population: {total_population:,}")
    print(f"  Total households: {total_households:,}")
    print(f"  Tigo coverage: {covered_grids} grids ({coverage_pct:.1f}%)")
    print(f"  Uncovered: {uncovered_grids} grids ({uncovered_pct:.1f}%)")

    # Verify uncovered grids have no tigo samples but may have claro
    uncovered_with_claro = sum(
        1 for r in population_data if not r["tigo_coverage"] and r["ookla_claro_samples"] > 0
    )
    print(f"  Uncovered grids with Claro samples: {uncovered_with_claro}")

    uncovered_with_tigo = sum(
        1 for r in population_data if not r["tigo_coverage"] and r["ookla_tigo_samples"] > 0
    )
    print(f"  Uncovered grids with Tigo samples: {uncovered_with_tigo} (should be 0)")

    # Save to file
    output_path = Path(__file__).parent.parent / "population.json"
    with open(output_path, "w") as f:
        json.dump(population_data, f, indent=2)

    print(f"\nData saved to {output_path}")


if __name__ == "__main__":
    main()
