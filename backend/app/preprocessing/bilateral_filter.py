from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.image_selector import ImageSelector
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class BilateralFilter:
    
    # Bilateral filtering.

    DEFAULT_DIAMETER = 9
    DEFAULT_SIGMA_COLOR = 75
    DEFAULT_SIGMA_SPACE = 75

    @staticmethod
    def apply(
        image_data: ImageData,
        diameter: int = DEFAULT_DIAMETER,
        sigma_color: float = DEFAULT_SIGMA_COLOR,
        sigma_space: float = DEFAULT_SIGMA_SPACE,
    ) -> np.ndarray:

        try:

            logger.info(
                "Applying bilateral filter..."
            )

            source = ImageSelector.get_latest(
                image_data
            )

            filtered = cv2.bilateralFilter(
                src=source,
                d=diameter,
                sigmaColor=sigma_color,
                sigmaSpace=sigma_space,
            )

            image_data.bilateral_image = filtered

            image_data.processing_history[
                "Bilateral"
            ] = filtered

            image_data.set_stage(
                "Bilateral Filtering"
            )

            logger.info(
                "Bilateral filtering completed."
            )

            return filtered

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Bilateral filtering failed: {ex}"
            ) from ex

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:

        if image_data.bilateral_image is None:

            raise ImageProcessingError(
                "Bilateral image not available."
            )

        return ImageStatistics.basic(
            image_data.bilateral_image
        )

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:

        if image_data.bilateral_image is None:

            raise ImageProcessingError(
                "Bilateral image not found."
            )

        source = ImageSelector.get_latest(
            image_data
        )

        return ImageStatistics.compare(
            source,
            image_data.bilateral_image,
        )

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:

        if image_data.bilateral_image is None:

            return BilateralFilter.apply(
                image_data
            )

        return image_data.bilateral_image.copy()

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:

        image_data.bilateral_image = None

        image_data.processing_history.pop(
            "Bilateral",
            None,
        )

        logger.info(
            "Bilateral filter reset."
        )