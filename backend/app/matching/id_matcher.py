from __future__ import annotations

import re

from app.utils.logger import logger


class IDMatcher:
    
    # Match OCR results using student IDs.

    @staticmethod
    def match(
        ocr_result: dict,
        student_records: list[dict],
    ) -> dict | None:
        
        # Match a student using their ID.

        student_id = IDMatcher.extract_id(
            ocr_result
        )

        if not student_id:

            return None

        for student in student_records:

            record_id = IDMatcher.normalize_id(
                student.get(
                    "student_id",
                    "",
                )
            )

            if student_id == record_id:

                logger.info(
                    "ID matched: %s",
                    student_id,
                )

                return {

                    "ocr_result": ocr_result,

                    "student": student,

                    "match_type": "ID",

                    "match_score": 100.0,

                }

        return None

    @staticmethod
    def extract_id(
        ocr_result: dict,
    ) -> str:
        
        # Extract student ID from OCR text.

        text = ocr_result.get(
            "clean_text",
            ocr_result.get(
                "text",
                "",
            ),
        )

        return IDMatcher.normalize_id(
            text
        )

    @staticmethod
    def normalize_id(
        student_id: str,
    ) -> str:
        
        # Remove non-numeric characters.

        return re.sub(

            r"\D",

            "",

            student_id,

        )

    @staticmethod
    def is_valid(
        student_id: str,
        minimum_length: int = 6,
    ) -> bool:
        
        # Validate student ID.

        student_id = IDMatcher.normalize_id(
            student_id
        )

        return (

            len(student_id)

            >= minimum_length

        )

    @staticmethod
    def exists(
        student_id: str,
        student_records: list[dict],
    ) -> bool:
        
        # Check whether an ID exists.

        student_id = IDMatcher.normalize_id(
            student_id
        )

        for student in student_records:

            record_id = IDMatcher.normalize_id(

                student.get(
                    "student_id",
                    "",
                )

            )

            if student_id == record_id:

                return True

        return False

    @staticmethod
    def find(
        student_id: str,
        student_records: list[dict],
    ) -> dict | None:
        
        # Return the matching student record.

        student_id = IDMatcher.normalize_id(
            student_id
        )

        for student in student_records:

            record_id = IDMatcher.normalize_id(

                student.get(
                    "student_id",
                    "",
                )

            )

            if student_id == record_id:

                return student

        return None

    @staticmethod
    def partial_match(
        ocr_result: dict,
        student_records: list[dict],
    ) -> dict | None:
        
        # Match using partial IDs. Useful when OCR misses a few digits.

        student_id = IDMatcher.extract_id(
            ocr_result
        )

        if len(student_id) < 4:

            return None

        for student in student_records:

            record_id = IDMatcher.normalize_id(

                student.get(
                    "student_id",
                    "",
                )

            )

            if (

                student_id in record_id

                or

                record_id.endswith(
                    student_id
                )

            ):

                logger.info(
                    "Partial ID match: %s -> %s",
                    student_id,
                    record_id,
                )

                return {

                    "ocr_result": ocr_result,

                    "student": student,

                    "match_type": "Partial ID",

                    "match_score": 90.0,

                }

        return None