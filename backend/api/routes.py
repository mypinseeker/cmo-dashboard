from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api")


def get_data(name):
    """Helper function to retrieve data from the global data_store."""
    from backend.main import data_store
    return data_store.get(name, [])


@router.get("/overview")
async def overview():
    """Get high-level CMO dashboard overview."""
    sites = get_data("sites")
    churn_attr = get_data("churn_attribution")
    comp = get_data("competitiveness")
    coverage = get_data("coverage")

    total_users = sum(c.get("total_mr_samples", 0) for c in coverage) if coverage else 12500000
    avg_experience = 0
    exp = get_data("experience_scores")
    if exp:
        avg_experience = round(sum(e.get("experience_score", 0) for e in exp) / len(exp), 2)

    alert_cities = [c["city"] for c in churn_attr if c.get("network_factor_pct", 0) > 50]

    return {
        "total_sites": len(sites),
        "total_users_estimate": total_users,
        "avg_experience_score": avg_experience,
        "alert_cities": alert_cities,
        "alert_count": len(alert_cities),
    }


@router.get("/sites")
async def list_sites(city: Optional[str] = None):
    """List all sites, optionally filtered by city."""
    sites = get_data("sites")
    if city:
        sites = [s for s in sites if s.get("city") == city]
    return sites


@router.get("/ookla")
async def ookla_data(
    city: Optional[str] = None,
    operator: Optional[str] = None,
    period: Optional[str] = None,
):
    """Get Ookla speed test data with optional filters."""
    data = get_data("ookla")
    if city:
        data = [d for d in data if d.get("city") == city]
    if operator:
        data = [d for d in data if d.get("operator") == operator]
    if period:
        data = [d for d in data if d.get("period") == period]
    return {"count": len(data), "data": data[:500]}  # Limit response size


@router.get("/coverage")
async def coverage_data(city: Optional[str] = None):
    """Get coverage data by city."""
    data = get_data("coverage")
    if city:
        data = [d for d in data if d.get("city") == city]
    return data


@router.get("/terminals")
async def terminals_data(city: Optional[str] = None):
    """Get terminal/device data by city."""
    data = get_data("terminals")
    if city:
        data = [d for d in data if d.get("city") == city]
    return data


@router.get("/churn")
async def churn_data(city: Optional[str] = None):
    """Get churn data and attribution analysis."""
    raw = get_data("churn")
    attr = get_data("churn_attribution")
    if city:
        raw = [d for d in raw if d.get("primary_city") == city]
        attr = [d for d in attr if d.get("city") == city]
    return {"total_churned": len(raw), "attribution": attr, "sample": raw[:100]}


@router.get("/potential")
async def potential_data(city: Optional[str] = None):
    """Get potential growth scores by city."""
    data = get_data("potential_scores")
    if city:
        data = [d for d in data if d.get("city") == city]
    return data


@router.get("/competitiveness")
async def competitiveness_data(city: Optional[str] = None):
    """Get competitive landscape data by city."""
    data = get_data("competitiveness")
    if city:
        data = [d for d in data if d.get("city") == city]
    return data


@router.get("/experience")
async def experience_data(city: Optional[str] = None):
    """Get experience quality scores by city."""
    coverage = get_data("coverage")
    if city:
        coverage = [c for c in coverage if c.get("city") == city]
    return {"coverage_quality": coverage}


@router.get("/drilldown/{city}")
async def drilldown(city: str):
    """Get comprehensive drilldown data for a specific city."""
    sites = [s for s in get_data("sites") if s.get("city") == city]
    coverage = [c for c in get_data("coverage") if c.get("city") == city]
    terminals = [t for t in get_data("terminals") if t.get("city") == city]
    churn_attr = [c for c in get_data("churn_attribution") if c.get("city") == city]
    comp = [c for c in get_data("competitiveness") if c.get("city") == city]
    potential = [p for p in get_data("potential_scores") if p.get("city") == city]

    return {
        "city": city,
        "sites_count": len(sites),
        "coverage": coverage,
        "terminals": terminals,
        "churn_attribution": churn_attr,
        "competitiveness": comp,
        "potential_grids": len(potential),
    }
