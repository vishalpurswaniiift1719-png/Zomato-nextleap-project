"""
Tests for Filter Engine Module
"""

import pytest
import pandas as pd
from src.filter_engine import UserQuery, filter_restaurants


@pytest.fixture
def sample_df():
    """Create a sample cleaned DataFrame for testing filters."""
    return pd.DataFrame({
        "name": ["Restaurant A", "Restaurant B", "Restaurant C", "Restaurant D", "Restaurant E"],
        "city": ["Btm", "Btm", "Indiranagar", "Btm", "Whitefield"],
        "budget_tier": ["low", "medium", "medium", "low", "high"],
        "cuisines": ["Chinese, North Indian", "South Indian", "Chinese", "Fast Food", "Chinese"],
        "rating": [4.5, 3.5, 4.0, 2.5, 4.8],
        "votes": [1000, 500, 800, 100, 2000]
    })


class TestUserQuery:
    def test_normalizes_location(self):
        q = UserQuery(location=" btm ")
        assert q.location == "Btm"

    def test_normalizes_budget(self):
        q = UserQuery(location="Btm", budget=" LOW ")
        assert q.budget == "low"
        
        q2 = UserQuery(location="Btm", budget="invalid_budget")
        assert q2.budget == "medium"

    def test_normalizes_cuisine(self):
        q = UserQuery(location="Btm", cuisine=" CHINESE ")
        assert q.cuisine == "chinese"

    def test_clamps_rating(self):
        q1 = UserQuery(location="Btm", min_rating=6.0)
        assert q1.min_rating == 5.0
        
        q2 = UserQuery(location="Btm", min_rating=-1.0)
        assert q2.min_rating == 0.0
        
        q3 = UserQuery(location="Btm", min_rating="not a float")
        assert q3.min_rating == 3.0


class TestFilterRestaurants:
    def test_filter_exact_match_happy_path(self, sample_df):
        # Btm + low budget + chinese + rating > 4.0 => Restaurant A
        query = UserQuery(location="Btm", budget="low", cuisine="Chinese", min_rating=4.0)
        result = filter_restaurants(sample_df, query)
        
        assert len(result) == 1
        assert result.iloc[0]["name"] == "Restaurant A"

    def test_filter_no_results_wrong_location(self, sample_df):
        query = UserQuery(location="Unknown City")
        result = filter_restaurants(sample_df, query)
        assert len(result) == 0

    def test_filter_cuisine_substring_match(self, sample_df):
        # Indiranagar + medium + chinese => Restaurant C
        query = UserQuery(location="Indiranagar", cuisine="chinese", budget="medium", min_rating=3.0)
        result = filter_restaurants(sample_df, query)
        
        assert len(result) == 1
        assert result.iloc[0]["name"] == "Restaurant C"

    def test_filter_rating_threshold(self, sample_df):
        # Btm + low budget => A (4.5) and D (2.5)
        # min rating 3.0 => Should only return A
        query = UserQuery(location="Btm", budget="low", min_rating=3.0)
        result = filter_restaurants(sample_df, query)
        
        assert len(result) == 1
        assert result.iloc[0]["name"] == "Restaurant A"

    def test_sorting_by_rating_and_votes(self, sample_df):
        # Add another Btm, low budget, chinese restaurant to test sorting
        new_row = pd.DataFrame([{
            "name": "Restaurant A2",
            "city": "Btm",
            "budget_tier": "low",
            "cuisines": "Chinese",
            "rating": 4.5,
            "votes": 1500  # More votes than Restaurant A
        }])
        df = pd.concat([sample_df, new_row], ignore_index=True)
        
        query = UserQuery(location="Btm", budget="low", cuisine="chinese", min_rating=4.0)
        result = filter_restaurants(df, query)
        
        assert len(result) == 2
        # A2 should be first because same rating (4.5) but more votes (1500 vs 1000)
        assert result.iloc[0]["name"] == "Restaurant A2"
        assert result.iloc[1]["name"] == "Restaurant A"

    def test_top_n_limit(self, sample_df):
        # Btm returns 3 restaurants, if top_n=2, it should return 2
        query = UserQuery(location="Btm", budget="medium", min_rating=0.0)
        # We need to relax budget to get all Btm restaurants for testing limit.
        # Actually in sample_df BTM has 1 med, 2 low. Let's just bypass budget for this test
        # by passing None or something? The dataclass defaults to 'medium'.
        # Let's add a test-specific dataframe
        df = pd.DataFrame({
            "name": [f"R{i}" for i in range(10)],
            "city": ["Btm"] * 10,
            "budget_tier": ["medium"] * 10,
            "cuisines": ["Chinese"] * 10,
            "rating": [4.0] * 10,
            "votes": [100] * 10
        })
        query = UserQuery(location="Btm", budget="medium")
        result = filter_restaurants(df, query, top_n=5)
        assert len(result) == 5
