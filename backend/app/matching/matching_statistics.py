from __future__ import annotations

from app.models.image_data import ImageData
from app.utils.logger import logger


class MatchingStatistics:
    
    # Calculate matching statistics.

    @staticmethod
    def calculate(
        image_data: ImageData,
    ) -> dict:
        
        # Calculate matching statistics.

        matches = image_data.matched_students or []
        unmatched = image_data.unmatched_results or []

        total_ocr = len(image_data.ocr_results or [])

        exact_matches = 0
        fuzzy_matches = 0
        partial_matches = 0
        manual_review = 0

        for match in matches:

            if isinstance(match, dict):
                match_type = match.get("match_type", "")
                match_score = match.get("match_score", 0.0)
            else:
                match_type = getattr(match, "match_type", "")
                match_score = getattr(match, "match_score", 0.0)

            if match_type in (
                "ID",
                "Name",
            ):

                exact_matches += 1

            elif match_type == "Fuzzy":

                fuzzy_matches += 1

            elif match_type in (
                "Partial ID",
                "Partial Name",
            ):

                partial_matches += 1

            if (

                match_score < 90

                or

                match_type == "Fuzzy"

            ):

                manual_review += 1

        accuracy = 0.0

        if total_ocr > 0:

            accuracy = round(

                len(matches)

                / total_ocr

                * 100,

                2,

            )

        statistics = {

            "Total OCR Results":
                total_ocr,

            "Matched Students":
                len(matches),

            "Unmatched Results":
                len(unmatched),

            "Exact Matches":
                exact_matches,

            "Partial Matches":
                partial_matches,

            "Fuzzy Matches":
                fuzzy_matches,

            "Manual Review":
                manual_review,

            "Matching Accuracy (%)":
                accuracy,

        }

        image_data.matching_statistics = (
            statistics
        )

        logger.info(
            "Matching statistics calculated."
        )

        return statistics

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        stats = MatchingStatistics.calculate(
            image_data
        )

        return (
            "\n"
            "========== Matching Statistics ==========\n"
            f"Total OCR Results      : {stats['Total OCR Results']}\n"
            f"Matched Students       : {stats['Matched Students']}\n"
            f"Unmatched Results      : {stats['Unmatched Results']}\n"
            f"Exact Matches          : {stats['Exact Matches']}\n"
            f"Partial Matches        : {stats['Partial Matches']}\n"
            f"Fuzzy Matches          : {stats['Fuzzy Matches']}\n"
            f"Manual Review          : {stats['Manual Review']}\n"
            f"Matching Accuracy (%)  : {stats['Matching Accuracy (%)']}\n"
        )

    @staticmethod
    def print(
        image_data: ImageData,
    ) -> None:
        
        # Print statistics.

        print(

            MatchingStatistics.summary(
                image_data
            )

        )

    @staticmethod
    def export(
        image_data: ImageData,
    ) -> dict:
        
        # Return cached statistics.

        if image_data.matching_statistics is None:

            return MatchingStatistics.calculate(
                image_data
            )

        return image_data.matching_statistics

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset statistics.

        image_data.matching_statistics = None

        logger.info(
            "Matching statistics reset."
        )