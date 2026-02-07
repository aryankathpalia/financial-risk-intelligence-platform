import json
from pathlib import Path

OFFLINE_DIR = Path("app/ml/offline")
BASE_DIR = Path(__file__).resolve().parents[3]
CACHE_PATH = BASE_DIR / "ml" / "offline" / "ieee_offline_metrics.json"





def load_cached_offline_metrics():
    if not CACHE_PATH.exists():
        raise RuntimeError(
            f"Offline metrics file missing at {CACHE_PATH}"
        )

    with open(CACHE_PATH, "r") as f:
        return json.load(f)
