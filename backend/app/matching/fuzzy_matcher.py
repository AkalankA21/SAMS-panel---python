from __future__ import annotations

from rapidfuzz import fuzz

from app.utils.logger import logger


class FuzzyMatcher:
    
    # Performs fuzzy student matching.

    DEFAULT_THRESHOLD = 80.0

    @staticmethod
    def match(
        ocr_result: dict,
        student_records: list[dict],
        threshold: float = DEFAULT_THRESHOLD,
    ) -> dict | None:
        
        # Find the best fuzzy match.

        text = (
            ocr_result.get(
                "clean_text",
                ocr_result.get(
                    "text",
                    "",
                ),
            )
            .strip()
            .upper()
        )

        if not text:

            return None

        best_student = None

        best_score = 0.0

        for student in student_records:

            name = (
                student.get(
                    "name",
                    "",
                )
                .strip()
                .upper()
            )

            if not name:

                continue

            score = fuzz.ratio(
                text,
                name,
            )

            if score > best_score:

                best_score = score

                best_student = student

        if (
            best_student is None
            or
            best_score < threshold
        ):

            return None

        logger.info(
            "Fuzzy match: '%s' -> '%s' (%.2f%%)",
            text,
            best_student["name"],
            best_score,
        )

        return {

            "ocr_result": ocr_result,

            "student": best_student,

            "match_type": "Fuzzy",

            "match_score": round(
                best_score,
                2,
            ),

        }

    @staticmethod
    def similarity(
        text1: str,
        text2: str,
    ) -> float:
        
        # Calculate similarity between two strings.

        return round(

            fuzz.ratio(

                text1.upper(),

                text2.upper(),

            ),

            2,

        )

    @staticmethod
    def partial_similarity(
        text1: str,
        text2: str,
    ) -> float:
        
        # Partial similarity.

        return round(

            fuzz.partial_ratio(

                text1.upper(),

                text2.upper(),

            ),

            2,

        )

    @staticmethod
    def token_similarity(
        text1: str,
        text2: str,
    ) -> float:
        
        # Token sort similarity.

        return round(

            fuzz.token_sort_ratio(

                text1.upper(),

                text2.upper(),

            ),

            2,

        )

    @staticmethod
    def best_candidate(
        text: str,
        student_records: list[dict],
    ) -> tuple[dict | None, float]:
        
        # Return the closest student and score.

        text = text.strip().upper()

        best_student = None

        best_score = 0.0

        for student in student_records:

            score = fuzz.ratio(

                text,

                student.get(
                    "name",
                    "",
                ).upper(),

            )

            if score > best_score:

                best_score = score

                best_student = student

        return (

            best_student,

            round(
                best_score,
                2,
            ),

        )

    @staticmethod
    def top_matches(
        text: str,
        student_records: list[dict],
        limit: int = 5,
    ) -> list:
        
        # Return top candidate matches.

        text = text.strip().upper()

        candidates = []

        for student in student_records:

            score = fuzz.ratio(

                text,

                student.get(
                    "name",
                    "",
                ).upper(),

            )

            candidates.append(

                (

                    student,

                    round(
                        score,
                        2,
                    ),

                )

            )

        candidates.sort(

            key=lambda item: item[1],

            reverse=True,

        )

        return candidates[:limit]