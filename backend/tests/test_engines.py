import pytest
import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.experience_score import (
    calculate_experience_score,
    calculate_batch_experience_scores
)
from engines.churn_attribution import attribute_churn
from engines.competitiveness import calculate_competitiveness
from engines.potential_score import calculate_potential


class TestExperienceScore:
    """Test experience score calculation with various input combinations."""

    def test_excellent_score(self):
        """Test excellent network quality scores."""
        score = calculate_experience_score(
            dl_throughput_mbps=60,
            latency_ms=15,
            prb_pct=40,
            rrc_success_pct=99.8,
            call_drop_pct=0.1
        )
        assert score >= 4.5, f"Expected excellent score >= 4.5, got {score}"

    def test_good_score(self):
        """Test good network quality scores."""
        score = calculate_experience_score(
            dl_throughput_mbps=35,
            latency_ms=25,
            prb_pct=60,
            rrc_success_pct=99.2,
            call_drop_pct=0.4
        )
        assert 3.5 <= score <= 4.5, f"Expected good score 3.5-4.5, got {score}"

    def test_poor_score(self):
        """Test poor network quality scores."""
        score = calculate_experience_score(
            dl_throughput_mbps=8,
            latency_ms=80,
            prb_pct=88,
            rrc_success_pct=96,
            call_drop_pct=1.5
        )
        assert score <= 2.5, f"Expected poor score <= 2.5, got {score}"

    def test_score_range(self):
        """Test that scores are always in valid range (0-5)."""
        score = calculate_experience_score(
            dl_throughput_mbps=50,
            latency_ms=20,
            prb_pct=50,
            rrc_success_pct=99.5,
            call_drop_pct=0.2
        )
        assert 1.0 <= score <= 5.0, f"Expected score in range [1,5], got {score}"

    def test_minimum_values(self):
        """Test minimum network quality."""
        score = calculate_experience_score(
            dl_throughput_mbps=1,
            latency_ms=500,
            prb_pct=95,
            rrc_success_pct=90,
            call_drop_pct=5.0
        )
        assert score <= 2.0, f"Expected low score <= 2.0, got {score}"

    def test_batch_calculation(self):
        """Test batch experience score calculation."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "radio_kpi.json").exists():
            pytest.skip("radio_kpi.json not found")
        if not (data_dir / "network_kpi.json").exists():
            pytest.skip("network_kpi.json not found")

        radio_path = str(data_dir / "radio_kpi.json")
        network_path = str(data_dir / "network_kpi.json")
        output_path = str(data_dir / "test_experience_scores.json")

        try:
            scores = calculate_batch_experience_scores(radio_path, network_path, output_path)
            assert len(scores) > 0, "No experience scores generated"
            assert all("experience_score" in s for s in scores), "Missing experience_score in results"
            assert all(1.0 <= s["experience_score"] <= 5.0 for s in scores), "Scores out of range"
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


class TestChurnAttribution:
    """Test churn attribution engine."""

    def test_churn_attribution_runs(self):
        """Test that churn attribution generates results."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "churn.json").exists():
            pytest.skip("churn.json not found")
        if not (data_dir / "coverage.json").exists():
            pytest.skip("coverage.json not found")

        churn_path = str(data_dir / "churn.json")
        coverage_path = str(data_dir / "coverage.json")
        output_path = str(data_dir / "test_churn_attribution.json")

        try:
            results = attribute_churn(churn_path, coverage_path, output_path=output_path)

            assert len(results) > 0, "No churn attribution results"

            # Verify structure
            for result in results:
                assert "city" in result, "Missing city in result"
                assert "total_churned" in result, "Missing total_churned in result"
                assert "network_factor_pct" in result, "Missing network_factor_pct in result"
                assert "recoverable_users" in result, "Missing recoverable_users in result"

                # Verify data integrity
                assert result["total_churned"] > 0, "Expected positive churn count"
                assert 0 <= result["network_factor_pct"] <= 100, f"Invalid network_factor_pct: {result['network_factor_pct']}"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_churn_attribution_sorted(self):
        """Test that churn attribution results are properly sorted."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "churn.json").exists():
            pytest.skip("churn.json not found")
        if not (data_dir / "coverage.json").exists():
            pytest.skip("coverage.json not found")

        churn_path = str(data_dir / "churn.json")
        coverage_path = str(data_dir / "coverage.json")
        output_path = str(data_dir / "test_churn_attribution_sorted.json")

        try:
            results = attribute_churn(churn_path, coverage_path, output_path=output_path)

            if len(results) > 1:
                # Verify sorted by total_churned descending
                for i in range(len(results) - 1):
                    assert results[i]["total_churned"] >= results[i+1]["total_churned"], \
                        "Results not sorted by total_churned"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


class TestCompetitiveness:
    """Test competitiveness calculation engine."""

    def test_competitiveness_runs(self):
        """Test that competitiveness analysis generates results."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "ookla.json").exists():
            pytest.skip("ookla.json not found")

        ookla_path = str(data_dir / "ookla.json")
        output_path = str(data_dir / "test_competitiveness.json")

        try:
            results = calculate_competitiveness(ookla_path, output_path)

            assert len(results) > 0, "No competitiveness results"

            # Verify structure
            for result in results:
                assert "city" in result, "Missing city"
                assert "competitiveness_ratio" in result, "Missing competitiveness_ratio"
                assert "tigo_dl_mbps" in result, "Missing tigo_dl_mbps"

                # Verify ratio is valid
                assert 0 <= result["competitiveness_ratio"] <= 2.0, \
                    f"Invalid competitiveness ratio: {result['competitiveness_ratio']}"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_competitiveness_operators(self):
        """Test that competitiveness includes operator metrics."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "ookla.json").exists():
            pytest.skip("ookla.json not found")

        ookla_path = str(data_dir / "ookla.json")
        output_path = str(data_dir / "test_competitiveness_ops.json")

        try:
            results = calculate_competitiveness(ookla_path, output_path)

            for result in results:
                # Check for operator speed metrics
                assert "tigo_dl_mbps" in result
                assert "tigo_ul_mbps" in result
                assert "tigo_latency_ms" in result
                assert result["tigo_dl_mbps"] >= 0, "Invalid Tigo download speed"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


class TestPotentialScore:
    """Test potential score calculation engine."""

    def test_potential_score_runs(self):
        """Test that potential score calculation generates results."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "population.json").exists():
            pytest.skip("population.json not found")

        population_path = str(data_dir / "population.json")
        output_path = str(data_dir / "test_potential_scores.json")

        try:
            results = calculate_potential(population_path, output_path)

            assert len(results) > 0, "No potential scores generated"

            # Verify structure
            for result in results:
                assert "grid_id" in result, "Missing grid_id"
                assert "potential_score" in result, "Missing potential_score"
                assert "population" in result, "Missing population"

                # Verify score range
                assert 0 <= result["potential_score"] <= 1.0, \
                    f"Invalid potential score: {result['potential_score']}"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_potential_score_components(self):
        """Test that potential score includes component scores."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "population.json").exists():
            pytest.skip("population.json not found")

        population_path = str(data_dir / "population.json")
        output_path = str(data_dir / "test_potential_components.json")

        try:
            results = calculate_potential(population_path, output_path)

            for result in results:
                assert "population_score" in result
                assert "coverage_gap_score" in result
                assert "competitor_score" in result
                assert "income_score" in result

                # Verify component scores are in valid range
                assert 0 <= result["population_score"] <= 1.0
                assert 0 <= result["coverage_gap_score"] <= 1.0
                assert 0 <= result["competitor_score"] <= 1.0
                assert 0 <= result["income_score"] <= 1.0

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_potential_score_sorted(self):
        """Test that potential scores are sorted descending."""
        data_dir = Path(__file__).parent.parent.parent / "data"

        if not (data_dir / "population.json").exists():
            pytest.skip("population.json not found")

        population_path = str(data_dir / "population.json")
        output_path = str(data_dir / "test_potential_sorted.json")

        try:
            results = calculate_potential(population_path, output_path)

            if len(results) > 1:
                # Verify sorted by score descending
                for i in range(len(results) - 1):
                    assert results[i]["potential_score"] >= results[i+1]["potential_score"], \
                        "Results not sorted by potential_score"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
