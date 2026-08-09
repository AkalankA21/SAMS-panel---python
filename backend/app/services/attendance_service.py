from __future__ import annotations

from app.models.image_data import ImageData

from app.attendance.attendance_detector import (
    AttendanceDetector,
)
from app.attendance.attendance_validator import (
    AttendanceValidator,
)
from app.attendance.attendance_result import (
    AttendanceResult,
)
from app.attendance.attendance_statistics import (
    AttendanceStatistics,
)

from app.utils.exceptions import (
    ImageProcessingError,
)
from app.utils.logger import logger


class AttendanceService:
    
    # Attendance processing service.

    @staticmethod
    def process(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Execute the attendance pipeline.

        logger.info(
            "Starting attendance pipeline..."
        )

        raw_results = AttendanceDetector.detect(
            image_data
        )

        valid_results, invalid_results = (

            AttendanceValidator.validate(
                raw_results
            )

        )

        image_data.invalid_attendance = (
            invalid_results
        )

        results = [

            AttendanceResult.from_detection(
                result
            )

            for result in valid_results

        ]

        image_data.attendance_results = (
            results
        )

        image_data.present_students = [

            result

            for result in results

            if result.is_present

        ]

        image_data.absent_students = [

            result

            for result in results

            if result.is_absent

        ]

        AttendanceStatistics.calculate(
            image_data
        )

        logger.info(
            "Attendance pipeline completed."
        )

        return results

    @staticmethod
    def get_results(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return attendance results.

        return (

            image_data.attendance_results

            or []

        )

    @staticmethod
    def get_present(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return present students.

        return (

            image_data.present_students

            or []

        )

    @staticmethod
    def get_absent(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return absent students.

        return (

            image_data.absent_students

            or []

        )

    @staticmethod
    def review_required(
        image_data: ImageData,
    ) -> list[AttendanceResult]:
        
        # Return manual review records.

        return [

            result

            for result in (

                image_data.attendance_results

                or []

            )

            if result.is_manual_review

        ]

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return attendance statistics.

        return AttendanceStatistics.calculate(
            image_data
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        return AttendanceStatistics.summary(
            image_data
        )

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Number of attendance records.

        return len(

            image_data.attendance_results

            or []

        )

    @staticmethod
    def has_results(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether attendance results exist.

        return (

            AttendanceService.count(
                image_data
            ) > 0

        )

    @staticmethod
    def get_result(
        image_data: ImageData,
        index: int,
    ) -> AttendanceResult:
        
        # Return one attendance record.

        results = (

            image_data.attendance_results

            or []

        )

        if not results:

            raise ImageProcessingError(
                "No attendance results."
            )

        if (

            index < 0

            or

            index >= len(results)

        ):

            raise IndexError(
                "Attendance index out of range."
            )

        return results[index]

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset attendance pipeline.

        AttendanceDetector.reset(
            image_data
        )

        AttendanceStatistics.reset(
            image_data
        )

        image_data.invalid_attendance = []

        logger.info(
            "Attendance service reset."
        )

    @staticmethod
    def validate_pipeline(
        image_data: ImageData,
    ) -> bool:
        
        # Verify attendance pipeline.

        return (

            image_data.attendance_results

            is not None

            and

            len(
                image_data.attendance_results
            ) > 0

        )