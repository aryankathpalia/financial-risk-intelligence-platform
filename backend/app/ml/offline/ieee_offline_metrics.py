import json
from pathlib import Path

OFFLINE_DIR = Path("app/ml/offline")
BASE_DIR = Path(__file__).resolve().parent
CACHE_PATH = BASE_DIR / "ieee_offline_metrics.json"



def load_cached_offline_metrics():
    """
    Used by API / UI.
    Static, label-backed (validation only).
    """
    if not CACHE_PATH.exists():
        return {
            "status": "missing",
            "message": "IEEE offline metrics not generated yet."
        }

    with open(CACHE_PATH, "r") as f:
        return json.load(f)
