from sqlalchemy.orm import Session
from app.database.models import ProcessingSession, StudentRecord, ProcessingLog, Statistic

class SessionRepository:
    @staticmethod
    def create_session(db: Session, session: ProcessingSession) -> ProcessingSession:
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session(db: Session, session_id: str) -> ProcessingSession | None:
        return db.query(ProcessingSession).filter(ProcessingSession.id == session_id).first()

    @staticmethod
    def list_sessions(db: Session) -> list[ProcessingSession]:
        return db.query(ProcessingSession).order_by(ProcessingSession.created_at.desc()).all()

    @staticmethod
    def delete_session(db: Session, session_id: str) -> bool:
        session = db.query(ProcessingSession).filter(ProcessingSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
            return True
        return False


class StudentRecordRepository:
    @staticmethod
    def add_records(db: Session, records: list[StudentRecord]) -> list[StudentRecord]:
        db.add_all(records)
        db.commit()
        return records

    @staticmethod
    def get_records_by_session(db: Session, session_id: str) -> list[StudentRecord]:
        return db.query(StudentRecord).filter(StudentRecord.session_id == session_id).all()


class ProcessingLogRepository:
    @staticmethod
    def add_logs(db: Session, logs: list[ProcessingLog]) -> list[ProcessingLog]:
        db.add_all(logs)
        db.commit()
        return logs

    @staticmethod
    def get_logs_by_session(db: Session, session_id: str) -> list[ProcessingLog]:
        return db.query(ProcessingLog).filter(ProcessingLog.session_id == session_id).order_by(ProcessingLog.timestamp.asc()).all()


class StatisticRepository:
    @staticmethod
    def create_statistic(db: Session, statistic: Statistic) -> Statistic:
        db.add(statistic)
        db.commit()
        db.refresh(statistic)
        return statistic

    @staticmethod
    def get_statistic_by_session(db: Session, session_id: str) -> Statistic | None:
        return db.query(Statistic).filter(Statistic.session_id == session_id).first()
