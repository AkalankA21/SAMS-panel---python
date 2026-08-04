from __future__ import annotations

from app.models.image_data import ImageData
from app.matching.id_matcher import IDMatcher
from app.matching.name_matcher import NameMatcher
from app.matching.fuzzy_matcher import FuzzyMatcher
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class StudentMatcher:
    
    # Main student matching class.

    @staticmethod
    def match(
        image_data: ImageData,
        student_records: list[dict],
        fuzzy_threshold: float = 80.0,
    ) -> list:
        
        # Match OCR results against student records.

        if image_data.ocr_results is None:

            raise ImageProcessingError(
                "OCR results unavailable."
            )

        logger.info(
            "Starting student matching..."
        )

        matches = []

        unmatched = []

        for result in image_data.ocr_results:

            matched = None

            # --------------------------
            # 1. Match by Student ID
            # --------------------------

            matched = IDMatcher.match(
                result,
                student_records,
            )

            # --------------------------
            # 2. Match by Name
            # --------------------------

            if matched is None:

                matched = NameMatcher.match(
                    result,
                    student_records,
                )

            # --------------------------
            # 3. Fuzzy Match
            # --------------------------

            if matched is None:

                matched = FuzzyMatcher.match(
                    result,
                    student_records,
                    threshold=fuzzy_threshold,
                )

            if matched is not None:

                matches.append(matched)

            else:

                unmatched.append(result)

        image_data.matched_students = matches

        image_data.unmatched_results = unmatched

        image_data.processing_history[
            "Student Matching"
        ] = len(matches)

        image_data.set_stage(
            "Student Matching"
        )

        logger.info(
            "%d students matched.",
            len(matches),
        )

        logger.info(
            "%d unmatched OCR results.",
            len(unmatched),
        )

        return matches

    @staticmethod
    def matched(
        image_data: ImageData,
    ) -> list:
        
        # Return matched students.

        return image_data.matched_students or []

    @staticmethod
    def unmatched(
        image_data: ImageData,
    ) -> list:
        
        # Return unmatched OCR results.

        return image_data.unmatched_results or []

    @staticmethod
    def total_matches(
        image_data: ImageData,
    ) -> int:
        
        # Number of matched students.

        if image_data.matched_students is None:

            return 0

        return len(
            image_data.matched_students
        )

    @staticmethod
    def total_unmatched(
        image_data: ImageData,
    ) -> int:
        
        # Number of unmatched OCR results.

        if image_data.unmatched_results is None:

            return 0

        return len(
            image_data.unmatched_results
        )

    @staticmethod
    def has_matches(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether any matches exist.

        return StudentMatcher.total_matches(
            image_data
        ) > 0

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset matching results.

        image_data.matched_students = None

        image_data.unmatched_results = None

        image_data.processing_history.pop(
            "Student Matching",
            None,
        )

        logger.info(
            "Student matching reset."
        )