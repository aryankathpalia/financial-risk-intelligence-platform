import json
from pathlib import Path

OFFLINE_METRICS_PATH = Path("app/ml/offline/offline_metrics.json")


def get_model_metrics():
    """
    Serve cached offline model metrics.
    This must be FAST and never run ML inference.
    """
    if not OFFLINE_METRICS_PATH.exists():
        raise RuntimeError(
            "Offline metrics not found. Run compute_and_cache_offline_metrics() first."
        )

    with open(OFFLINE_METRICS_PATH, "r") as f:
        return json.load(f)
