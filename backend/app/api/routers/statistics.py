from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.repositories import StatisticRepository, SessionRepository
from app.utils.serializer import serialize_result

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"]
)

@router.get("/{session_id}")
def get_session_statistics(session_id: str, db: Session = Depends(get_db)):
    """
    Get pipeline statistics metadata for the given session ID.
    """
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    stats = StatisticRepository.get_statistic_by_session(db, session_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Statistics for session ID {session_id} not found."
        )
        
    return serialize_result({
        "id": stats.id,
        "session_id": stats.session_id,
        "tables_detected": stats.tables_detected,
        "cells_detected": stats.cells_detected,
        "cells_valid": stats.cells_valid,
        "ocr_texts": stats.ocr_texts,
        "matched_students": stats.matched_students,
        "signatures": stats.signatures
    })
