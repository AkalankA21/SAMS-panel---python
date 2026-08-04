import os
import uuid
import time
import shutil
import logging
import json
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np
from sqlalchemy.orm import Session

from app.sams import SAMS
from app.database.models import ProcessingSession, StudentRecord, ProcessingLog, Statistic
from app.database.repositories import SessionRepository, StudentRecordRepository, ProcessingLogRepository, StatisticRepository
from app.visualization.table_visualizer import TableVisualizer
from app.visualization.student_table import StudentTable
from app.utils.logger import logger as app_logger
from app.utils.serializer import serialize_result

# Configure logging interception
class CaptureLogsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_entries = []

    def emit(self, record):
        # We catch any logs from the pipeline
        self.log_entries.append({
            "stage": getattr(record, "stage", "Pipeline"),
            "message": record.getMessage(),
            "level": record.levelname,
            "timestamp": datetime.utcnow()
        })

class SessionService:
    @staticmethod
    def process_attendance(db: Session, image_bytes: bytes, image_filename: str, xml_bytes: bytes, xml_filename: str) -> ProcessingSession:
        session_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        
        # Paths setup
        results_dir = Path(f"./results/{session_id}")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Unique persistent file names stored in the session directory
        timestamp_prefix = created_at.strftime("%Y%m%d_%H%M%S")
        persistent_image_path = results_dir / f"{timestamp_prefix}_image_{image_filename}"
        persistent_xml_path = results_dir / f"{timestamp_prefix}_xml_{xml_filename}"
        
        # Save persistent files
        with open(persistent_image_path, "wb") as f:
            f.write(image_bytes)
        with open(persistent_xml_path, "wb") as f:
            f.write(xml_bytes)
            
        # Logging attachment
        log_capturer = CaptureLogsHandler()
        sams_logger = logging.getLogger("SAMS")
        sams_logger.addHandler(log_capturer)
        
        start_time = time.time()
        status = "success"
        
        # Explicitly log stages
        log_capturer.log_entries.append({
            "stage": "Image Loading",
            "message": f"Uploading {image_filename} and {xml_filename} completed successfully.",
            "level": "INFO",
            "timestamp": datetime.utcnow()
        })
        
        try:
            # Run SAMS pipeline
            sams = SAMS(image_path=persistent_image_path, xml_path=persistent_xml_path)
            image_data = sams.run()
            
            processing_time = round(time.time() - start_time, 3)
            
            # 1. Export intermediate stage visualization images
            # Save original
            cv2.imwrite(str(results_dir / "original.png"), image_data.image)
            
            # Save perspective
            if image_data.perspective_image is not None:
                cv2.imwrite(str(results_dir / "perspective.png"), image_data.perspective_image)
            
            # Save grayscale
            if image_data.grayscale_image is not None:
                cv2.imwrite(str(results_dir / "grayscale.png"), image_data.grayscale_image)
                
            # Save threshold
            # Use binary_image if present, else fallback
            thresh_img = image_data.binary_image if image_data.binary_image is not None else image_data.threshold_image
            if thresh_img is not None:
                cv2.imwrite(str(results_dir / "threshold.png"), thresh_img)
                
            # Save detected table overlay
            try:
                table_overlay = TableVisualizer.contour(image_data)
                cv2.imwrite(str(results_dir / "table.png"), table_overlay)
            except Exception:
                pass
                
            # Save grid lines overlay
            try:
                grid_overlay = TableVisualizer.grid(image_data)
                cv2.imwrite(str(results_dir / "grid.png"), grid_overlay)
            except Exception:
                pass

            # Save cells crop overlay (Draw boundary rectangles)
            if image_data.perspective_image is not None and image_data.valid_cells:
                cells_img = image_data.perspective_image.copy()
                for cell in image_data.valid_cells:
                    x, y, w, h = cell.get("bbox", (0, 0, 0, 0))
                    cv2.rectangle(cells_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imwrite(str(results_dir / "cells.png"), cells_img)

            # Save OCR overlay
            if image_data.perspective_image is not None and image_data.ocr_results:
                ocr_img = image_data.perspective_image.copy()
                for res in image_data.ocr_results:
                    # Get bbox from corresponding valid cell if matches
                    cell_idx = res.get("id")
                    if cell_idx is not None and cell_idx < len(image_data.valid_cells):
                        x, y, w, h = image_data.valid_cells[cell_idx].get("bbox", (0,0,0,0))
                        cv2.rectangle(ocr_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        cv2.putText(ocr_img, str(res.get("text", "")), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.imwrite(str(results_dir / "ocr.png"), ocr_img)

            # Save signature overlay
            if image_data.perspective_image is not None and image_data.attendance_results:
                sig_img = image_data.perspective_image.copy()
                for record in image_data.attendance_results:
                    sig = record.get("signature")
                    if sig:
                        # Extract row and column coordinates
                        bbox = getattr(sig, "bbox", sig.get("bbox", None)) if hasattr(sig, "bbox") or isinstance(sig, dict) else None
                        if bbox:
                            x, y, w, h = bbox
                            color = (0, 255, 0) if record.get("status") == "Present" else (0, 0, 255)
                            cv2.rectangle(sig_img, (x, y), (x+w, y+h), color, 2)
                cv2.imwrite(str(results_dir / "signature.png"), sig_img)

            # Save final attendance verdict overlay
            if image_data.perspective_image is not None and image_data.attendance_results:
                att_img = image_data.perspective_image.copy()
                for record in image_data.attendance_results:
                    match = record.get("match")
                    sig = record.get("signature")
                    status_str = record.get("status", "Absent")
                    if sig and match:
                        bbox = getattr(sig, "bbox", sig.get("bbox", None)) if hasattr(sig, "bbox") or isinstance(sig, dict) else None
                        if bbox:
                            x, y, w, h = bbox
                            color = (0, 255, 0) if status_str == "Present" else (0, 0, 255) if status_str == "Absent" else (0, 165, 255)
                            cv2.putText(att_img, f"{status_str}", (x - 120, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.imwrite(str(results_dir / "attendance.png"), att_img)

            # Save match results to CSV in the persistent folder
            try:
                StudentTable.export_csv(image_data, results_dir / "matched_students.csv")
            except Exception as csv_err:
                app_logger.error(f"Failed to export CSV: {csv_err}")

            # Parse results statistics
            total_students = len(image_data.attendance_results or [])
            present_students = len(image_data.present_students or [])
            absent_students = len(image_data.absent_students or [])
            manual_review_students = total_students - present_students - absent_students
            
            att_rate = round((present_students / total_students * 100), 2) if total_students > 0 else 0.0
            
            # Serialize fields for SQLite
            serialized_students = [res.to_dict() for res in (image_data.attendance_results or [])]
            serialized_ocr = image_data.ocr_results or []
            serialized_matches = [m.to_dict() for m in (image_data.matched_students or [])]
            
            detected_sigs = []
            for r in (image_data.attendance_results or []):
                sig = r.get("signature")
                if sig:
                    detected_sigs.append(sig if isinstance(sig, dict) else {
                        "present": getattr(sig, "present", False),
                        "confidence": getattr(sig, "confidence", 0.0),
                        "ink_ratio": getattr(sig, "ink_ratio", 0.0),
                        "bbox": getattr(sig, "bbox", None)
                    })
            
            conf_vals = {
                "ocr": [float(res.get("confidence", 0.0)) for res in (image_data.ocr_results or [])],
                "signature": [float(r.get("confidence", 0.0)) for r in (image_data.attendance_results or []) if r.get("signature")]
            }
            
            vis_paths = {
                "original": f"results/{session_id}/original.png",
                "perspective": f"results/{session_id}/perspective.png",
                "grayscale": f"results/{session_id}/grayscale.png",
                "threshold": f"results/{session_id}/threshold.png",
                "table": f"results/{session_id}/table.png",
                "grid": f"results/{session_id}/grid.png",
                "cells": f"results/{session_id}/cells.png",
                "ocr": f"results/{session_id}/ocr.png",
                "signature": f"results/{session_id}/signature.png",
                "attendance": f"results/{session_id}/attendance.png"
            }

            # Add log write stage
            log_capturer.log_entries.append({
                "stage": "Database Save",
                "message": "Session attendance records written to SQLite database.",
                "level": "INFO",
                "timestamp": datetime.utcnow()
            })

            # Save log file in the persistent folder
            try:
                log_file_path = results_dir / "processing.log"
                with open(log_file_path, "w", encoding="utf-8") as lf:
                    for log_val in log_capturer.log_entries:
                        lf.write(f"[{log_val['level']}] [{log_val['stage']}] {log_val['message']}\n")
            except Exception as log_err:
                app_logger.error(f"Failed to write log file: {log_err}")

            # Logs required by prompt
            app_logger.info("Saving Job...")
            app_logger.info("Saving Results...")
            
            # Create ProcessingSession database row
            session_row = ProcessingSession(
                id=session_id,
                created_at=created_at,
                image_name=image_filename,
                xml_name=xml_filename,
                processing_time=processing_time,
                status=status,
                attendance_rate=att_rate,
                present_students=present_students,
                absent_students=absent_students,
                manual_review=manual_review_students,
                ocr_results=json.dumps(serialize_result(serialized_ocr)),
                matched_students=json.dumps(serialize_result(serialized_matches)),
                detected_signatures=json.dumps(serialize_result(detected_sigs)),
                confidence_values=json.dumps(serialize_result(conf_vals)),
                visualization_paths=json.dumps(serialize_result(vis_paths)),
                csv_path=f"results/{session_id}/matched_students.csv",
                logs_path=f"results/{session_id}/processing.log",
                temp_image_path=str(persistent_image_path),
                temp_xml_path=str(persistent_xml_path),
                student_list=json.dumps(serialize_result(serialized_students))
            )
            SessionRepository.create_session(db, session_row)
            
            # Save student records
            db_records = []
            for res in (image_data.attendance_results or []):
                match = res.get("match")
                sig = res.get("signature")
                status_str = res.get("status", "Absent")
                
                student_id = "Unknown"
                student_name = "Unknown"
                detected_name = ""
                confidence = 1.0
                requires_review = False
                
                if match:
                    student_id = getattr(match, "student_id", getattr(match, "id", match.get("student_id", match.get("id", "Unknown")))) if isinstance(match, dict) else getattr(match, "student_id", "Unknown")
                    student_name = getattr(match, "student_name", "Unknown")
                    detected_name = getattr(match, "cleaned_text", getattr(match, "ocr_text", ""))
                    confidence = getattr(match, "confidence", 1.0)
                    requires_review = getattr(match, "requires_review", False)

                sig_detected = False
                if sig:
                    sig_detected = sig.get("present", status_str == "Present")

                db_records.append(StudentRecord(
                    session_id=session_id,
                    student_id=str(student_id),
                    student_name=str(student_name),
                    detected_name=str(detected_name),
                    attendance=status_str,
                    confidence=float(confidence),
                    signature_detected=bool(sig_detected),
                    review_required=bool(requires_review)
                ))
            StudentRecordRepository.add_records(db, db_records)
            
            # Save SAMS processing metrics/statistics
            tables_count = 1 if image_data.table_contour is not None else 0
            cells_count = len(image_data.cells or [])
            valid_cells_count = len(image_data.valid_cells or [])
            ocr_text_count = len(image_data.recognized_text or [])
            matched_count = len(image_data.matched_students or [])
            sig_count = present_students
            
            statistic_row = Statistic(
                session_id=session_id,
                tables_detected=tables_count,
                cells_detected=cells_count,
                cells_valid=valid_cells_count,
                ocr_texts=ocr_text_count,
                matched_students=matched_count,
                signatures=sig_count
            )
            StatisticRepository.create_statistic(db, statistic_row)
            
            # Write intercepted logs to table
            db_logs = []
            for log_val in log_capturer.log_entries:
                db_logs.append(ProcessingLog(
                    session_id=session_id,
                    stage=log_val["stage"],
                    message=log_val["message"],
                    level=log_val["level"],
                    timestamp=log_val["timestamp"]
                ))
            ProcessingLogRepository.add_logs(db, db_logs)
            
            app_logger.info("Result Stored.")
            return session_row
            
        except Exception as e:
            # Log failure row
            status = "failed"
            error_msg = str(e)
            
            # Save session entry as failed
            failed_session = ProcessingSession(
                id=session_id,
                created_at=created_at,
                image_name=image_filename,
                xml_name=xml_filename,
                processing_time=round(time.time() - start_time, 3),
                status=status,
                csv_path=None,
                logs_path=f"results/{session_id}/processing.log",
                temp_image_path=str(persistent_image_path),
                temp_xml_path=str(persistent_xml_path)
            )
            db.add(failed_session)
            db.commit()
            
            # Append final error log
            log_capturer.log_entries.append({
                "stage": "Pipeline",
                "message": f"Pipeline crashed with exception: {error_msg}",
                "level": "ERROR",
                "timestamp": datetime.utcnow()
            })
            
            # Write logs to processing.log file
            try:
                log_file_path = results_dir / "processing.log"
                with open(log_file_path, "w", encoding="utf-8") as lf:
                    for log_val in log_capturer.log_entries:
                        lf.write(f"[{log_val['level']}] [{log_val['stage']}] {log_val['message']}\n")
            except Exception:
                pass

            # Save error log inside database table
            db_logs = []
            for log_val in log_capturer.log_entries:
                db_logs.append(ProcessingLog(
                    session_id=session_id,
                    stage=log_val["stage"],
                    message=log_val["message"],
                    level=log_val["level"],
                    timestamp=log_val["timestamp"]
                ))
            ProcessingLogRepository.add_logs(db, db_logs)
            
            raise e
            
        finally:
            # Remove custom logger handler
            sams_logger.removeHandler(log_capturer)