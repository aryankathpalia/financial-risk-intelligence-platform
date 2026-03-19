# app/api/models.py

from fastapi import APIRouter
from app.services.online_metrics import get_online_model_stats
from app.ml.offline.ieee_offline_metrics import load_cached_offline_metrics

router = APIRouter(tags=["Models"])


@router.get("/offline-metrics")
def offline_metrics():
    """
    Offline evaluation metrics (CACHED, IEEE).
    """
    return load_cached_offline_metrics()


@router.get("/online-stats")
def online_stats():
    """
    Online production monitoring (unlabeled).
    """
    return get_online_model_stats()
