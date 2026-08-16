"""
Data Loader Module
==================
Handles loading the Zomato restaurant dataset from HuggingFace Hub
and caching it locally as Parquet for fast subsequent reads.

Usage:
    from src.data_loader import load_dataset

    df = load_dataset()  # Returns a clean pandas DataFrame
"""

import os
from pathlib import Path

import pandas as pd

# ─── Constants ────────────────────────────────────────────────────────────────
HUGGINGFACE_DATASET = "ManikaSaini/zomato-restaurant-recommendation"
LOCAL_CACHE_PATH = Path(__file__).parent.parent / "data" / "zomato_restaurants.parquet"


def load_from_huggingface() -> pd.DataFrame:
    """
    Download the Zomato dataset from HuggingFace Hub and return as DataFrame.
    
    Returns:
        pd.DataFrame: Raw restaurant data from HuggingFace.
    
    Raises:
        ImportError: If the `datasets` library is not installed.
        ConnectionError: If HuggingFace Hub is unreachable.
    """
    from datasets import load_dataset as hf_load_dataset

    print(f"📥 Downloading dataset from HuggingFace: {HUGGINGFACE_DATASET}")
    dataset = hf_load_dataset(HUGGINGFACE_DATASET)

    # Most HF datasets have a "train" split
    split = "train" if "train" in dataset else list(dataset.keys())[0]
    df = dataset[split].to_pandas()

    print(f"✅ Loaded {len(df)} restaurants from HuggingFace")
    return df


def save_to_cache(df: pd.DataFrame, path: Path = LOCAL_CACHE_PATH) -> None:
    """
    Save DataFrame to local Parquet cache for fast subsequent reads.
    
    Args:
        df: The DataFrame to cache.
        path: File path for the Parquet file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"💾 Cached {len(df)} restaurants to {path}")


def load_from_cache(path: Path = LOCAL_CACHE_PATH) -> pd.DataFrame:
    """
    Load DataFrame from local Parquet cache.
    
    Args:
        path: File path for the cached Parquet file.
    
    Returns:
        pd.DataFrame: Cached restaurant data.
    
    Raises:
        FileNotFoundError: If the cache file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Cache not found at {path}. Run load_dataset() first.")

    df = pd.read_parquet(path)
    print(f"📂 Loaded {len(df)} restaurants from local cache")
    return df


def load_dataset(force_download: bool = False) -> pd.DataFrame:
    """
    Load the Zomato dataset. Uses local cache if available, otherwise
    downloads from HuggingFace and caches locally.
    
    Args:
        force_download: If True, skip cache and re-download from HuggingFace.
    
    Returns:
        pd.DataFrame: Restaurant dataset ready for cleaning.
    """
    if not force_download and LOCAL_CACHE_PATH.exists():
        return load_from_cache()

    try:
        df = load_from_huggingface()
        save_to_cache(df)
        return df
    except Exception as e:
        # Fallback: try local cache even if force_download was set
        if LOCAL_CACHE_PATH.exists():
            print(f"⚠️ HuggingFace download failed ({e}). Using local cache.")
            return load_from_cache()
        raise ConnectionError(
            f"Cannot load dataset. HuggingFace failed ({e}) and no local cache exists."
        ) from e
