"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from orchestrator.config import settings
from orchestrator.api.routes import rfp, analytics, products

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RFP Automation System API",
    description="Enterprise-level multi-agent AI platform for automating RFP response processes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rfp.router, prefix="/api/rfp", tags=["RFP"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RFP Automation System API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "operational",
            "redis": "operational"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "orchestrator.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
