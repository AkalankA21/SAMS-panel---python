from __future__ import annotations

import csv
from pathlib import Path

from app.models.image_data import ImageData
from app.attendance.attendance_result import (
    AttendanceResult,
)

from app.utils.logger import logger
from app.utils.exceptions import (
    ImageProcessingError,
)


class AttendanceExporter:
    
    # Export attendance results.

    @staticmethod
    def export_csv(
        image_data: ImageData,
        output_file: str | Path,
    ) -> Path:
        
        # Export attendance results to CSV.

        results = (
            image_data.attendance_results
            or []
        )

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not results:

            logger.info(
                "No attendance results available; creating empty export file."
            )

            with open(
                output_file,
                "w",
                newline="",
                encoding="utf-8",
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "Student ID",
                        "Student Name",
                        "Status",
                        "Signature Detected",
                        "Confidence",
                        "Ink Ratio",
                        "Row",
                        "Column",
                        "Requires Review",
                    ]
                )

            return output_file

        with open(

            output_file,

            "w",

            newline="",

            encoding="utf-8",

        ) as file:

            writer = csv.writer(file)

            writer.writerow(

                [

                    "Student ID",

                    "Student Name",

                    "Status",

                    "Signature Detected",

                    "Confidence",

                    "Ink Ratio",

                    "Row",

                    "Column",

                    "Requires Review",

                ]

            )

            for record in results:

                if not isinstance(
                    record,
                    AttendanceResult,
                ):
                    continue

                writer.writerow(

                    [

                        record.student_id,

                        record.student_name,

                        record.status,

                        "Yes"
                        if record.signature_detected
                        else "No",

                        f"{record.confidence:.2f}",

                        f"{record.ink_ratio:.4f}",

                        record.row,

                        record.column,

                        "Yes"
                        if record.requires_review
                        else "No",

                    ]

                )

        logger.info(

            "Attendance exported to %s",

            output_file,

        )

        return output_file

    @staticmethod
    def present_students(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return present students.

        return [

            record

            for record in (
                image_data.attendance_results
                or []
            )

            if isinstance(
                record,
                AttendanceResult,
            )

            and

            record.is_present

        ]

    @staticmethod
    def absent_students(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return absent students.

        return [

            record

            for record in (
                image_data.attendance_results
                or []
            )

            if isinstance(
                record,
                AttendanceResult,
            )

            and

            record.is_absent

        ]

    @staticmethod
    def manual_review(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return manual review records.

        return [

            record

            for record in (
                image_data.attendance_results
                or []
            )

            if isinstance(
                record,
                AttendanceResult,
            )

            and

            record.is_manual_review

        ]

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> dict:
        
        # Export summary.

        return {

            "Total":

                len(
                    image_data.attendance_results
                    or []
                ),

            "Present":

                len(
                    AttendanceExporter.present_students(
                        image_data
                    )
                ),

            "Absent":

                len(
                    AttendanceExporter.absent_students(
                        image_data
                    )
                ),

            "Manual Review":

                len(
                    AttendanceExporter.manual_review(
                        image_data
                    )
                ),

        }