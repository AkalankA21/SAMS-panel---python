from __future__ import annotations

from app.utils.logger import logger


class AttendanceValidator:
    
    # Validate attendance results.

    VALID_STATUS = {

        "Present",

        "Absent",

        "Manual Review",

    }

    @staticmethod
    def validate(
        attendance_results: list[dict],
    ) -> tuple[list[dict], list[dict]]:
        
        # Validate attendance results.

        valid = []

        invalid = []

        seen_students = set()

        for result in attendance_results:

            if not AttendanceValidator.is_valid(
                result,
                seen_students,
            ):

                invalid.append(result)

                continue

            student = result["match"]

            student_id = getattr(

                student,

                "student_id",

                "",

            )

            seen_students.add(
                student_id
            )

            valid.append(result)

        logger.info(

            "%d valid attendance records, %d invalid.",

            len(valid),

            len(invalid),

        )

        return (

            valid,

            invalid,

        )

    @staticmethod
    def is_valid(
        result: dict,
        seen_students: set,
    ) -> bool:
        
        # Validate a single attendance record.

        if result is None:

            return False

        if "status" not in result:

            return False

        if result["status"] not in AttendanceValidator.VALID_STATUS:

            return False

        if "match" not in result:

            return False

        student = result["match"]

        student_id = getattr(

            student,

            "student_id",

            "",

        )

        if student_id in seen_students:

            logger.warning(

                "Duplicate attendance record: %s",

                student_id,

            )

            return False

        return True

    @staticmethod
    def manual_review(
        attendance_results: list[dict],
    ) -> list[dict]:
        
        # Return manual review records.

        return [

            result

            for result in attendance_results

            if result["status"] == "Manual Review"

        ]

    @staticmethod
    def duplicates(
        attendance_results: list[dict],
    ) -> list[dict]:
        
        # Return duplicate records.

        duplicates = []

        seen = set()

        for result in attendance_results:

            student = result["match"]

            student_id = getattr(

                student,

                "student_id",

                "",

            )

            if student_id in seen:

                duplicates.append(result)

            else:

                seen.add(student_id)

        return duplicates

    @staticmethod
    def summary(
        attendance_results: list[dict],
    ) -> dict:
        
        # Return validation summary.

        valid, invalid = AttendanceValidator.validate(
            attendance_results
        )

        review = AttendanceValidator.manual_review(
            attendance_results
        )

        duplicates = AttendanceValidator.duplicates(
            attendance_results
        )

        return {

            "Total Records":
                len(attendance_results),

            "Valid Records":
                len(valid),

            "Invalid Records":
                len(invalid),

            "Duplicate Records":
                len(duplicates),

            "Manual Review":
                len(review),

        }