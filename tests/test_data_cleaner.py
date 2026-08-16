"""
Tests for Data Cleaner Module
"""

import pytest
import pandas as pd
import numpy as np
from src.data_cleaner import clean_dataset, _parse_rating, _map_cost_to_budget


class TestParseRating:
    """Tests for the _parse_rating helper."""

    def test_normal_float(self):
        assert _parse_rating(4.3) == 4.3

    def test_normal_int(self):
        assert _parse_rating(4) == 4.0

    def test_string_float(self):
        assert _parse_rating("4.3") == 4.3

    def test_new_string(self):
        assert _parse_rating("NEW") == 0.0

    def test_dash(self):
        assert _parse_rating("-") == 0.0

    def test_empty_string(self):
        assert _parse_rating("") == 0.0

    def test_none(self):
        assert _parse_rating(None) == 0.0

    def test_nan(self):
        assert _parse_rating(float("nan")) == 0.0

    def test_slash_format(self):
        assert _parse_rating("4.1/5") == 4.1


class TestMapCostToBudget:
    """Tests for the _map_cost_to_budget helper."""

    def test_low_budget(self):
        assert _map_cost_to_budget(300) == "low"

    def test_low_boundary(self):
        assert _map_cost_to_budget(500) == "low"

    def test_medium_budget(self):
        assert _map_cost_to_budget(800) == "medium"

    def test_medium_boundary(self):
        assert _map_cost_to_budget(1500) == "medium"

    def test_high_budget(self):
        assert _map_cost_to_budget(2000) == "high"

    def test_zero_cost(self):
        assert _map_cost_to_budget(0) == "medium"  # Default

    def test_nan_cost(self):
        assert _map_cost_to_budget(float("nan")) == "medium"  # Default


class TestCleanDataset:
    """Tests for the clean_dataset function."""

    @pytest.fixture
    def sample_raw_df(self):
        """Create a sample raw DataFrame mimicking HuggingFace data."""
        return pd.DataFrame({
            "Restaurant Name": ["  Barbeque Nation ", "Mainland China", "Cafe Coffee Day", None],
            "City": ["  delhi", "MUMBAI", "bangalore", "delhi"],
            "Cuisines": ["North Indian, Chinese", "Chinese", None, "Cafe"],
            "Aggregate Rating": [4.3, "NEW", 3.8, "-"],
            "Average Cost for two": [1200, 1800, 400, 0],
            "Votes": [1542, "200", None, 50],
            "Has Online Delivery": ["Yes", "No", "Yes", "No"],
        })

    def test_drops_null_names(self, sample_raw_df):
        result = clean_dataset(sample_raw_df)
        assert result["name"].isna().sum() == 0

    def test_normalizes_city_to_title_case(self, sample_raw_df):
        result = clean_dataset(sample_raw_df)
        cities = result["city"].tolist()
        assert "Delhi" in cities
        assert "Mumbai" in cities
        assert "Bangalore" in cities

    def test_parses_ratings_to_float(self, sample_raw_df):
        result = clean_dataset(sample_raw_df)
        assert result["rating"].dtype == float
        assert (result["rating"] >= 0).all()
        assert (result["rating"] <= 5).all()

    def test_adds_budget_tier_column(self, sample_raw_df):
        result = clean_dataset(sample_raw_df)
        assert "budget_tier" in result.columns
        assert set(result["budget_tier"].unique()).issubset({"low", "medium", "high"})

    def test_fills_missing_cuisines(self, sample_raw_df):
        result = clean_dataset(sample_raw_df)
        assert result["cuisines"].isna().sum() == 0
        assert "Unknown" in result["cuisines"].values

    def test_handles_string_votes(self, sample_raw_df):
        result = clean_dataset(sample_raw_df)
        assert result["votes"].dtype in [int, np.int64]
