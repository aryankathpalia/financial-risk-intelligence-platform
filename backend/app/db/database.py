from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("DATABASE_PUBLIC_URL")
)


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(
    DATABASE_URL,

 
    pool_size=1,              # ONE connection
    max_overflow=0,           # no extra connections
    pool_pre_ping=True,       
    pool_recycle=180,         

    connect_args={
        "sslmode": "require",
        "connect_timeout": 5,
    },
)



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
