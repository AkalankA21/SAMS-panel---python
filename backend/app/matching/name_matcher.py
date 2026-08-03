from __future__ import annotations

import re

from app.utils.logger import logger


class NameMatcher:
    
    # Match OCR results using student names.

    @staticmethod
    def match(
        ocr_result: dict,
        student_records: list[dict],
    ) -> dict | None:
        
        # Match using an exact normalized name.

        name = NameMatcher.extract_name(
            ocr_result
        )

        if not name:

            return None

        for student in student_records:

            student_name = NameMatcher.normalize_name(

                student.get(
                    "name",
                    "",
                )

            )

            if name == student_name:

                logger.info(
                    "Name matched: %s",
                    student_name,
                )

                return {

                    "ocr_result": ocr_result,

                    "student": student,

                    "match_type": "Name",

                    "match_score": 100.0,

                }

        return None

    @staticmethod
    def extract_name(
        ocr_result: dict,
    ) -> str:
        
        # Extract normalized name from OCR.

        text = ocr_result.get(

            "clean_text",

            ocr_result.get(

                "text",

                "",

            ),

        )

        return NameMatcher.normalize_name(
            text
        )

    @staticmethod
    def normalize_name(
        name: str,
    ) -> str:
        
        # Normalize student names.

        if not name:

            return ""

        name = name.upper()

        name = re.sub(

            r"[^\w\s]",

            "",

            name,

        )

        name = re.sub(

            r"\s+",

            " ",

            name,

        )

        return name.strip()

    @staticmethod
    def equals(
        name1: str,
        name2: str,
    ) -> bool:
        
        # Compare two names.

        return (

            NameMatcher.normalize_name(
                name1
            )

            ==

            NameMatcher.normalize_name(
                name2
            )

        )

    @staticmethod
    def exists(
        name: str,
        student_records: list[dict],
    ) -> bool:
        
        # Check whether a name exists.

        name = NameMatcher.normalize_name(
            name
        )

        for student in student_records:

            if (

                name

                ==

                NameMatcher.normalize_name(

                    student.get(

                        "name",

                        "",

                    )

                )

            ):

                return True

        return False

    @staticmethod
    def find(
        name: str,
        student_records: list[dict],
    ) -> dict | None:
        
        # Return matching student.

        name = NameMatcher.normalize_name(
            name
        )

        for student in student_records:

            student_name = NameMatcher.normalize_name(

                student.get(
                    "name",
                    "",
                )

            )

            if name == student_name:

                return student

        return None

    @staticmethod
    def contains(
        ocr_result: dict,
        student_records: list[dict],
    ) -> dict | None:
        
        # Match using substring comparison. Useful when OCR recognizes only part of a student's name.

        name = NameMatcher.extract_name(
            ocr_result
        )

        if len(name) < 3:

            return None

        for student in student_records:

            student_name = NameMatcher.normalize_name(

                student.get(
                    "name",
                    "",
                )

            )

            if (

                name in student_name

                or

                student_name in name

            ):

                logger.info(
                    "Partial name match: %s",
                    student_name,
                )

                return {

                    "ocr_result": ocr_result,

                    "student": student,

                    "match_type": "Partial Name",

                    "match_score": 90.0,

                }

        return None

    @staticmethod
    def first_name(
        name: str,
    ) -> str:
        
        # Return first name.

        parts = NameMatcher.normalize_name(
            name
        ).split()

        if not parts:

            return ""

        return parts[0]

    @staticmethod
    def last_name(
        name: str,
    ) -> str:
        
        # Return last name.

        parts = NameMatcher.normalize_name(
            name
        ).split()

        if not parts:

            return ""

        return parts[-1]