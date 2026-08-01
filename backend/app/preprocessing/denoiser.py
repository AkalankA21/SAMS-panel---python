from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.image_selector import ImageSelector
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class Denoiser:
    
    # Non-local Means Denoising.

    DEFAULT_H = 10
    DEFAULT_TEMPLATE = 7
    DEFAULT_SEARCH = 21

    @staticmethod
    def apply(
        image_data: ImageData,
        h: int = DEFAULT_H,
        template_window: int = DEFAULT_TEMPLATE,
        search_window: int = DEFAULT_SEARCH,
    ) -> np.ndarray:

        try:

            logger.info(
                "Applying Non-Local Means Denoising..."
            )

            source = ImageSelector.get_latest(
                image_data
            )

            result = cv2.fastNlMeansDenoising(
                src=source,
                h=h,
                templateWindowSize=template_window,
                searchWindowSize=search_window,
            )

            image_data.denoised_image = result

            image_data.processing_history[
                "Denoised"
            ] = result

            image_data.set_stage(
                "Noise Removal"
            )

            logger.info(
                "Denoising completed."
            )

            return result

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Denoising failed: {ex}"
            ) from ex

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:

        if image_data.denoised_image is None:

            raise ImageProcessingError(
                "Denoised image not available."
            )

        return ImageStatistics.basic(
            image_data.denoised_image
        )

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:

        if image_data.denoised_image is None:

            raise ImageProcessingError(
                "Denoised image not available."
            )

        source = ImageSelector.get_latest(
            image_data
        )

        return ImageStatistics.compare(
            source,
            image_data.denoised_image,
        )

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:

        if image_data.denoised_image is None:

            return Denoiser.apply(
                image_data
            )

        return image_data.denoised_image.copy()

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:

        image_data.denoised_image = None

        image_data.processing_history.pop(
            "Denoised",
            None,
        )

        logger.info(
            "Denoiser reset."
        )