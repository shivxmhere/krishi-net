import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from app.config import settings
from app.database import engine, Base, get_db
from app.db.init_db import init_db
from app.models.disease import Disease  # Ensure models are loaded
from app.models.user import User        # Ensure models are loaded
from app.api.endpoints import detect, auth
from app.core.logging_config import setup_logging, LoggingMiddleware
from app.core.limiter import limiter
from app.services.ml_service import ml_service

# Initialize Logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables and seed data. Shutdown: cleanup."""
    logger.info("Starting Krishi-Net API...", extra={"version": settings.APP_VERSION})
    Base.metadata.create_all(bind=engine)
    init_db()
    yield
    logger.info("Shutting down Krishi-Net API...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered crop disease detection for J&K farmers.",
    lifespan=lifespan,
)

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(detect.router, prefix="/api", tags=["detection"])

@app.get("/health", tags=["system"])
async def health_check(response: Response):
    """
    Enhanced Health Check
    Verifies: Database connection, ML Model status
    """
    health_status = {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "unknown",
        "ml_model": ml_service.mode,
        "timestamp": time.time()
    }
    
    # Check Database
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Health check failed: Database unreachable: {e}")
        health_status["database"] = "disconnected"
        health_status["status"] = "error"
        
    # Check ML Model
    if ml_service.mode == "STUB (Fallback)":
        health_status["status"] = "degraded"
        
    # Caching header for health check (5 minutes as per requirements)
    response.headers["Cache-Control"] = "public, max-age=300"
    
    return health_status
