"""
FastAPI Main Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.routes import router as api_v1_router
from backend.app.api.v1.profile_routes import router as profile_router
from backend.app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Astrology-Interpreter API",
    description="High-Precision Deterministic Calculation Engine & Anti-Sycophancy Astrological Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable Universal CORS for React Native (Web, iOS, Android)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health_check():
    """
    Health check endpoint returning system status.
    """
    return {
        "status": "healthy",
        "engine": "Astrology-Interpreter Engine v2.0.0",
        "precision_mode": "sub-arcsecond",
        "timezone_resolution": "offline-spatial"
    }
