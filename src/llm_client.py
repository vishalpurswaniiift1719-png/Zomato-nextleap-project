"""
LLM Client Module
=================
Handles the connection and communication with Google Gemini via the google-genai SDK.
"""

import os
import json
from dotenv import load_dotenv

# Import the new google-genai SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

from src.prompt_builder import build_system_prompt, build_user_prompt
import pandas as pd


import time
from functools import lru_cache

@lru_cache(maxsize=256)
def _generate_with_retry(api_key: str, model_names: tuple, system_prompt: str, user_prompt: str) -> str:
    """
    Global cached function that attempts to call the Gemini API using a cascade of models.
    If a model hits a rate limit or 503, it dynamically swaps to the next model in the tuple.
    """
    client = genai.Client(api_key=api_key)
    
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.4,
        response_mime_type="application/json"
    )

    for attempt, current_model in enumerate(model_names):
        try:
            response = client.models.generate_content(
                model=current_model,
                contents=user_prompt,
                config=config,
            )
            return response.text
        except Exception as e:
            error_str = str(e).lower()
            # If rate limited (429) or service unavailable (503), swap to next model
            if "429" in error_str or "503" in error_str or "quota" in error_str or "exhausted" in error_str:
                if attempt < len(model_names) - 1:
                    print(f"Model {current_model} overloaded or limited. Swapping to {model_names[attempt+1]}...")
                    time.sleep(1) # Small pause before model swap
                    continue
            
            print(f"Error calling Gemini API: {e}")
            return "[]"
            
    return "[]"


class LLMClient:
    def __init__(self, fallback_models: tuple = None):
        """
        Initialize the Gemini client using the GEMINI_API_KEY from .env.
        """
        load_dotenv()
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
            
        if genai is None:
            raise ImportError("The 'google-genai' package is not installed. Please run: pip install google-genai")
            
        # A robust cascade of fast models. Each has its own independent rate limit bucket!
        self.fallback_models = fallback_models or (
            "gemini-3.6-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash",
            "gemini-3.7-flash",
            "gemini-3.5-flash"
        )

    def generate_recommendations(self, preferences: str, candidates_df: pd.DataFrame) -> str:
        """
        Send the filtered candidates to Gemini and get JSON recommendations back.
        
        Args:
            preferences: Free-text user preferences.
            candidates_df: The top N filtered restaurants.
            
        Returns:
            str: The raw JSON string returned by the LLM.
        """
        if candidates_df.empty:
            return "[]"

        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(preferences, candidates_df)

        return _generate_with_retry(self.api_key, self.fallback_models, system_prompt, user_prompt)
