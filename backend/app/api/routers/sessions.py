from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.session import ProcessingSession
from app.database.repositories import SessionRepository
import shutil
import os

router = APIRouter(
    tags=["sessions"]
)

@router.get("/history", response_model=list[ProcessingSession])
@router.get("/sessions", response_model=list[ProcessingSession])
def get_previous_sessions(db: Session = Depends(get_db)):
    """
    Get lists of all past SAMS processing session runs.
    """
    return SessionRepository.list_sessions(db)

@router.delete("/history/{session_id}", status_code=status.HTTP_200_OK)
@router.delete("/session/{session_id}", status_code=status.HTTP_200_OK)
def delete_processing_session(session_id: str, db: Session = Depends(get_db)):
    """
    Delete session metadata database logs and remove generated intermediate image files.
    """
    session = SessionRepository.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found."
        )
        
    # Delete database entries
    success = SessionRepository.delete_session(db, session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session ID {session_id} from database."
        )
        
    # Remove visualization directory
    results_path = f"./results/{session_id}"
    if os.path.exists(results_path):
        try:
            shutil.rmtree(results_path)
        except Exception as e:
            # We don't fail the request if file deletion fails, just log it
            print(f"Warning: Failed to clean up visualizer folder: {e}")
            
    return {"detail": f"Session ID {session_id} and related visualizations successfully deleted."}
