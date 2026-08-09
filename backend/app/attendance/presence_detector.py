from __future__ import annotations

from app.utils.logger import logger


class PresenceDetector:
    
    # Detect student presence.

    # Minimum confidence required
    MIN_CONFIDENCE = 85.0

    # Minimum ink ratio required
    MIN_INK_RATIO = 0.08

    @staticmethod
    def is_present(
        signature: dict,
    ) -> bool:
        
        # Determine whether a student is present.

        if signature is None:

            return False

        if signature.get("present", False) and not signature.get("review_required", False):

            logger.info(
                "Student marked PRESENT."
            )

            return True

        return False

    @staticmethod
    def confidence(
        signature: dict,
    ) -> float:
        
        # Return detection confidence.

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
        
        # Explain why the student is marked present or not.

        if signature is None:

            return "No signature data."

        if PresenceDetector.is_present(
            signature
        ):

            return (
                "Signature detected with "
                "high confidence."
            )

        confidence = signature.get(
            "confidence",
            0.0,
        )

        ink = signature.get(
            "ink_ratio",
            0.0,
        )

        if confidence < PresenceDetector.MIN_CONFIDENCE:

            return (
                f"Low confidence ({confidence:.2f}%)."
            )

        if ink < PresenceDetector.MIN_INK_RATIO:

            return (
                f"Insufficient ink ratio ({ink:.4f})."
            )

        return "Presence not confirmed."

    @staticmethod
    def summary(
        signature: dict,
    ) -> dict:
        
        # Return presence summary.

        return {

            "Present":
                PresenceDetector.is_present(
                    signature
                ),

            "Confidence":
                PresenceDetector.confidence(
                    signature
                ),

            "Ink Ratio":
                PresenceDetector.ink_ratio(
                    signature
                ),

            "Reason":
                PresenceDetector.reason(
                    signature
                ),

        }