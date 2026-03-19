import json
from pathlib import Path

# Directory where THIS file lives:
# /app/app/ml/offline
BASE_DIR = Path(__file__).resolve().parent

# Exact file path
CACHE_PATH = BASE_DIR / "ieee_offline_metrics.json"


def load_cached_offline_metrics():
    """
    Static offline validation metrics.
    Safe for Docker / Railway / local.
    """
    if not CACHE_PATH.exists():
        return {
            "status": "missing",
            "message": f"Offline metrics file missing at {CACHE_PATH}"
        }

    with open(CACHE_PATH, "r") as f:
        return json.load(f)
