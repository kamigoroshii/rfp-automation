"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from orchestrator.config import settings
from orchestrator.api.routes import rfp, analytics, products, copilot, auditor

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
# Include routers
app.include_router(rfp.router, prefix="/api/rfp", tags=["RFP"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(copilot.router, prefix="/api/copilot", tags=["Copilot"])
app.include_router(auditor.router, prefix="/api/auditor", tags=["Auditor"])

# Background Task for Email Monitoring
import asyncio
from agents.sales.agent import SalesAgent

async def check_emails_periodically():
    """Background task to check emails every hour"""
    agent = SalesAgent()
    while True:
        try:
            logger.info("Starting hourly email check...")
            rfps = agent.check_emails_imap()
            if rfps:
                logger.info(f"Found {len(rfps)} new RFPs from email.")
                # Here you might trigger further processing if needed
            else:
                logger.info("No new RFPs found in email.")
        except Exception as e:
            logger.error(f"Error in email monitoring task: {e}")
        
        # Wait for 1 hour (3600 seconds)
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    asyncio.create_task(check_emails_periodically())


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
