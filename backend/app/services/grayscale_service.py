"""
Grayscale Service Module.

This service acts as a high-level manager and coordinator for all grayscale conversion
tasks, image dimension validation, and channel intensity analysis in the SAMS pipeline.
"""

from __future__ import annotations

import numpy as np

from app.preprocessing.grayscale_converter import GrayscaleConverter
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class GrayscaleService:
    """
    Service class to handle and coordinate grayscale conversion operations and statistics.
    """

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        """
        Converts an image to grayscale using GrayscaleConverter.

        :param image: Input image array.
        :return: 1-channel grayscale image array.
        """
        logger.info("GrayscaleService: Processing to_grayscale request.")
        return GrayscaleConverter.convert(image)

    @staticmethod
    def ensure_grayscale(image: np.ndarray) -> np.ndarray:
        """
        Ensures that the output image is guaranteed to be 1-channel grayscale.
        If the image is already grayscale, returns it directly without reprocessing.

        :param image: Input image array.
        :return: 1-channel grayscale image array.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ImageProcessingError("Invalid image array provided to GrayscaleService.")

        if len(image.shape) == 2:
            logger.info("GrayscaleService: Image is already 1-channel grayscale.")
            return image.copy()

        logger.info("GrayscaleService: Converting 3-channel image to grayscale.")
        return GrayscaleConverter.convert(image)

    @staticmethod
    def is_grayscale(image: np.ndarray) -> bool:
        """
        Checks whether an image is single-channel grayscale or a 3-channel grayscale equivalent.

        :param image: Input image array.
        :return: True if single channel or channels are identical, False otherwise.
        """
        if image is None or not isinstance(image, np.ndarray):
            return False

        if len(image.shape) == 2:
            return True

        if len(image.shape) == 3 and image.shape[2] == 1:
            return True

        if len(image.shape) == 3 and image.shape[2] == 3:
            b, g, r = image[:, :, 0], image[:, :, 1], image[:, :, 2]
            return bool(np.array_equal(b, g) and np.array_equal(g, r))

        return False

    @staticmethod
    def get_grayscale_stats(image: np.ndarray) -> dict[str, float]:
        """
        Calculates intensity statistics for a grayscale image.

        :param image: Input image array (converted to grayscale if necessary).
        :return: Dictionary containing mean, std_dev, min, max, and median pixel intensities.
        """
        gray = GrayscaleService.ensure_grayscale(image)

        stats = {
            "mean_intensity": float(np.mean(gray)),
            "std_intensity": float(np.std(gray)),
            "min_intensity": float(np.min(gray)),
            "max_intensity": float(np.max(gray)),
            "median_intensity": float(np.median(gray)),
        }
        logger.info(f"GrayscaleService: Intensity stats calculated -> {stats}")
        return stats
