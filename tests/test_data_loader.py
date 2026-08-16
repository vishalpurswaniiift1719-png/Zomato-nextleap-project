"""
Tests for Data Loader Module
"""

import pytest
from pathlib import Path


class TestLoadDataset:
    """Tests for the load_dataset() function."""

    def test_returns_dataframe(self):
        """load_dataset() should return a pandas DataFrame."""
        from src.data_loader import load_dataset
        df = load_dataset()
        assert hasattr(df, "columns"), "Should return a DataFrame-like object"
        assert len(df) > 0, "Dataset should not be empty"

    def test_caches_locally_after_first_load(self):
        """After first load, a local parquet cache should exist."""
        from src.data_loader import load_dataset, LOCAL_CACHE_PATH
        _ = load_dataset()
        assert LOCAL_CACHE_PATH.exists(), f"Cache file should exist at {LOCAL_CACHE_PATH}"

    def test_loads_from_cache_when_available(self):
        """Second call should load from cache (faster)."""
        from src.data_loader import load_dataset
        import time

        # Ensure cache exists
        _ = load_dataset()

        # Time the cached load
        start = time.perf_counter()
        df = load_dataset()
        elapsed = time.perf_counter() - start

        assert len(df) > 0
        assert elapsed < 2.0, f"Cached load should be fast, took {elapsed:.2f}s"

    def test_force_download_bypasses_cache(self):
        """force_download=True should re-download from HuggingFace."""
        from src.data_loader import load_dataset
        df = load_dataset(force_download=True)
        assert len(df) > 0
