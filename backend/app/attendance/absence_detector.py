from __future__ import annotations

from app.utils.logger import logger


class AbsenceDetector:
    
    # Detect student absence.

    # Maximum confidence considered
    # as an empty signature cell.
    MIN_CONFIDENCE = 85.0

    # Maximum ink ratio for an empty cell.
    MAX_INK_RATIO = 0.02

    @staticmethod
    def is_absent(
        signature: dict,
    ) -> bool:
        
        # Determine whether a student is absent.

        if signature is None:

            return True

        if not signature.get("present", False) and not signature.get("review_required", False):

            logger.info(
                "Student marked ABSENT."
            )

            return True

        return False

    @staticmethod
    def confidence(
        signature: dict,
    ) -> float:
        
        # Return confidence.

        if signature is None:

            return 0.0

        return float(

            signature.get(
                "confidence",
                0.0,
            )

        )

    @staticmethod
    def ink_ratio(
        signature: dict,
    ) -> float:
        
        # Return ink ratio.

        if signature is None:

            return 0.0

        return float(

            signature.get(
                "ink_ratio",
                0.0,
            )

        )

    @staticmethod
    def reason(
        signature: dict,
    ) -> str:
        
        # Explain why the student is marked absent.

        if signature is None:

            return "No signature detected."

        if AbsenceDetector.is_absent(
            signature
        ):

            return (
                "Signature cell is empty."
            )

        confidence = signature.get(
            "confidence",
            0.0,
        )

        ink = signature.get(
            "ink_ratio",
            0.0,
        )

        if confidence < AbsenceDetector.MIN_CONFIDENCE:

            return (
                f"Low confidence ({confidence:.2f}%). "
                "Manual review required."
            )

        if ink > AbsenceDetector.MAX_INK_RATIO:

            return (
                f"Ink ratio ({ink:.4f}) "
                "indicates possible signature."
            )

        return "Attendance status uncertain."

    @staticmethod
    def requires_review(
        signature: dict,
    ) -> bool:
        
        # Determine whether manual review is required.

        if signature is None:

            return False

        return signature.get("review_required", False)

    @staticmethod
    def summary(
        signature: dict,
    ) -> dict:
        
        # Return absence summary.

        return {

            "Absent":
                AbsenceDetector.is_absent(
                    signature
                ),

            "Confidence":
                AbsenceDetector.confidence(
                    signature
                ),

            "Ink Ratio":
                AbsenceDetector.ink_ratio(
                    signature
                ),

            "Manual Review":
                AbsenceDetector.requires_review(
                    signature
                ),

            "Reason":
                AbsenceDetector.reason(
                    signature
                ),

        }