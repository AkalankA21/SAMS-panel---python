from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.repositories import SessionRepository
import os

router = APIRouter(
    prefix="/visualizations",
    tags=["visualizations"]
)

@router.get("/{session_id}")
def get_session_visualizations(session_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Get absolute server URLs for the intermediate pipeline images generated in this session.
    """
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    results_path = f"./results/{session_id}"
    if not os.path.exists(results_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visualization directory for session ID {session_id} not found."
        )
        
    # Build maps of existing files
    visual_files = {
        "original": "original.png",
        "perspective": "perspective.png",
        "grayscale": "grayscale.png",
        "threshold": "threshold.png",
        "table": "table.png",
        "grid": "grid.png",
        "cells": "cells.png",
        "ocr": "ocr.png",
        "signature": "signature.png",
        "attendance": "attendance.png"
    }
    
    base_url = str(request.base_url)
    urls = {}
    for key, filename in visual_files.items():
        file_path = os.path.join(results_path, filename)
        if os.path.exists(file_path):
            urls[key] = f"{base_url}results/{session_id}/{filename}"
        else:
            urls[key] = None
            
    return urls

