"""
Prompt Builder Module
=====================
Constructs the system and user prompts for the Zomato AI recommender.
Takes a DataFrame of pre-filtered candidates and formats them into a JSON string
for the LLM to process.
"""

import pandas as pd
import json
from typing import Optional


def build_system_prompt() -> str:
    """
    Returns the system prompt instructing the LLM on its role,
    constraints, and expected JSON output format.
    """
    return """You are an expert Zomato Restaurant Recommender.
Your task is to analyze a list of candidate restaurants and pick the best options (or as many as available) based on the user's specific preferences.

CRITICAL RULES:
1. You MUST ONLY recommend restaurants that are present in the provided candidate list.
2. DO NOT invent or hallucinate restaurants, ratings, or cuisines.
3. You must output your response STRICTLY as a valid JSON array of objects.

JSON OUTPUT FORMAT:
[
  {
    "name": "Exact Restaurant Name from candidates list",
    "rank": 1,
    "reason": "A highly concise, 1 sentence maximum explanation of why this matches the user preferences."
  },
  ...
]
"""

def build_user_prompt(preferences: str, candidates_df: pd.DataFrame) -> str:
    """
    Constructs the user prompt containing the natural language preferences
    and the structured JSON list of candidate restaurants.
    
    Args:
        preferences: Free-text preferences from the user (e.g. "I want a romantic place").
        candidates_df: The filtered DataFrame (top N results from filter_engine).
        
    Returns:
        str: The complete user prompt.
    """
    if candidates_df.empty:
        return "I have no candidate restaurants to choose from."

    # Convert candidates to a simplified JSON string for the LLM
    # We only send what the LLM needs to make a decision
    simplified_candidates = []
    
    for _, row in candidates_df.iterrows():
        candidate = {
            "name": row.get("name", "Unknown"),
            "cuisines": row.get("cuisines", "Unknown"),
            "rating": row.get("rating", 0.0),
            "votes": row.get("votes", 0),
            "budget_tier": row.get("budget_tier", "medium"),
            "cost_for_two": row.get("avg_cost_for_two", 0)
        }
        simplified_candidates.append(candidate)
        
    candidates_json = json.dumps(simplified_candidates, indent=2)
    
    user_prompt = f"""USER PREFERENCES:
{preferences if preferences else "Find the best highly-rated options."}

CANDIDATE RESTAURANTS (Choose up to {len(candidates_df)} from this list, ordered by relevance):
{candidates_json}

Return ONLY the JSON array. Do not include markdown code blocks or any other text.
"""
    return user_prompt
