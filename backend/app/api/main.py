from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database.database import engine, Base
from app.api.routers import process, results, statistics, logs, visualizations, sessions

# Database migrations to safely add new columns without dropping data
def migrate_database():
    import sqlite3
    from app.database.database import DATABASE_PATH
    try:
        # Check if DB file exists before migrating
        if not os.path.exists(DATABASE_PATH):
            return
            
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processing_sessions'")
        table_exists = cursor.fetchone()
        if not table_exists:
            conn.close()
            return
            
        cursor.execute("PRAGMA table_info(processing_sessions)")
        columns = [row[1] for row in cursor.fetchall()]
        
        new_cols = {
            "ocr_results": "TEXT",
            "matched_students": "TEXT",
            "detected_signatures": "TEXT",
            "confidence_values": "TEXT",
            "visualization_paths": "TEXT",
            "csv_path": "TEXT",
            "logs_path": "TEXT",
            "temp_image_path": "TEXT",
            "temp_xml_path": "TEXT",
            "student_list": "TEXT"
        }
        
        for col, col_type in new_cols.items():
            if col not in columns:
                cursor.execute(f"ALTER TABLE processing_sessions ADD COLUMN {col} {col_type}")
                print(f"Migration: Added column {col} to processing_sessions.")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

# Run migrations
migrate_database()

# Initialize SQLite tables on startup
Base.metadata.create_all(bind=engine)

# Ensure results directory exists for static mounting
os.makedirs("./results", exist_ok=True)

app = FastAPI(
    title="SAMS REST API Backend",
    description="REST API for the AI-powered Student Attendance Management System (SAMS)",
    version="1.0"
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(process.router)
app.include_router(results.router)
app.include_router(statistics.router)
app.include_router(logs.router)
app.include_router(visualizations.router)
app.include_router(sessions.router)

# Mount static folder results/ to render visualization images locally
app.mount("/results", StaticFiles(directory="results"), name="results")

@app.get("/")
def read_root():
    return {
        "title": "SAMS Backend API",
        "status": "online",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
