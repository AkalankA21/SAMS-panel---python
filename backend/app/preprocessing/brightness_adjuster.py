from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class BrightnessAdjuster:
    
    # Performs brightness adjustment on grayscale images.

    MIN_BRIGHTNESS = -255
    MAX_BRIGHTNESS = 255

    @staticmethod
    def adjust(
        image_data: ImageData,
        beta: int = 30,
    ) -> np.ndarray:
        
        # Increase or decrease image brightness.

        try:

            logger.info("Brightness adjustment started.")

            if image_data is None:
                raise ImageProcessingError(
                    "ImageData cannot be None."
                )

            if image_data.grayscale_image is None:
                raise ImageProcessingError(
                    "Grayscale image not found."
                )

            beta = max(
                BrightnessAdjuster.MIN_BRIGHTNESS,
                min(
                    BrightnessAdjuster.MAX_BRIGHTNESS,
                    beta,
                ),
            )

            adjusted = cv2.convertScaleAbs(
                image_data.grayscale_image,
                alpha=1.0,
                beta=beta,
            )

            image_data.brightness_image = adjusted

            image_data.processing_history[
                "Brightness"
            ] = adjusted

            image_data.set_stage(
                "Brightness Adjustment"
            )

            logger.info(
                "Brightness adjustment completed."
            )

            return adjusted

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Brightness adjustment failed: {ex}"
            ) from ex

    @staticmethod
    def automatic(
        image_data: ImageData,
        target_mean: int = 130,
    ) -> np.ndarray:
        
        # Automatically adjust brightness so the image mean approaches the target value.

        try:

            if image_data.grayscale_image is None:

                raise ImageProcessingError(
                    "Grayscale image not found."
                )

            gray = image_data.grayscale_image

            current_mean = gray.mean()

            beta = int(
                target_mean - current_mean
            )

            return BrightnessAdjuster.adjust(
                image_data,
                beta,
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
        
        # Return brightness statistics.

        if image_data.brightness_image is None:

            raise ImageProcessingError(
                "Brightness image not available."
            )

        image = image_data.brightness_image

        return {

            "Minimum": int(image.min()),

            "Maximum": int(image.max()),

            "Mean": round(
                float(image.mean()),
                2,
            ),

            "Standard Deviation": round(
                float(image.std()),
                2,
            ),
        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Remove brightness adjustment.

        image_data.brightness_image = None

        image_data.processing_history.pop(
            "Brightness",
            None,
        )

        logger.info(
            "Brightness adjustment reset."
        )

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:
        
        # Compare grayscale and brightness images.

        if image_data.grayscale_image is None:

            raise ImageProcessingError(
                "Grayscale image missing."
            )

        if image_data.brightness_image is None:

            raise ImageProcessingError(
                "Brightness image missing."
            )

        return {

            "Original Mean": round(
                float(
                    image_data.grayscale_image.mean()
                ),
                2,
            ),

            "Adjusted Mean": round(
                float(
                    image_data.brightness_image.mean()
                ),
                2,
            ),

            "Difference": round(
                float(
                    image_data.brightness_image.mean()
                    - image_data.grayscale_image.mean()
                ),
                2,
            ),
        }

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return brightness image for GUI preview.

        if image_data.brightness_image is None:

            return BrightnessAdjuster.adjust(
                image_data
            )

        return image_data.brightness_image.copy()