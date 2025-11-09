"""
Products endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from orchestrator.services.product_service import ProductService

logger = logging.getLogger(__name__)
router = APIRouter()
product_service = ProductService()


@router.get("/list")
async def get_products(
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get list of products with optional filtering
    """
    try:
        products = await product_service.get_products(
            category=category,
            limit=limit,
            offset=offset
        )
        return {
            "products": products,
            "total": len(products),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{sku}")
async def get_product_detail(sku: str):
    """
    Get detailed information about a specific product
    """
    try:
        product = await product_service.get_product_by_sku(sku)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product {sku}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_products(
    query: str = Query(..., min_length=2),
    limit: int = 20
):
    """
    Search products by query
    """
    try:
        results = await product_service.search_products(query=query, limit=limit)
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_categories():
    """
    Get all product categories
    """
    try:
        categories = await product_service.get_categories()
        return {
            "categories": categories
        }
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_product_stats():
    """
    Get product statistics
    """
    try:
        stats = await product_service.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching product stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
