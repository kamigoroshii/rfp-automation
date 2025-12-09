"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

from orchestrator.config import settings
from orchestrator.api.routes import rfp, analytics, products, copilot, auditor, emails, notifications, pdf_generator

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
app.include_router(emails.router, prefix="/api/emails", tags=["Emails"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(pdf_generator.router, prefix="/api/rfp", tags=["pdf"])

# Serve uploaded files (PDFs, documents)
uploads_dir = os.path.join(os.getcwd(), "data", "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Background Task for Email Monitoring
import asyncio
from agents.sales.agent import SalesAgent

async def check_emails_periodically():
    """Background task to check emails every hour"""
    agent = SalesAgent()
    # Import services here to avoid circular dependencies if any
    from orchestrator.services.rfp_service import RFPService
    from orchestrator.services.notification_service import NotificationService
    
    rfp_service = RFPService()
    notification_service = NotificationService()
    
    while True:
        try:
            logger.info("Starting hourly email check...")
            logger.info("Starting hourly email check...")
            # Run blocking code in thread pool
            loop = asyncio.get_event_loop()
            rfps = await loop.run_in_executor(None, agent.check_emails_imap)
            
            if rfps:
                logger.info(f"Found {len(rfps)} new RFPs from email.")
                for rfp in rfps:
                    # Save RFP to DB
                    # Save RFP to DB
                    await rfp_service.create_rfp(rfp)
                    
                    # Update Email Status (Link RFP ID)
                    if getattr(rfp, 'source_email_id', None):
                         await loop.run_in_executor(
                             None, 
                             agent._update_email_status, 
                             rfp.source_email_id, 
                             'processed', 
                             rfp.rfp_id
                         )
                    
                    # Check for High Value Alert (> $1M)
                    # We need to simulate value estimation if not present, 
                    # but check_emails_imap sets project_value if found
                    await notification_service.notify_high_value_rfp({
                        'rfp_id': rfp.rfp_id,
                        'title': rfp.title,
                        'source': rfp.source,
                        'total_estimate': rfp.project_value, # from RFPSummary
                        'deadline': rfp.deadline
                    })
                    
                    # Trigger Processing
                    await rfp_service.process_rfp(rfp.rfp_id)
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
