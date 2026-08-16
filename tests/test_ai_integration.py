"""
Tests for AI Integration Module
(prompt_builder and output_formatter)
"""

import pytest
import pandas as pd
import json
from src.prompt_builder import build_user_prompt
from src.output_formatter import parse_and_verify


@pytest.fixture
def candidates_df():
    """Create a sample DataFrame of candidates."""
    return pd.DataFrame({
        "name": ["Restaurant A", "Restaurant B", "Restaurant C"],
        "cuisines": ["Chinese", "Italian", "Indian"],
        "rating": [4.5, 4.2, 3.8],
        "votes": [1000, 500, 200],
        "budget_tier": ["low", "medium", "medium"],
        "avg_cost_for_two": [300, 800, 600]
    })


class TestPromptBuilder:
    def test_build_user_prompt_includes_preferences(self, candidates_df):
        prompt = build_user_prompt("I want something spicy", candidates_df)
        assert "I want something spicy" in prompt

    def test_build_user_prompt_includes_candidates_json(self, candidates_df):
        prompt = build_user_prompt("Test", candidates_df)
        assert "Restaurant A" in prompt
        assert "Restaurant B" in prompt
        assert "Restaurant C" in prompt
        # Verify it's actually formatted as a JSON string internally
        assert '"name": "Restaurant A"' in prompt


class TestOutputFormatter:
    def test_parse_valid_json(self, candidates_df):
        valid_json = '''
        [
            {"name": "Restaurant A", "rank": 1, "reason": "Great Chinese food."},
            {"name": "Restaurant C", "rank": 2, "reason": "Good Indian food."}
        ]
        '''
        recs = parse_and_verify(valid_json, candidates_df)
        
        assert len(recs) == 2
        assert recs[0].name == "Restaurant A"
        assert recs[0].rank == 1
        assert recs[0].rating == 4.5  # Pulled from DF, not LLM
        assert recs[1].name == "Restaurant C"
        
    def test_parse_hallucinated_restaurant(self, candidates_df):
        invalid_json = '''
        [
            {"name": "Fake Restaurant", "rank": 1, "reason": "I invented this."}
        ]
        '''
        recs = parse_and_verify(invalid_json, candidates_df)
        
        # Should fallback to top 3 from dataset because valid_recommendations will be empty
        assert len(recs) == 3
        assert recs[0].name == "Restaurant A"
        assert recs[1].name == "Restaurant B"
        assert recs[2].name == "Restaurant C"

    def test_parse_malformed_json_fallback(self, candidates_df):
        malformed = "This is not JSON at all."
        recs = parse_and_verify(malformed, candidates_df)
        
        assert len(recs) == 3
        assert recs[0].name == "Restaurant A"

    def test_parse_strips_markdown_blocks(self, candidates_df):
        markdown_json = '''```json
        [
            {"name": "Restaurant B", "rank": 1, "reason": "It's Italian."}
        ]
        ```'''
        recs = parse_and_verify(markdown_json, candidates_df)
        
        assert len(recs) == 1
        assert recs[0].name == "Restaurant B"
