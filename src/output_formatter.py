"""
Output Formatter Module
=======================
Parses the raw JSON string from the LLM, validates it against the candidate list,
and constructs the final safe Recommendation objects.
"""

import json
import pandas as pd
from dataclasses import dataclass
from typing import List


@dataclass
class Recommendation:
    rank: int
    name: str
    reason: str
    rating: float
    cost: float
    cuisines: str
    location: str


def parse_and_verify(llm_json_str: str, candidates_df: pd.DataFrame) -> List[Recommendation]:
    if candidates_df.empty:
        return []
        
    # If the LLM client passed an explicit error string instead of JSON
    if llm_json_str.startswith("ERROR:"):
        return _fallback_recommendations(candidates_df, llm_json_str)
        
    try:
        clean_str = llm_json_str.strip()
        if clean_str.startswith("```json"):
            clean_str = clean_str[7:]
        if clean_str.endswith("```"):
            clean_str = clean_str[:-3]
            
        llm_results = json.loads(clean_str)
    except json.JSONDecodeError:
        print("Failed to parse LLM JSON. Falling back to default list.")
        return _fallback_recommendations(candidates_df, f"Parse Error. Raw output: {llm_json_str[:100]}...")
        
    if not isinstance(llm_results, list):
        print("LLM did not return a list. Falling back to default list.")
        return _fallback_recommendations(candidates_df, "Format Error: LLM did not return a JSON array.")

    valid_recommendations = []
    
    for item in llm_results:
        # Check if expected fields exist
        if not isinstance(item, dict) or "name" not in item:
            continue
            
        rec_name = item["name"]
        
        # Verify the name actually exists in our candidates DataFrame
        matching_row = candidates_df[candidates_df["name"] == rec_name]
        
        if not matching_row.empty:
            row = matching_row.iloc[0]
            
            rec = Recommendation(
                rank=int(item.get("rank", len(valid_recommendations) + 1)),
                name=row["name"],
                reason=item.get("reason", "Highly recommended based on your preferences."),
                rating=row.get("rating", 0.0),
                cost=row.get("avg_cost_for_two", 0.0),
                cuisines=row.get("cuisines", ""),
                location=row.get("city", "")
            )
            valid_recommendations.append(rec)
                
    # If the LLM returned nothing valid, use fallback
    if not valid_recommendations:
        return _fallback_recommendations(candidates_df, "Verification Error: LLM returned valid JSON but no restaurant names matched the database exactly.")
        
    # Ensure they are sorted by rank
    valid_recommendations.sort(key=lambda x: x.rank)
    return valid_recommendations


def _fallback_recommendations(candidates_df: pd.DataFrame, error_msg: str = None) -> List[Recommendation]:
    fallback_recs = []
    
    for rank, (index, row) in enumerate(candidates_df.iterrows(), start=1):
        reason_text = error_msg if error_msg else "This is one of the highest-rated options matching your criteria."
        rec = Recommendation(
            rank=rank,
            name=row["name"],
            reason=reason_text,
            rating=row.get("rating", 0.0),
            cost=row.get("avg_cost_for_two", 0.0),
            cuisines=row.get("cuisines", ""),
            location=row.get("city", "")
        )
        fallback_recs.append(rec)
        
    return fallback_recs
