from fastapi import APIRouter
from app.schemas.feedback import AlertFeedback

router = APIRouter()

# Temporary in-memory store
FEEDBACK_DB: list[AlertFeedback] = []

@router.post("/")
def submit_feedback(feedback: AlertFeedback):
    FEEDBACK_DB.append(feedback)
    return {
        "status": "saved",
        "total_feedback": len(FEEDBACK_DB)
    }
