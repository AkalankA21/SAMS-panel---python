from pydantic import BaseModel
from datetime import datetime

class ProcessingSessionBase(BaseModel):
    id: str
    created_at: datetime
    image_name: str
    xml_name: str
    processing_time: float
    status: str
    attendance_rate: float
    present_students: int
    absent_students: int
    manual_review: int

class ProcessingSessionCreate(BaseModel):
    id: str
    image_name: str
    xml_name: str

class ProcessingSession(ProcessingSessionBase):
    class Config:
        from_attributes = True
