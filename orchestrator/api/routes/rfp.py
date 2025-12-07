"""
RFP endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import uuid
import logging

from shared.models import RFPSummary, RFPResponse
from shared.database.connection import get_db_connection
from orchestrator.services.rfp_service import RFPService

logger = logging.getLogger(__name__)
router = APIRouter()
rfp_service = RFPService()


@router.get("/list")
async def get_rfps(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get list of RFPs with optional filtering
    """
    try:
        rfps = await rfp_service.get_rfps(status=status, limit=limit, offset=offset)
        return {
            "rfps": rfps,
            "total": len(rfps),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error fetching RFPs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{rfp_id}")
async def get_rfp_detail(rfp_id: str):
    """
    Get detailed information about a specific RFP
    """
    try:
        rfp = await rfp_service.get_rfp_by_id(rfp_id)
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        return rfp
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching RFP {rfp_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit")
async def submit_rfp(
    title: str = Form(...),
    source: str = Form(...),
    deadline: str = Form(...),
    scope: str = Form(...),
    testing_requirements: str = Form(""),
    file: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None
):
    """
    Submit a new RFP for processing
    """
    try:
        # Parse testing requirements
        test_reqs = [req.strip() for req in testing_requirements.split(",") if req.strip()]
        
        # Create RFP summary
        rfp_id = str(uuid.uuid4())
        rfp_summary = RFPSummary(
            rfp_id=rfp_id,
            title=title,
            source=source,
            deadline=datetime.fromisoformat(deadline.replace('Z', '+00:00')),
            scope=scope,
            testing_requirements=test_reqs,
            discovered_at=datetime.now(),
            status="new"
        )
        
        # Save to database
        await rfp_service.create_rfp(rfp_summary)
        
        # If file uploaded, save it
        if file:
            await rfp_service.save_rfp_file(rfp_id, file)
        
        # Trigger processing (async)
        # Trigger processing (async background task)
        # Note: In Sync/Test mode this might block if Sync logic is heavy, 
        # but BackgroundTasks schedules it after response.
        if background_tasks:
            background_tasks.add_task(rfp_service.process_rfp, rfp_id)
        else:
            # Fallback if dependency injection fails (should not happen in FastAPI)
            await rfp_service.process_rfp(rfp_id)
        
        return {
            "success": True,
            "rfp_id": rfp_id,
            "message": "RFP submitted successfully"
        }
    except Exception as e:
        logger.error(f"Error submitting RFP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{rfp_id}/status")
async def update_rfp_status(
    rfp_id: str,
    status: str
):
    """
    Update RFP status
    """
    try:
        await rfp_service.update_status(rfp_id, status)
        return {
            "success": True,
            "rfp_id": rfp_id,
            "status": status
        }
    except Exception as e:
        logger.error(f"Error updating RFP status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{rfp_id}/feedback")
async def submit_feedback(
    rfp_id: str,
    outcome: str,
    actual_price: Optional[float] = None,
    match_accuracy: Optional[float] = None,
    notes: Optional[str] = None
):
    """
    Submit feedback for an RFP
    """
    try:
        await rfp_service.submit_feedback(
            rfp_id=rfp_id,
            outcome=outcome,
            actual_price=actual_price,
            match_accuracy=match_accuracy,
            notes=notes
        )
        return {
            "success": True,
            "message": "Feedback submitted successfully"
        }
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{rfp_id}")
async def delete_rfp(rfp_id: str):
    """
    Delete an RFP
    """
    try:
        await rfp_service.delete_rfp(rfp_id)
        return {
            "success": True,
            "message": "RFP deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting RFP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
