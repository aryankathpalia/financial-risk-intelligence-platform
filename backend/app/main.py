# app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.base import Base
from app.db.models import transaction

from app.api.ingestion import router as ingestion_router
from app.api.analytics import router as analytics_router
from app.api import models

from app.api import (
    scoring,
    transactions,
    dashboard,
    alerts,
    feedback,
)

from app.api import health

                  
# DB init
                  
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Risk Intelligence API",
    version="0.1.0"
)

                  
# CORS
                  
import os

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://financial-risk-intelligence-platform-.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



                  
# Routers (ONLY real API routers)
                  

app.include_router(
    scoring.router,
    prefix="/api/scoring",
    tags=["Scoring"]
)

app.include_router(
    transactions.router,
    prefix="/api/transactions",
    tags=["Transactions"]
)

app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    alerts.router,
    prefix="/api/alerts",
    tags=["Alerts"]
)

app.include_router(
    feedback.router,
    prefix="/api/feedback",
    tags=["Feedback"]
)

app.include_router(
    ingestion_router,
    prefix="/api/ingestion",
    tags=["Ingestion"]
)


app.include_router(health.router)


app.include_router(models.router)

app.include_router(
    analytics_router,
    prefix="/api/analytics",
    tags=["Analytics"]
)

