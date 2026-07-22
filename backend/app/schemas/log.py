from pydantic import BaseModel
from datetime import datetime

class ProcessingLogBase(BaseModel):
    stage: str
    message: str
    level: str
    timestamp: datetime

class ProcessingLogCreate(ProcessingLogBase):
    pass

class ProcessingLog(ProcessingLogBase):
    id: int
    session_id: str

    class Config:
        from_attributes = True
