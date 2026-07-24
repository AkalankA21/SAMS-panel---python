"""
Median Filter Module.

This module provides functionality to apply Median Blur filtering to an image.

Academic Note (Order-Statistic Filtering):
The Median Filter is a non-linear digital filtering technique. Unlike linear filters (e.g., Mean or Gaussian),
which replace a target pixel with a weighted linear combination of neighboring intensities,
the Median Filter replaces the center pixel value with the MEDIAN value of all pixels inside the sliding kernel window:

    g(x, y) = median { f(x + k, y + l) | (k, l) in W }

Where W is a rectangular window (e.g., 3x3, 5x5) centered at (x, y).

Key Advantages for SAMS:
1. Impulse Noise Removal: Highly effective against "salt-and-pepper" noise caused by camera sensor defects or scanner dust.
2. Edge Preservation: Because the median value must be an existing intensity from the neighborhood (or middle rank),
   it does not create synthetic intermediate values across strong boundaries, preserving sharp gridlines and text characters.

Kernel Requirement:
OpenCV requires kernel_size to be an odd positive integer greater than 1 (e.g., 3, 5, 7).
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class MedianFilter:
    """
    Class providing median blur filtering operations.
    """

    @staticmethod
    def apply(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Applies a Median Blur filter to the input image.

        :param image: Input image array (Grayscale or BGR).
        :param kernel_size: Aperture linear size; must be an odd integer greater than 1 (e.g., 3, 5, 7).
        :return: Median-filtered uint8 image.
        :raises ImageProcessingError: If image is invalid or kernel_size is not odd/greater than 1.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("MedianFilter: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for median filtering.")

        if kernel_size <= 1 or kernel_size % 2 == 0:
            logger.error(f"MedianFilter: Invalid kernel_size {kernel_size}. Must be an odd integer > 1.")
            raise ImageProcessingError(f"Kernel size must be an odd integer greater than 1 (received {kernel_size}).")

        try:
            logger.info(f"MedianFilter: Applying median blur filter with kernel_size={kernel_size}.")
            # cv2.medianBlur applies 2D median filtering across spatial dimensions
            filtered_image = cv2.medianBlur(image, ksize=kernel_size)
            return filtered_image
        except Exception as ex:
            logger.error(f"Median filtering failed: {ex}")
            raise ImageProcessingError(f"Median filter error: {ex}") from ex
