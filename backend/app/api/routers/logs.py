from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.log import ProcessingLog
from app.database.repositories import ProcessingLogRepository, SessionRepository

router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)

@router.get("/{session_id}", response_model=list[ProcessingLog])
def get_session_logs(session_id: str, db: Session = Depends(get_db)):
    """
    Get pipeline run logs for the given session ID.
    """
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    logs = ProcessingLogRepository.get_logs_by_session(db, session_id)
    return logs
