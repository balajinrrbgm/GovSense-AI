"""
GovSense AI - Main FastAPI Application
AI-Powered Governance Platform for Maharashtra
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from api.routes import predictions, requests, tracking, public
from api.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting GovSense AI API...")
    logger.info(f"📍 Region: {settings.REGION}")
    logger.info(f"🔧 Environment: {'Development' if settings.API_RELOAD else 'Production'}")
    logger.info(f"🎯 Mock Data Mode: {settings.USE_MOCK_DATA}")
    yield
    logger.info("👋 Shutting down GovSense AI API...")


# Initialize FastAPI app
app = FastAPI(
    title="GovSense AI API",
    description="AI-Powered Governance Platform - Transforming Citizen Service Delivery",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "service": "GovSense AI API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "region": settings.REGION,
        "features": {
            "predictive_dashboard": True,
            "service_prioritization": True,
            "transparency_portal": True
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "operational",
            "gemini": "operational" if settings.ENABLE_GEMINI else "disabled",
            "vertex_ai": "operational" if settings.ENABLE_VERTEX_AI else "disabled",
            "bigquery": "operational" if settings.ENABLE_BIGQUERY else "disabled"
        },
        "region": settings.REGION,
        "mock_data": settings.USE_MOCK_DATA
    }


# Include routers
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(requests.router, prefix="/api/requests", tags=["Service Requests"])
app.include_router(tracking.router, prefix="/api/tracking", tags=["Tracking"])
app.include_router(public.router, prefix="/api/public", tags=["Public Portal"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.API_RELOAD else "An error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info"
    )
