# app/api/health.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "financial-risk-intelligence-api"
    }
