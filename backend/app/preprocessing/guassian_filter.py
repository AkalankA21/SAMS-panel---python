"""
Gaussian Filter Module.

This module provides functionality to apply Gaussian Blur spatial filtering.

Academic Note (Gaussian Convolution Kernel):
The Gaussian filter is a linear spatial low-pass filter that convolves an image with a 2D Gaussian kernel.
The continuous 2D Gaussian distribution function is given by:

    G(x, y) = (1 / (2 * pi * sigma^2)) * exp( - (x^2 + y^2) / (2 * sigma^2) )

Where:
- x, y are spatial distances from the kernel center origin (0, 0).
- sigma is the Gaussian standard deviation controlling the width of the bell curve (blur intensity).

Key Characteristics:
1. Low-Pass Filtering: Attenuates high-frequency noise while smoothing low-frequency background details.
2. Isotropic Smoothness: Weights decrease smoothly away from the center pixel, suppressing Gaussian noise.
3. Separation: The 2D Gaussian filter is separable into two 1D Gaussian operations, allowing O(N*K) fast computation.

Kernel Requirement:
OpenCV requires kernel_size dimensions to be positive odd integers, e.g., (3, 3), (5, 5), (7, 7).
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class GaussianFilter:
    """
    Class providing Gaussian blur spatial filtering operations.
    """

    @staticmethod
    def apply(
        image: np.ndarray,
        kernel_size: tuple[int, int] = (5, 5),
        sigma_x: float = 0.0,
        sigma_y: float = 0.0
    ) -> np.ndarray:
        """
        Applies a Gaussian Blur filter to an image.

        :param image: Input image array (Grayscale or BGR).
        :param kernel_size: Tuple (width, height) specifying kernel dimensions. Both must be positive odd numbers.
        :param sigma_x: Gaussian kernel standard deviation in X direction. If 0, calculated from kernel size.
        :param sigma_y: Gaussian kernel standard deviation in Y direction. If 0, defaults to sigma_x.
        :return: Gaussian-blurred uint8 image.
        :raises ImageProcessingError: If image is invalid or kernel dimensions are not odd/positive.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("GaussianFilter: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for Gaussian filtering.")

        kw, kh = kernel_size
        if kw <= 0 or kh <= 0 or kw % 2 == 0 or kh % 2 == 0:
            logger.error(f"GaussianFilter: Invalid kernel dimensions {kernel_size}. Must be positive odd integers.")
            raise ImageProcessingError(f"Kernel dimensions must be positive odd integers (received {kernel_size}).")

        try:
            logger.info(f"GaussianFilter: Applying cv2.GaussianBlur with kernel_size={kernel_size}, sigma_x={sigma_x}.")
            # cv2.GaussianBlur applies 2D discrete Gaussian kernel convolution
            blurred_image = cv2.GaussianBlur(
                image,
                ksize=kernel_size,
                sigmaX=sigma_x,
                sigmaY=sigma_y
            )
            return blurred_image
        except Exception as ex:
            logger.error(f"Gaussian filtering failed: {ex}")
            raise ImageProcessingError(f"Gaussian filter error: {ex}") from ex
