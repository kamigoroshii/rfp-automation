"""
Analytics endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime, timedelta
import logging

from orchestrator.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)
router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/dashboard")
async def get_dashboard_data():
    """
    Get dashboard overview data
    """
    try:
        data = await analytics_service.get_dashboard_data()
        return data
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_trends(
    period: str = "month",
    metric: str = "rfps"
):
    """
    Get trend data for charts
    """
    try:
        trends = await analytics_service.get_trends(period=period, metric=metric)
        return {
            "period": period,
            "metric": metric,
            "data": trends
        }
    except Exception as e:
        logger.error(f"Error fetching trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_performance_metrics():
    """
    Get system performance metrics
    """
    try:
        metrics = await analytics_service.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error fetching performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/monthly")
async def get_monthly_report(
    year: int,
    month: int
):
    """
    Get monthly report
    """
    try:
        report = await analytics_service.get_monthly_report(year=year, month=month)
        return report
    except Exception as e:
        logger.error(f"Error generating monthly report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/win-rate")
async def get_win_rate(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Get win rate statistics
    """
    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        win_rate = await analytics_service.get_win_rate(
            start_date=start_date,
            end_date=end_date
        )
        return win_rate
    except Exception as e:
        logger.error(f"Error fetching win rate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
