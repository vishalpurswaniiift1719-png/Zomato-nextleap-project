"""
Zomato AI-Powered Restaurant Recommendation System

Modules:
    - data_loader:      Load dataset from HuggingFace or local cache
    - data_cleaner:     Preprocess and normalize restaurant data
    - filter_engine:    Deterministic filtering by location, budget, cuisine, rating
    - prompt_builder:   Construct structured prompts for the LLM
    - llm_client:       Interface with OpenAI / Gemini APIs
    - output_formatter: Parse LLM responses and merge with verified data
    - app:              Streamlit UI entry point
"""
