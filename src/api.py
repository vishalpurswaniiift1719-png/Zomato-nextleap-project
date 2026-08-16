"""
FastAPI Backend for Zomato Recommender
======================================
Serves the data and AI logic to the Next.js frontend.
"""

import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager
import traceback

from src.data_loader import load_dataset
from src.data_cleaner import clean_dataset
from src.filter_engine import UserQuery, filter_restaurants
from src.llm_client import LLMClient
from src.output_formatter import parse_and_verify

# Global variables for caching state
app_state = {
    "is_ready": False,
    "error": None
}

def load_data_sync():
    """Synchronous function to load data"""
    try:
        print("Background: Loading and cleaning dataset...")
        raw_df = load_dataset()
        df = clean_dataset(raw_df)
        app_state["df"] = df
        
        cities = df["city"].dropna().unique().tolist()
        app_state["locations"] = sorted([c for c in cities if c.strip() and c.lower() != "nan"])
        app_state["is_ready"] = True
        print(f"Background: Loaded {len(df)} restaurants and {len(app_state['locations'])} unique locations.")
    except Exception as e:
        app_state["error"] = str(e)
        print(f"Background Error: {traceback.format_exc()}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Spawn the long-running dataset load in a background thread 
    # so uvicorn binds to the port instantly!
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, load_data_sync)
    yield

app = FastAPI(title="Zomato AI Concierge API", lifespan=lifespan)

# Allow Next.js frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    location: str
    budget: str
    cuisines: list[str] = []
    min_rating: float = 3.0
    preferences: str = ""

@app.get("/api/locations")
async def get_locations():
    """Returns the list of all unique neighborhoods/locations in the dataset."""
    if app_state.get("error"):
        raise HTTPException(status_code=500, detail=f"Dataset error: {app_state['error']}")
    if not app_state["is_ready"]:
        raise HTTPException(status_code=503, detail="Dataset is still downloading on the server. Please try again in 30 seconds.")
    return {"locations": app_state["locations"]}

@app.post("/api/recommend")
async def get_recommendations(req: RecommendationRequest):
    """Filters the dataset and asks Gemini for personalized recommendations."""
    if app_state.get("error"):
        raise HTTPException(status_code=500, detail=f"Dataset error: {app_state['error']}")
    if not app_state["is_ready"]:
        raise HTTPException(status_code=503, detail="Dataset is still downloading on the server. Please try again in 30 seconds.")
        
    df = app_state["df"]
    
    # Join cuisines list into a comma-separated string for our filter_engine
    cuisine_str = ", ".join(req.cuisines)
    
    # 1. Prepare query
    query = UserQuery(
        location=req.location,
        budget=req.budget,
        cuisine=cuisine_str,
        min_rating=req.min_rating,
        additional_prefs=req.preferences
    )
    
    # 2. Filter dataset
    candidates_df = filter_restaurants(df, query, top_n=5)
    
    if candidates_df.empty:
        return {"recommendations": []}
        
    # 3. Ask LLM
    try:
        client = LLMClient()
        raw_json = client.generate_recommendations(query.additional_prefs, candidates_df)
        
        # 4. Parse & Guardrail
        recommendations = parse_and_verify(raw_json, candidates_df)
        
        # Convert dataclasses to dicts for JSON response
        return {"recommendations": [rec.__dict__ for rec in recommendations]}
        
    except Exception as e:
        print(f"Error during recommendation: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
