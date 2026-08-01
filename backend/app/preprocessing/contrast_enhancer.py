from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class ContrastEnhancer:
    
    # Performs contrast enhancement.

    MIN_CONTRAST = 0.1
    MAX_CONTRAST = 5.0

    @staticmethod
    def enhance(
        image_data: ImageData,
        alpha: float = 1.5,
    ) -> np.ndarray:
        
        # Enhance image contrast.

        try:

            logger.info(
                "Starting contrast enhancement."
            )

            if image_data is None:

                raise ImageProcessingError(
                    "ImageData cannot be None."
                )

            if image_data.grayscale_image is None:

                raise ImageProcessingError(
                    "Grayscale image not found."
                )

            alpha = max(
                ContrastEnhancer.MIN_CONTRAST,
                min(
                    ContrastEnhancer.MAX_CONTRAST,
                    alpha,
                ),
            )

            enhanced = cv2.convertScaleAbs(
                image_data.grayscale_image,
                alpha=alpha,
                beta=0,
            )

            image_data.contrast_image = enhanced

            image_data.processing_history[
                "Contrast"
            ] = enhanced

            image_data.set_stage(
                "Contrast Enhancement"
            )

            logger.info(
                "Contrast enhancement completed."
            )

            return enhanced

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Contrast enhancement failed: {ex}"
            ) from ex

    @staticmethod
    def automatic(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Automatically improve contrast using image standard deviation.

        try:

            if image_data.grayscale_image is None:

                raise ImageProcessingError(
                    "Grayscale image not found."
                )

            gray = image_data.grayscale_image

            std = gray.std()

            if std < 30:

                alpha = 2.0

            elif std < 50:

                alpha = 1.5

            else:

                alpha = 1.2

            return ContrastEnhancer.enhance(
                image_data,
                alpha,
            )

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return contrast statistics.

        if image_data.contrast_image is None:

            raise ImageProcessingError(
                "Contrast image not found."
            )

        image = image_data.contrast_image

        return {

            "Minimum":
                int(image.min()),

            "Maximum":
                int(image.max()),

            "Mean":
                round(
                    float(image.mean()),
                    2,
                ),

            "Standard Deviation":
                round(
                    float(image.std()),
                    2,
                ),

            "Contrast Alpha":
                "Enhanced",
        }

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:
        
        # Compare grayscale and enhanced image.

        if image_data.contrast_image is None:

            raise ImageProcessingError(
                "Contrast image not available."
            )

        original_std = float(
            image_data.grayscale_image.std()
        )

        enhanced_std = float(
            image_data.contrast_image.std()
        )

        return {

            "Original Std":
                round(original_std, 2),

            "Enhanced Std":
                round(enhanced_std, 2),

            "Difference":
                round(
                    enhanced_std - original_std,
                    2,
                ),
        }

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return enhanced image.

        if image_data.contrast_image is None:

            return ContrastEnhancer.enhance(
                image_data
            )

        return image_data.contrast_image.copy()

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Remove contrast enhancement.

        image_data.contrast_image = None

        image_data.processing_history.pop(
            "Contrast",
            None,
        )

        logger.info(
            "Contrast enhancement reset."
        )