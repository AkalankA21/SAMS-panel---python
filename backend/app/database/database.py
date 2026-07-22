from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from pathlib import Path

# Resolve absolute path to backend/database directory
DB_DIR = Path(__file__).resolve().parent.parent.parent / "database"
DATABASE_PATH = DB_DIR / "sams.db"

# Ensure the database folder exists
DB_DIR.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Session generator helper for routers dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
