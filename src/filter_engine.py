"""
Filter Engine Module
====================
Deterministic filtering engine that narrows down the restaurant dataset
based on user preferences before passing the candidates to the AI.

Usage:
    from src.filter_engine import UserQuery, filter_restaurants
    
    query = UserQuery(location="BTM", budget="low", cuisine="Chinese")
    candidates = filter_restaurants(df, query)
"""

import pandas as pd
from dataclasses import dataclass, field


@dataclass
class UserQuery:
    """
    Represents the structured preferences of a user query.
    Normalizes inputs automatically.
    """
    location: str
    budget: str = "medium"  # low | medium | high
    cuisine: str = ""       # Optional
    min_rating: float = 3.0 # 0.0 - 5.0
    additional_prefs: str = "" # Free text for the LLM

    def __post_init__(self):
        # Normalize location (title case, strip)
        if self.location:
            self.location = str(self.location).strip().title()
        
        # Normalize budget
        if self.budget:
            budget_lower = str(self.budget).strip().lower()
            if budget_lower in ["low", "medium", "high"]:
                self.budget = budget_lower
            else:
                self.budget = "medium"
        else:
            self.budget = "medium"
            
        # Normalize cuisine
        if self.cuisine:
            self.cuisine = str(self.cuisine).strip().lower()
            
        # Clamp rating
        try:
            self.min_rating = float(self.min_rating)
            self.min_rating = max(0.0, min(5.0, self.min_rating))
        except (ValueError, TypeError):
            self.min_rating = 3.0


def filter_restaurants(df: pd.DataFrame, query: UserQuery, top_n: int = 10) -> pd.DataFrame:
    """
    Filter the restaurant dataset based on user preferences.
    
    Args:
        df: Cleaned Pandas DataFrame containing restaurant data.
        query: UserQuery object with normalized preferences.
        top_n: Maximum number of candidates to return.
        
    Returns:
        pd.DataFrame: Top matching candidates, sorted by rating and votes.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    filtered = df.copy()

    # 1. Location Filter (Exact Match)
    if query.location and "city" in filtered.columns:
        filtered = filtered[filtered["city"] == query.location]
        
    if filtered.empty:
        return filtered

    # 2. Budget Filter (Exact Match on mapped tier)
    if query.budget and "budget_tier" in filtered.columns:
        filtered = filtered[filtered["budget_tier"] == query.budget]

    if filtered.empty:
        return filtered

    # 3. Cuisine Filter (Substring Match/Fuzzy)
    if query.cuisine and "cuisines" in filtered.columns:
        # Convert cuisines column to lower case for comparison
        cuisines_lower = filtered["cuisines"].str.lower()
        # Find rows where the queried cuisine is a substring
        filtered = filtered[cuisines_lower.str.contains(query.cuisine, na=False, regex=False)]
        
    if filtered.empty:
        return filtered

    # 4. Minimum Rating Filter
    if query.min_rating > 0 and "rating" in filtered.columns:
        filtered = filtered[filtered["rating"] >= query.min_rating]

    if filtered.empty:
        return filtered

    # 5. Sort by Rating (desc) and Votes (desc)
    sort_cols = []
    ascendings = []
    
    if "rating" in filtered.columns:
        sort_cols.append("rating")
        ascendings.append(False)
    
    if "votes" in filtered.columns:
        sort_cols.append("votes")
        ascendings.append(False)
        
    if sort_cols:
        filtered = filtered.sort_values(by=sort_cols, ascending=ascendings)

    # 6. Return Top N
    return filtered.head(top_n).reset_index(drop=True)
