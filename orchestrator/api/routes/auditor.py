"""
Auditor API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from agents.auditor.agent import AuditorAgent
from shared.models import RFPSummary, ProductMatch, PricingBreakdown

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Auditor Agent
auditor = AuditorAgent()


class AuditRequest(BaseModel):
    rfp_id: str
    rfp_data: Dict[str, Any]
    matches: Optional[List[Dict[str, Any]]] = None
    pricing: Optional[Dict[str, Any]] = None


class AuditResponse(BaseModel):
    rfp_id: str
    audit_timestamp: str
    overall_recommendation: str
    critical_issues_count: int
    summary: str
    rfp_validation: Dict[str, Any]
    match_validation: Optional[Dict[str, Any]] = None
    pricing_validation: Optional[Dict[str, Any]] = None


@router.post("/validate/rfp", response_model=Dict[str, Any])
async def validate_rfp(rfp_data: Dict[str, Any]):
    """
    Validate RFP for completeness and compliance
    """
    try:
        # Convert dict to RFPSummary
        rfp = RFPSummary(**rfp_data)
        
        # Validate
        validation_result = auditor.validate_rfp(rfp)
        
        return {
            "success": True,
            "validation": validation_result
        }
        
    except Exception as e:
        logger.error(f"Error validating RFP: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate/matches", response_model=Dict[str, Any])
async def validate_matches(
    rfp_data: Dict[str, Any],
    matches: List[Dict[str, Any]]
):
    """
    Validate product matches for quality
    """
    try:
        # Convert to models
        rfp = RFPSummary(**rfp_data)
        match_objects = [ProductMatch(**m) for m in matches]
        
        # Validate
        validation_result = auditor.validate_matches(rfp, match_objects)
        
        return {
            "success": True,
            "validation": validation_result
        }
        
    except Exception as e:
        logger.error(f"Error validating matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate/pricing", response_model=Dict[str, Any])
async def validate_pricing(
    rfp_data: Dict[str, Any],
    pricing_data: Dict[str, Any],
    historical_prices: Optional[List[float]] = None
):
    """
    Validate pricing for anomalies
    """
    try:
        # Convert to models
        rfp = RFPSummary(**rfp_data)
        pricing = PricingBreakdown(**pricing_data)
        
        # Validate
        validation_result = auditor.validate_pricing(rfp, pricing, historical_prices)
        
        return {
            "success": True,
            "validation": validation_result
        }
        
    except Exception as e:
        logger.error(f"Error validating pricing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/audit/complete", response_model=AuditResponse)
async def complete_audit(request: AuditRequest):
    """
    Generate complete audit report for RFP, matches, and pricing
    """
    try:
        # Convert to models
        rfp = RFPSummary(**request.rfp_data)
        
        matches = []
        if request.matches:
            matches = [ProductMatch(**m) for m in request.matches]
        
        pricing = None
        if request.pricing:
            pricing = PricingBreakdown(**request.pricing)
        
        # Generate audit report
        if not matches or not pricing:
            raise HTTPException(
                status_code=400,
                detail="Both matches and pricing are required for complete audit"
            )
        
        audit_report = auditor.generate_audit_report(rfp, matches, pricing)
        
        return AuditResponse(**audit_report)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating audit report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": auditor.name,
        "version": auditor.version
    }
