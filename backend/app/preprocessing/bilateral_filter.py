"""
Bilateral Filter Module.

This module provides functionality for edge-preserving bilateral filtering.

Academic Note (Bilateral Filter Theory & Formulation):
While traditional Gaussian filtering smooths noise by averaging neighboring pixels based strictly on spatial distance,
it also blurs sharp structural edges. The Bilateral Filter overcomes this limitation by taking into account
BOTH spatial closeness AND photometric (color/intensity) similarity:

    BF[I]_p = (1 / W_p) * sum_{q in S} G_{sigma_s}(||p - q||) * G_{sigma_r}(|I_p - I_q|) * I_q

Where:
1. Domain Gaussian (Spatial Kernel G_{sigma_s}): Weights pixels higher if they are spatially close to the center pixel p.
2. Range Gaussian (Photometric Kernel G_{sigma_r}): Weights pixels higher if their intensity/color difference is small.
   If pixel q has a very different intensity from center pixel p (i.e. across an edge), G_{sigma_r} approaches 0,
   preventing edge pixels from blending across the boundary!

Parameters in OpenCV:
- d: Diameter of pixel neighborhood used during filtering. If d <= 0, computed from sigma_space.
- sigmaColor: Filter sigma in intensity/color space. Larger values mean broader color variations blend together.
- sigmaSpace: Filter sigma in coordinate space. Larger values mean farther pixels influence each other.

Importance for SAMS Attendance Processing:
Preserves sharp, crisp handwritten marks, printed text, and grid borders while smoothing paper texture noise and shadows.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class BilateralFilter:
    """
    Class providing edge-preserving bilateral filtering operations.
    """

    @staticmethod
    def apply(
        image: np.ndarray,
        d: int = 9,
        sigma_color: float = 75.0,
        sigma_space: float = 75.0
    ) -> np.ndarray:
        """
        Applies a Bilateral Filter to an image for edge-preserving smoothing.

        :param image: Input image array (Grayscale or 3-channel BGR).
        :param d: Pixel neighborhood diameter (e.g. 5, 9). Small values (5) for real-time, 9 for offline filters.
        :param sigma_color: Filter sigma in color space. Higher values allow larger intensity differences to be smoothed.
        :param sigma_space: Filter sigma in spatial coordinate space. Higher values extend spatial reach.
        :return: Edge-preserved filtered uint8 image.
        :raises ImageProcessingError: If image is invalid.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("BilateralFilter: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for bilateral filtering.")

        try:
            logger.info(f"BilateralFilter: Applying cv2.bilateralFilter (d={d}, sigma_color={sigma_color}, sigma_space={sigma_space}).")
            # cv2.bilateralFilter processes spatial and range kernels concurrently
            filtered_image = cv2.bilateralFilter(
                image,
                d=d,
                sigmaColor=sigma_color,
                sigmaSpace=sigma_space
            )
            return filtered_image
        except Exception as ex:
            logger.error(f"Bilateral filtering failed: {ex}")
            raise ImageProcessingError(f"Bilateral filter error: {ex}") from ex
