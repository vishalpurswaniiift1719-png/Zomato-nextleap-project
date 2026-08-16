"""
Data Cleaner Module
===================
Preprocesses and normalizes the raw Zomato dataset.

Responsibilities:
    - Handle missing / malformed values
    - Normalize text fields (consistent casing)
    - Parse ratings to float (handle 'NEW', '-', etc.)
    - Map cost to budget tiers (low / medium / high)

Usage:
    from src.data_loader import load_dataset
    from src.data_cleaner import clean_dataset

    raw_df = load_dataset()
    clean_df = clean_dataset(raw_df)
"""

import pandas as pd
import numpy as np


# ─── Budget Tier Boundaries (₹ for two) ──────────────────────────────────────
BUDGET_TIERS = {
    "low": (0, 500),
    "medium": (501, 1500),
    "high": (1501, float("inf")),
}


def _normalize_text_column(series: pd.Series) -> pd.Series:
    """Strip whitespace and convert to title case."""
    return series.astype(str).str.strip().str.title()


def _parse_rating(value) -> float:
    """
    Convert a rating value to float.
    Handles edge cases: 'NEW', '-', 'nan', empty strings → 0.0
    """
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    
    value_str = str(value).strip()
    if value_str in ("", "-", "NEW", "nan", "None"):
        return 0.0
    
    try:
        return float(value_str.split("/")[0])  # Handle "4.1/5" format
    except (ValueError, IndexError):
        return 0.0


def _map_cost_to_budget(cost: float) -> str:
    """
    Map average cost for two to a budget tier.
    
    Args:
        cost: Average cost for two in ₹.
    
    Returns:
        One of 'low', 'medium', 'high'.
    """
    if pd.isna(cost) or cost <= 0:
        return "medium"  # Default for unknown

    for tier, (low, high) in BUDGET_TIERS.items():
        if low <= cost <= high:
            return tier
    return "high"


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize the raw Zomato dataset.
    
    Steps:
        1. Standardize column names (lowercase, underscores)
        2. Handle missing values in critical columns
        3. Normalize text fields (city, cuisine names)
        4. Parse ratings to float
        5. Add budget_tier column

    Args:
        df: Raw DataFrame from data_loader.
    
    Returns:
        pd.DataFrame: Cleaned, normalized DataFrame with budget_tier column.
    """
    df = df.copy()

    # ── Step 1: Standardize column names ──────────────────────────────────
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    print(f"📋 Columns after normalization: {list(df.columns)}")

    # ── Step 2: Identify key columns ──────────────────────────────────────
    # The dataset may use various column names; we try common variants
    col_mapping = _detect_columns(df)
    print(f"🔍 Detected column mapping: {col_mapping}")

    # Rename to our standard names
    df = df.rename(columns=col_mapping)

    # ── Step 3: Handle missing values ─────────────────────────────────────
    if "name" in df.columns:
        df = df.dropna(subset=["name"])
        df["name"] = df["name"].astype(str).str.strip()

    if "city" in df.columns:
        df["city"] = _normalize_text_column(df["city"])
        df = df[df["city"] != "Nan"]

    if "cuisines" in df.columns:
        df["cuisines"] = df["cuisines"].fillna("Unknown").astype(str).str.strip()

    # ── Step 4: Parse ratings ─────────────────────────────────────────────
    if "rating" in df.columns:
        df["rating"] = df["rating"].apply(_parse_rating)
        # Clamp to [0, 5]
        df["rating"] = df["rating"].clip(0.0, 5.0)

    # ── Step 5: Parse cost and add budget tier ────────────────────────────
    if "avg_cost_for_two" in df.columns:
        df["avg_cost_for_two"] = pd.to_numeric(df["avg_cost_for_two"], errors="coerce").fillna(0)
        df["budget_tier"] = df["avg_cost_for_two"].apply(_map_cost_to_budget)
    else:
        df["avg_cost_for_two"] = 0
        df["budget_tier"] = "medium"

    # ── Step 6: Parse votes ───────────────────────────────────────────────
    if "votes" in df.columns:
        df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)

    # ── Step 7: Parse boolean fields ──────────────────────────────────────
    for col in ["online_delivery", "table_booking"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().isin(["yes", "true", "1"])

    # ── Step 8: Drop duplicates ───────────────────────────────────────────
    initial_count = len(df)
    df = df.drop_duplicates(subset=["name", "city"], keep="first")
    dropped = initial_count - len(df)
    if dropped > 0:
        print(f"🗑️ Dropped {dropped} duplicate restaurants")

    # ── Summary ───────────────────────────────────────────────────────────
    print(f"✅ Cleaned dataset: {len(df)} restaurants")
    print(f"   Cities: {df['city'].nunique() if 'city' in df.columns else 'N/A'}")
    print(f"   Rating range: {df['rating'].min():.1f} – {df['rating'].max():.1f}" if 'rating' in df.columns else "")
    print(f"   Budget tiers: {df['budget_tier'].value_counts().to_dict()}" if 'budget_tier' in df.columns else "")

    return df.reset_index(drop=True)


def _detect_columns(df: pd.DataFrame) -> dict:
    """
    Auto-detect column names from the dataset and map them to our standard names.
    Different dataset versions may use different column names.
    
    Returns:
        dict: Mapping from detected column names to our standard names.
    """
    mapping = {}
    columns_lower = {c.lower(): c for c in df.columns}

    # Define possible variants for each standard column name
    variants = {
        "name": ["name", "restaurant_name", "restaurant"],
        "city": ["city", "location", "locality", "area"],
        "cuisines": ["cuisines", "cuisine", "cuisine_type"],
        "rating": ["rating", "aggregate_rating", "avg_rating", "rate"],
        "avg_cost_for_two": ["avg_cost_for_two", "average_cost_for_two", "cost", "price", "approx_cost_for_two_people", "approx_cost"],
        "votes": ["votes", "num_votes", "vote_count", "reviews_list"],
        "online_delivery": ["online_delivery", "has_online_delivery", "online_order"],
        "table_booking": ["table_booking", "has_table_booking", "book_table"],
    }

    for standard_name, possible_names in variants.items():
        for variant in possible_names:
            if variant in columns_lower:
                actual_col = columns_lower[variant]
                if actual_col != standard_name:
                    mapping[actual_col] = standard_name
                break

    return mapping
