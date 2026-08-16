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


class LLMClient:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini client using the GEMINI_API_KEY from .env.
        """
        load_dotenv()
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
            
        if genai is None:
            raise ImportError("The 'google-genai' package is not installed. Please run: pip install google-genai")
            
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

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

        try:
            # Configure generation for JSON output and deterministic behavior
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.4,
                response_mime_type="application/json"
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config,
            )
            
            # The model is forced to return JSON via response_mime_type
            return response.text
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"ERROR: {e}"
