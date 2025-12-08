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


@router.get("/reports", response_model=Dict[str, Any])
async def get_audit_reports(limit: int = 50, offset: int = 0):
    """
    Get list of audit reports
    """
    try:
        from shared.database.connection import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get reports
        cursor.execute("""
            SELECT 
                a.audit_id, a.rfp_id, a.audit_timestamp,
                a.overall_recommendation, a.compliance_score,
                a.critical_issues_count, a.summary,
                a.rfp_validation, a.match_validation, a.pricing_validation,
                r.title
            FROM audit_reports a
            LEFT JOIN rfps r ON a.rfp_id = r.rfp_id
            ORDER BY a.audit_timestamp DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        rows = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM audit_reports")
        total = cursor.fetchone()[0]
        
        # Get stats
        cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE overall_recommendation = 'APPROVE') as approved,
                COUNT(*) FILTER (WHERE overall_recommendation = 'REVIEW') as review,
                COUNT(*) FILTER (WHERE overall_recommendation = 'REJECT') as rejected,
                AVG(compliance_score) as avg_compliance
            FROM audit_reports
        """)
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        # Format reports
        reports = []
        for row in rows:
            reports.append({
                "audit_id": row[0],
                "rfp_id": row[1],
                "audit_timestamp": row[2].isoformat() if row[2] else None,
                "overall_recommendation": row[3],
                "compliance_score": float(row[4]) if row[4] else 0,
                "critical_issues_count": row[5],
                "summary": row[6],
                "rfp_validation": row[7],
                "match_validation": row[8],
                "pricing_validation": row[9],
                "rfp_title": row[10]
            })
        
        return {
            "reports": reports,
            "total": total,
            "stats": {
                "approved": stats[0] or 0,
                "review": stats[1] or 0,
                "rejected": stats[2] or 0,
                "avg_compliance_score": float(stats[3]) if stats[3] else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching audit reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": auditor.name,
        "version": auditor.version
    }
