from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.repositories import SessionRepository
from app.utils.logger import logger
from app.utils.serializer import serialize_result
import os
import json

router = APIRouter(
    prefix="/results",
    tags=["results"]
)

@router.get("/{session_id}")
def get_attendance_results(session_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Get the complete production attendance results and visualization maps for the given job ID.
    """
    logger.info("Fetching Job...")
    
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    status_str = "completed" if session.status == "success" else session.status
    
    # Parse OCR
    ocr = []
    if session.ocr_results:
        try:
            ocr = json.loads(session.ocr_results)
        except Exception:
            pass
            
    # Parse Students
    students = []
    if session.student_list:
        try:
            raw_students = json.loads(session.student_list)
            for s in raw_students:
                status_val = s.get("status", s.get("attendance", "Absent"))
                review_val = s.get("requires_review", s.get("review_required", False))
                students.append({
                    "student_id": s.get("student_id"),
                    "student_name": s.get("student_name"),
                    "attendance": status_val,
                    "status": status_val,
                    "signature_detected": s.get("signature_detected", False),
                    "confidence": s.get("confidence", 0.0),
                    "review_required": review_val,
                    "requires_review": review_val,
                    "ink_ratio": s.get("ink_ratio", 0.0)
                })
        except Exception:
            pass
            
    if not students:
        # Fallback to records table
        for r in session.records:
            students.append({
                "student_id": r.student_id,
                "student_name": r.student_name,
                "attendance": r.attendance,
                "status": r.attendance,
                "signature_detected": r.signature_detected,
                "confidence": r.confidence,
                "review_required": r.review_required,
                "requires_review": r.review_required,
                "detected_name": r.detected_name,
                "ink_ratio": 0.0
            })
            
    # Parse statistics
    statistics = {}
    if session.statistics:
        statistics = {
            "tables_detected": session.statistics.tables_detected,
            "cells_detected": session.statistics.cells_detected,
            "cells_valid": session.statistics.cells_valid,
            "ocr_texts": session.statistics.ocr_texts,
            "matched_students": session.statistics.matched_students,
            "signatures": session.statistics.signatures
        }
        
    # Attendance summary
    total = session.present_students + session.absent_students + session.manual_review
    attendance = {
        "attendance_rate": session.attendance_rate,
        "present": session.present_students,
        "absent": session.absent_students,
        "manual_review": session.manual_review,
        "total": total
    }
    
    # Build absolute visualization URLs
    results_path = f"./results/{session_id}"
    base_url = str(request.base_url)
    
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
    
    visualizations = {}
    for key, filename in visual_files.items():
        file_path = os.path.join(results_path, filename)
        if os.path.exists(file_path):
            visualizations[key] = f"{base_url}results/{session_id}/{filename}"
        else:
            visualizations[key] = None
            
    # Build absolute download URLs
    downloads = {}
    csv_file = os.path.join(results_path, "matched_students.csv")
    if os.path.exists(csv_file):
        downloads["csv"] = f"{base_url}results/{session_id}/matched_students.csv"
        
    logger.info("Returning JSON...")
    
    return serialize_result({
        "job_id": session_id,
        "status": status_str,
        "attendance": attendance,
        "students": students,
        "ocr": ocr,
        "statistics": statistics,
        "visualizations": visualizations,
        "downloads": downloads
    })

