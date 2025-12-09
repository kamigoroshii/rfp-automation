from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import logging
from datetime import datetime
from orchestrator.services.rfp_service import RFPService
from shared.models import RFPSummary

logger = logging.getLogger(__name__)

router = APIRouter()
rfp_service = RFPService()

@router.get("/list")
async def get_rfps(status: Optional[str] = None):
    """Get list of RFPs"""
    rfps = await rfp_service.get_rfps(status)
    return {"rfps": rfps, "total": len(rfps)}

@router.get("/{rfp_id}")
async def get_rfp(rfp_id: str):
    """Get RFP details"""
    rfp = await rfp_service.get_rfp_by_id(rfp_id)
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    return rfp

class RFPCreate(BaseModel):
    title: str
    source: str
    deadline: datetime
    scope: str
    testing_requirements: List[str] = []
    # Pre-calculated results
    match_score: float = 0
    total_estimate: float = 0
    specifications: List[dict] = []
    matches: List[dict] = []
    pricing: List[dict] = []
    recommended_sku: Optional[str] = None

@router.post("/create-json")
async def create_rfp_json(rfp: RFPCreate):
    """Create RFP from JSON with pre-calculated results"""
    try:
        import uuid
        rfp_id = f"RFP-WEB-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        
        summary = RFPSummary(
            rfp_id=rfp_id,
            title=rfp.title,
            source=rfp.source,
            deadline=rfp.deadline,
            scope=rfp.scope,
            testing_requirements=rfp.testing_requirements,
            discovered_at=datetime.now(),
            status='completed'
        )
        
        # Create Basic RFP
        await rfp_service.create_rfp(summary)
        
        # Save Detailed Results matches structure aligns with what save_results expects
        clean_matches = []
        for m in rfp.matches:
            clean_matches.append({
                'sku': m.get('sku'),
                'name': m.get('name') or m.get('product_name'), 
                'match_score': m.get('match_score'),
                'matched_specs': m.get('matched_specs') or m.get('specification_alignment') or {}
            })

        result = {
            'matches': clean_matches,
            'pricing': rfp.pricing,
            'specifications': rfp.specifications,
            'recommendation': {'sku': rfp.recommended_sku}
        }
        
        await rfp_service.save_results(rfp_id, result)
        
        return {"id": rfp_id, "rfp_id": rfp_id, "status": "completed"}
        
    except Exception as e:
        logger.error(f"Error creating RFP JSON: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def submit_rfp(
    title: str = Form(...),
    source: str = Form("Manual Upload"),
    deadline: str = Form(...),
    scope: str = Form(...),
    testing_requirements: str = Form(""),
    file: UploadFile = File(None)
):
    """Submit new RFP"""
    try:
        import uuid
        rfp_id = f"RFP-MANUAL-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        
        # Parse testing reqs
        reqs_list = [r.strip() for r in testing_requirements.split(',')] if testing_requirements else []
        
        # Determine deadline
        try:
            deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        except:
            deadline_dt = datetime.now() # Fallback

        # Save file if present
        if file:
            await rfp_service.save_rfp_file(rfp_id, file)

        summary = RFPSummary(
            rfp_id=rfp_id,
            title=title,
            source=source,
            deadline=deadline_dt,
            scope=scope,
            testing_requirements=reqs_list,
            discovered_at=datetime.now(),
            status='processing'
        )
        
        await rfp_service.create_rfp(summary)
        
        # Trigger processing
        await rfp_service.process_rfp(rfp_id)
        
        return {"id": rfp_id, "status": "processing"}
        
    except Exception as e:
        logger.error(f"Error submitting RFP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{rfp_id}/feedback")
async def submit_feedback(rfp_id: str, feedback: dict):
    """Submit feedback"""
    await rfp_service.submit_feedback(
        rfp_id=rfp_id,
        outcome=feedback.get('outcome', 'pending'),
        actual_price=feedback.get('actual_price'),
        match_accuracy=feedback.get('match_accuracy'),
        notes=feedback.get('notes')
    )
    return {"status": "success"}

@router.delete("/{rfp_id}")
async def delete_rfp(rfp_id: str):
    """Delete RFP"""
    await rfp_service.delete_rfp(rfp_id)
    return {"status": "success"}
