from pydantic import BaseModel

class StudentRecordBase(BaseModel):
    student_id: str
    student_name: str
    detected_name: str | None = None
    attendance: str
    confidence: float
    signature_detected: bool
    review_required: bool

class StudentRecordCreate(StudentRecordBase):
    pass

class StudentRecord(StudentRecordBase):
    id: int
    session_id: str

    class Config:
        from_attributes = True
