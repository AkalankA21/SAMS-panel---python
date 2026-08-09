from __future__ import annotations

from app.models.image_data import ImageData
from app.attendance.attendance_result import (
    AttendanceResult,
)


class AttendanceStatistics:
    
    # Calculate attendance statistics.

    @staticmethod
    def calculate(
        image_data: ImageData,
    ) -> dict:
        
        # Calculate attendance statistics.

        results = (
            image_data.attendance_results
            or []
        )

        total = len(results)

        present = sum(
            1
            for record in results
            if isinstance(record, AttendanceResult)
            and record.is_present
        )

        absent = sum(
            1
            for record in results
            if isinstance(record, AttendanceResult)
            and record.is_absent
        )

        review = sum(
            1
            for record in results
            if isinstance(record, AttendanceResult)
            and record.is_manual_review
        )

        signature_detected = sum(
            1
            for record in results
            if isinstance(record, AttendanceResult)
            and record.signature_detected
        )

        attendance_rate = (
            present / total * 100
            if total > 0
            else 0.0
        )

        absence_rate = (
            absent / total * 100
            if total > 0
            else 0.0
        )

        signature_rate = (
            signature_detected / total * 100
            if total > 0
            else 0.0
        )

        statistics = {

            "total_students": total,

            "present_students": present,

            "absent_students": absent,

            "manual_review": review,

            "signature_detected": signature_detected,

            "attendance_rate": round(
                attendance_rate,
                2,
            ),

            "absence_rate": round(
                absence_rate,
                2,
            ),

            "signature_detection_rate": round(
                signature_rate,
                2,
            ),

        }

        image_data.attendance_statistics = (
            statistics
        )

        return statistics

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        stats = AttendanceStatistics.calculate(
            image_data
        )

        return (
            "\nAttendance Statistics\n"
            "-------------------------\n"
            f"Total Students      : {stats['total_students']}\n"
            f"Present             : {stats['present_students']}\n"
            f"Absent              : {stats['absent_students']}\n"
            f"Manual Review       : {stats['manual_review']}\n"
            f"Attendance Rate     : {stats['attendance_rate']}%\n"
            f"Absence Rate        : {stats['absence_rate']}%\n"
            f"Signature Detected  : {stats['signature_detected']}\n"
            f"Signature Rate      : {stats['signature_detection_rate']}%\n"
        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset attendance statistics.

        image_data.attendance_statistics = {}

    @staticmethod
    def get(
        image_data: ImageData,
    ) -> dict:
        
        # Return statistics.

        return (
            image_data.attendance_statistics
            or {}
        )