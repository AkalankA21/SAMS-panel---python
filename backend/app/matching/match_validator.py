from __future__ import annotations

from app.utils.logger import logger


class MatchValidator:

    # Validate student matches.

    MIN_CONFIDENCE = 80.0

    @staticmethod
    def validate(
        matches: list[dict],
        minimum_score: float = MIN_CONFIDENCE,
    ) -> tuple[list[dict], list[dict]]:
        
        # Validate all matches.

        valid_matches = []

        invalid_matches = []

        used_student_ids = set()

        for match in matches:

            if not MatchValidator.is_valid(
                match,
                used_student_ids,
                minimum_score,
            ):

                invalid_matches.append(
                    match
                )

                continue

            student = match["student"]

            student_id = student.get(
                "student_id",
                "",
            )

            used_student_ids.add(
                student_id
            )

            valid_matches.append(
                match
            )

        logger.info(
            "%d valid matches, %d invalid matches.",
            len(valid_matches),
            len(invalid_matches),
        )

        return (

            valid_matches,

            invalid_matches,

        )

    @staticmethod
    def is_valid(
        match: dict,
        used_student_ids: set,
        minimum_score: float,
    ) -> bool:
        
        # Validate a single match.

        if match is None:

            return False

        if "student" not in match:

            return False

        if "match_score" not in match:

            return False

        score = float(
            match["match_score"]
        )

        if score < minimum_score:

            return False

        student = match["student"]

        student_id = student.get(
            "student_id",
            "",
        )

        if student_id in used_student_ids:

            logger.warning(
                "Duplicate student ID: %s",
                student_id,
            )

            return False

        return True

    @staticmethod
    def duplicate_students(
        matches: list[dict],
    ) -> list[dict]:
        
        # Return duplicated student matches.

        duplicates = []

        seen = set()

        for match in matches:

            student_id = match["student"].get(
                "student_id",
                "",
            )

            if student_id in seen:

                duplicates.append(
                    match
                )

            else:

                seen.add(
                    student_id
                )

        return duplicates

    @staticmethod
    def low_confidence(
        matches: list[dict],
        threshold: float = MIN_CONFIDENCE,
    ) -> list[dict]:
        
        # Return low-confidence matches.

        return [

            match

            for match in matches

            if match.get(
                "match_score",
                0.0,
            ) < threshold

        ]

    @staticmethod
    def manual_review(
        matches: list[dict],
    ) -> list[dict]:
        
        # Return matches requiring review.

        review = []

        for match in matches:

            if (

                match.get(
                    "match_type"
                ) == "Fuzzy"

                or

                match.get(
                    "match_score",
                    0,
                ) < 90

            ):

                review.append(
                    match
                )

        return review

    @staticmethod
    def unmatched(
        ocr_results: list[dict],
        matches: list[dict],
    ) -> list[dict]:
        
        # Return OCR results that were not matched.

        matched_ids = {

            id(
                match["ocr_result"]
            )

            for match in matches

        }

        return [

            result

            for result in ocr_results

            if id(result)

            not in matched_ids

        ]

    @staticmethod
    def summary(
        matches: list[dict],
    ) -> dict:
        
        # Return validation summary.

        duplicates = MatchValidator.duplicate_students(
            matches
        )

        review = MatchValidator.manual_review(
            matches
        )

        low = MatchValidator.low_confidence(
            matches
        )

        return {

            "Total Matches":
                len(matches),

            "Duplicate Matches":
                len(duplicates),

            "Low Confidence":
                len(low),

            "Manual Review":
                len(review),

            "Validated":
                len(matches)
                - len(duplicates)
                - len(low),

        }