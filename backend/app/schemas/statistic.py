from pydantic import BaseModel

class StatisticBase(BaseModel):
    tables_detected: int
    cells_detected: int
    cells_valid: int
    ocr_texts: int
    matched_students: int
    signatures: int

class StatisticCreate(StatisticBase):
    pass

class Statistic(StatisticBase):
    id: int
    session_id: str

    class Config:
        from_attributes = True
