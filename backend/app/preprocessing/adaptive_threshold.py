from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.image_selector import ImageSelector
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class AdaptiveThreshold:
    
    # Adaptive Thresholding.

    DEFAULT_BLOCK_SIZE = 11
    DEFAULT_C = 2
    MAX_VALUE = 255

    @staticmethod
    def mean(
        image_data: ImageData,
        block_size: int = DEFAULT_BLOCK_SIZE,
        c: int = DEFAULT_C,
        inverse: bool = False,
    ) -> np.ndarray:

        try:

            logger.info(
                "Applying Adaptive Mean Threshold..."
            )

            source = ImageSelector.get_latest(image_data)

            if len(source.shape) == 3:
                source = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

            if block_size % 2 == 0:
                block_size += 1

            threshold_type = cv2.THRESH_BINARY

            if inverse:
                threshold_type = cv2.THRESH_BINARY_INV

            result = cv2.adaptiveThreshold(
                source,
                AdaptiveThreshold.MAX_VALUE,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                threshold_type,
                block_size,
                c,
            )

            image_data.adaptive_mean_image = result

            image_data.processing_history[
                "Adaptive Mean"
            ] = result

            image_data.set_stage(
                "Adaptive Mean Threshold"
            )

            return result

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def gaussian(
        image_data: ImageData,
        block_size: int = DEFAULT_BLOCK_SIZE,
        c: int = DEFAULT_C,
        inverse: bool = False,
    ) -> np.ndarray:

        try:

            logger.info(
                "Applying Adaptive Gaussian Threshold..."
            )

            source = ImageSelector.get_latest(image_data)

            if len(source.shape) == 3:
                source = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

            if block_size % 2 == 0:
                block_size += 1

            threshold_type = cv2.THRESH_BINARY

            if inverse:
                threshold_type = cv2.THRESH_BINARY_INV

            result = cv2.adaptiveThreshold(
                source,
                AdaptiveThreshold.MAX_VALUE,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                threshold_type,
                block_size,
                c,
            )

            image_data.adaptive_gaussian_image = result

            image_data.processing_history[
                "Adaptive Gaussian"
            ] = result

            image_data.set_stage(
                "Adaptive Gaussian Threshold"
            )

            return result

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def statistics(
        image: np.ndarray,
    ) -> dict:

        return ImageStatistics.basic(image)

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> dict:

        return {

            "Adaptive Mean":
                image_data.adaptive_mean_image,

            "Adaptive Gaussian":
                image_data.adaptive_gaussian_image,
        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ):

        image_data.adaptive_mean_image = None

        image_data.adaptive_gaussian_image = None

        image_data.processing_history.pop(
            "Adaptive Mean",
            None,
        )

        image_data.processing_history.pop(
            "Adaptive Gaussian",
            None,
        )

        logger.info(
            "Adaptive threshold reset."
        )