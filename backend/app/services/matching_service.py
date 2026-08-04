from __future__ import annotations

from app.models.image_data import ImageData

from app.matching.student_matcher import (
    StudentMatcher,
)
from app.matching.match_validator import (
    MatchValidator,
)
from app.matching.match_result import (
    MatchResult,
)
from app.matching.matching_statistics import (
    MatchingStatistics,
)

from app.utils.exceptions import (
    ImageProcessingError,
)
from app.utils.logger import logger


class MatchingService:
    
    # Student matching service.

    @staticmethod
    def process(
        image_data: ImageData,
        student_records: list[dict] | None = None,
        fuzzy_threshold: float = 80.0,
    ) -> list[MatchResult]:
        
        # Execute the complete matching pipeline.

        logger.info(
            "Starting student matching pipeline..."
        )

        record_source = (
            student_records
            if student_records is not None
            else image_data.student_records
            or []
        )

        if not record_source:
            raise ImageProcessingError("Matching failed: Student records list from XML is empty.")

        raw_matches = StudentMatcher.match(

            image_data,

            record_source,

            fuzzy_threshold,

        )

        valid_matches, invalid_matches = (

            MatchValidator.validate(
                raw_matches
            )

        )

        image_data.invalid_matches = (
            invalid_matches
        )

        results = [

            MatchResult.from_match(
                match
            )

            for match in valid_matches

        ]

        image_data.matched_students = (
            results
        )

        MatchingStatistics.calculate(
            image_data
        )

        logger.info(
            "Student matching pipeline completed."
        )

        return results

    @staticmethod
    def get_matches(
        image_data: ImageData,
    ) -> list[MatchResult]:
        
        # Return matched students.

        return (
            image_data.matched_students
            or []
        )

    @staticmethod
    def get_invalid(
        image_data: ImageData,
    ) -> list:
        
        # Return invalid matches.

        return getattr(

            image_data,

            "invalid_matches",

            [],

        )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return matching statistics.

        return MatchingStatistics.calculate(
            image_data
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        return MatchingStatistics.summary(
            image_data
        )

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Number of matched students.

        return len(

            image_data.matched_students

            or []

        )

    @staticmethod
    def has_matches(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether any students have been matched.

        return (
            MatchingService.count(
                image_data
            ) > 0
        )

    @staticmethod
    def get_match(
        image_data: ImageData,
        index: int,
    ) -> MatchResult:
        
        # Return a single match.

        matches = (
            image_data.matched_students
            or []
        )

        if not matches:

            raise ImageProcessingError(
                "No matched students."
            )

        if (

            index < 0

            or

            index >= len(matches)

        ):

            raise IndexError(
                "Match index out of range."
            )

        return matches[index]

    @staticmethod
    def review_required(
        image_data: ImageData,
    ) -> list[MatchResult]:
        
        # Return matches that require manual review.

        matches = (
            image_data.matched_students
            or []
        )

        return [

            match

            for match in matches

            if match.requires_review

        ]

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset matching data.

        StudentMatcher.reset(
            image_data
        )

        MatchingStatistics.reset(
            image_data
        )

        image_data.invalid_matches = []

        logger.info(
            "Matching service reset."
        )

    @staticmethod
    def validate_pipeline(
        image_data: ImageData,
    ) -> bool:
        
        # Verify matching pipeline output.

        return (

            image_data.matched_students
            is not None

            and

            len(
                image_data.matched_students
            ) > 0

        )