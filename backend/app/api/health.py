# app/api/health.py

from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/")
@router.head("/")
def health_check(response: Response):
    # HEAD requests must return no body
    if response is not None:
        response.status_code = 200
    return {
        "status": "ok",
        "service": "financial-risk-intelligence-api"
    }
