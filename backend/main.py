from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from contextlib import asynccontextmanager

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
data_store = {}


def load_data_sync():
    """Load all data files into memory."""
    for name in [
        "sites",
        "ookla",
        "churn",
        "coverage",
        "terminals",
        "population",
        "experience_scores",
        "churn_attribution",
        "competitiveness",
        "potential_scores",
    ]:
        path = os.path.join(DATA_DIR, f"{name}.json")
        if os.path.exists(path):
            try:
                with open(path) as f:
                    data_store[name] = json.load(f)
                print(f"Loaded {name}: {len(data_store[name])} records")
            except Exception as e:
                print(f"Error loading {name}: {e}")


# Ensure data is loaded on import
if not data_store:
    load_data_sync()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    load_data_sync()
    yield
    # Shutdown
    pass


app = FastAPI(title="CMO Dashboard API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "data_loaded": list(data_store.keys())}


# Include API routes
from backend.api.routes import router

app.include_router(router)
