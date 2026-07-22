from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class ProcessingSession(Base):
    __tablename__ = "processing_sessions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    image_name = Column(String, nullable=False)
    xml_name = Column(String, nullable=False)
    processing_time = Column(Float, default=0.0)
    status = Column(String, default="success")  # success, failed
    attendance_rate = Column(Float, default=0.0)
    present_students = Column(Integer, default=0)
    absent_students = Column(Integer, default=0)
    manual_review = Column(Integer, default=0)

    # Redesigned persistent storage fields
    ocr_results = Column(String, nullable=True)
    matched_students = Column(String, nullable=True)
    detected_signatures = Column(String, nullable=True)
    confidence_values = Column(String, nullable=True)
    visualization_paths = Column(String, nullable=True)
    csv_path = Column(String, nullable=True)
    logs_path = Column(String, nullable=True)
    temp_image_path = Column(String, nullable=True)
    temp_xml_path = Column(String, nullable=True)
    student_list = Column(String, nullable=True)

    # Relationships
    records = relationship("StudentRecord", back_populates="session", cascade="all, delete-orphan")
    logs = relationship("ProcessingLog", back_populates="session", cascade="all, delete-orphan")
    statistics = relationship("Statistic", back_populates="session", uselist=False, cascade="all, delete-orphan")


class StudentRecord(Base):
    __tablename__ = "student_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("processing_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(String, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    detected_name = Column(String, nullable=True)
    attendance = Column(String, nullable=False)  # Present, Absent, Manual Review
    confidence = Column(Float, default=1.0)
    signature_detected = Column(Boolean, default=False)
    review_required = Column(Boolean, default=False)

    # Relationships
    session = relationship("ProcessingSession", back_populates="records")


class ProcessingLog(Base):
    __tablename__ = "processing_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("processing_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    stage = Column(String, nullable=False)
    message = Column(String, nullable=False)
    level = Column(String, default="INFO")  # INFO, WARNING, ERROR
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ProcessingSession", back_populates="logs")


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("processing_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    tables_detected = Column(Integer, default=0)
    cells_detected = Column(Integer, default=0)
    cells_valid = Column(Integer, default=0)
    ocr_texts = Column(Integer, default=0)
    matched_students = Column(Integer, default=0)
    signatures = Column(Integer, default=0)

    # Relationships
    session = relationship("ProcessingSession", back_populates="statistics")
