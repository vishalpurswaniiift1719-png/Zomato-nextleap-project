"""
FastAPI Backend for Zomato Recommender
======================================
Serves the data and AI logic to the Next.js frontend.
"""

from fastapi import FastAPI, HTTPException
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
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load and clean dataset once at startup
    print("Loading and cleaning dataset...")
    raw_df = load_dataset()
    df = clean_dataset(raw_df)
    
    # Store for use in routes
    app_state["df"] = df
    
    # Extract unique locations (remember: data_cleaner renamed 'location' to 'city')
    # Filter out empty or Nan strings
    cities = df["city"].dropna().unique().tolist()
    app_state["locations"] = sorted([c for c in cities if c.strip() and c.lower() != "nan"])
    
    print(f"Loaded {len(df)} restaurants and {len(app_state['locations'])} unique locations.")
    
    yield
    # Cleanup (if any)
    app_state.clear()


app = FastAPI(title="Zomato AI Concierge API", lifespan=lifespan)

# Allow Next.js frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    if "locations" not in app_state:
        raise HTTPException(status_code=503, detail="Dataset still loading")
    return {"locations": app_state["locations"]}


@app.post("/api/recommend")
async def get_recommendations(req: RecommendationRequest):
    """Filters the dataset and asks Gemini for personalized recommendations."""
    if "df" not in app_state:
        raise HTTPException(status_code=503, detail="Dataset still loading")
        
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
