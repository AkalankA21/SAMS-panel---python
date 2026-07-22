from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.session import ProcessingSession
from app.services.session_service import SessionService

router = APIRouter(
    prefix="/process",
    tags=["process"]
)

@router.post("", response_model=ProcessingSession, status_code=status.HTTP_201_CREATED)
async def process_sheet(
    image: UploadFile = File(...),
    xml: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload image scan and official student XML structure, 
    execute SAMS pipeline, record log streams, and save results.
    """
    # Simple validation on formats
    if not (image.filename.lower().endswith(('.jpg', '.jpeg', '.png'))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Supported formats: .jpg, .jpeg, .png"
        )
    if not xml.filename.lower().endswith('.xml'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid XML file format. Supported format: .xml"
        )
        
    try:
        image_bytes = await image.read()
        xml_bytes = await xml.read()
        
        session = SessionService.process_attendance(
            db=db,
            image_bytes=image_bytes,
            image_filename=image.filename,
            xml_bytes=xml_bytes,
            xml_filename=xml.filename
        )
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SAMS execution failed: {str(e)}"
        )
