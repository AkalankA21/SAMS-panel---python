from __future__ import annotations

import csv
from pathlib import Path

from app.models.image_data import ImageData
from app.matching.match_result import MatchResult
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class StudentTable:
    
    # Display and export matched students.

    @staticmethod
    def print(
        image_data: ImageData,
    ) -> None:
        
        # Print matched students.

        matches = image_data.matched_students or []

        if not matches:

            print()
            print("No matched students available.")
            return

        print()

        print("=" * 130)

        print(
            f"{'Student ID':<15}"
            f"{'Student Name':<30}"
            f"{'OCR Text':<25}"
            f"{'Match Type':<15}"
            f"{'Score':<10}"
            f"{'OCR Conf.':<12}"
            f"{'Review'}"
        )

        print("=" * 130)

        for match in matches:

            print(

                f"{match.student_id:<15}"

                f"{match.student_name:<30}"

                f"{match.cleaned_text:<25}"

                f"{match.match_type:<15}"

                f"{match.match_score:<10.2f}"

                f"{match.confidence:<12.2f}"

                f"{'Yes' if match.requires_review else 'No'}"

            )

        print("=" * 130)

    @staticmethod
    def export_csv(
        image_data: ImageData,
        output_file: str | Path,
    ) -> None:
        
        # Export matched students to CSV.

        matches = image_data.matched_students or []

        if not matches:

            logger.info("No matched students available to export.")
            return

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
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

                    "Row",

                    "Column",

                    "OCR Text",

                    "Cleaned Text",

                    "Match Type",

                    "Match Score",

                    "OCR Confidence",

                    "Requires Review",

                ]

            )

            for match in matches:

                writer.writerow(

                    [

                        match.student_id,

                        match.student_name,

                        match.row,

                        match.column,

                        match.ocr_text,

                        match.cleaned_text,

                        match.match_type,

                        match.match_score,

                        match.confidence,

                        match.requires_review,

                    ]

                )

        logger.info(
            "Student table exported to %s",
            output_file,
        )

    @staticmethod
    def total_students(
        image_data: ImageData,
    ) -> int:
        
        # Return total matched students.

        return len(
            image_data.matched_students
            or []
        )

    @staticmethod
    def review_students(
        image_data: ImageData,
    ) -> list[MatchResult]:
        
        # Return students requiring review.

        return [

            match

            for match in (
                image_data.matched_students
                or []
            )

            if match.requires_review

        ]

    @staticmethod
    def exact_matches(
        image_data: ImageData,
    ) -> list[MatchResult]:
        
        # Return exact matches.

        return [

            match

            for match in (
                image_data.matched_students
                or []
            )

            if match.is_exact

        ]

    @staticmethod
    def fuzzy_matches(
        image_data: ImageData,
    ) -> list[MatchResult]:
        
        # Return fuzzy matches.

        return [

            match

            for match in (
                image_data.matched_students
                or []
            )

            if match.is_fuzzy

        ]

    @staticmethod
    def partial_matches(
        image_data: ImageData,
    ) -> list[MatchResult]:
        
        # Return partial matches.

        return [

            match

            for match in (
                image_data.matched_students
                or []
            )

            if match.is_partial

        ]

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> dict:
        
        # Return table summary.

        return {

            "Total Students":

                StudentTable.total_students(
                    image_data
                ),

            "Exact Matches":

                len(
                    StudentTable.exact_matches(
                        image_data
                    )
                ),

            "Partial Matches":

                len(
                    StudentTable.partial_matches(
                        image_data
                    )
                ),

            "Fuzzy Matches":

                len(
                    StudentTable.fuzzy_matches(
                        image_data
                    )
                ),

            "Needs Review":

                len(
                    StudentTable.review_students(
                        image_data
                    )
                ),

        }

    @staticmethod
    def print_summary(
        image_data: ImageData,
    ) -> None:
        
        # Print summary.

        summary = StudentTable.summary(
            image_data
        )

        print()

        print("=" * 50)

        print("STUDENT TABLE SUMMARY")

        print("=" * 50)

        for key, value in summary.items():

            print(

                f"{key:<20}: {value}"

            )

        print("=" * 50)