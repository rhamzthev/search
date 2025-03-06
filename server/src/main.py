from typing import Union, List, Dict, Any, Optional
import re
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .db.db import search_pages

app = FastAPI(root_path="/api")

origins = [
    "http://search.rhamzthev.com",
    "https://search.rhamzthev.com",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search", response_model=List[Dict[str, Any]])
def search(q: str = Query(..., min_length=1, description="Search query"), 
           limit: Optional[int] = Query(10, ge=1, le=100, description="Maximum number of results")):
    """
    Search for pages matching the query string.
    Results are ranked using TF-IDF scoring.
    """
    results = search_pages(q, limit)
    return results