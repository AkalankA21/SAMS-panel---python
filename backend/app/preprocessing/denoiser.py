"""
Denoiser Module.

This module provides functionality to apply Fast Non-Local Means Denoising.

Academic Note (Non-Local Means Denoising):
Traditional spatial filters (e.g., Gaussian, Median) assume noise can be removed by averaging pixel intensities
within a local neighborhood around a target pixel.
In contrast, Non-Local Means (NL-Means) Denoising operates on a non-local principle:
It searches a larger region of the image for patches that are structurally similar to the patch centered at the target pixel.

Algorithm Steps:
1. Template Window (e.g., 7x7): A small local patch around pixel p.
2. Search Window (e.g., 21x21): A larger surrounding area searched for matching patches.
3. Patch Distance Weighting: Computes Euclidean distance between template window and candidate windows.
   The target pixel is restored as a weighted average of all pixels with similar surrounding patch structures:

       u(p) = (1 / C(p)) * sum_{q in SearchArea} w(p, q) * v(q)

Where:
- h (filtering strength): Controls weight attenuation. Larger h removes more noise but may blur fine details.
- templateWindowSize: Size of patch used to compute weights (should be odd, e.g., 7).
- searchWindowSize: Size of window used to search for similar patches (should be odd, e.g., 21).

OpenCV Functions:
- cv2.fastNlMeansDenoising: Optimized NL-means implementation for single-channel grayscale images.
- cv2.fastNlMeansDenoisingColored: NL-means implementation for 3-channel BGR color images.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class Denoiser:
    """
    Class providing Fast Non-Local Means Denoising operations for grayscale and color images.
    """

    @staticmethod
    def denoise_grayscale(
        image: np.ndarray,
        h: float = 10.0,
        template_window_size: int = 7,
        search_window_size: int = 21
    ) -> np.ndarray:
        """
        Applies Fast Non-Local Means Denoising on a single-channel grayscale image.

        :param image: Input 1-channel grayscale image array.
        :param h: Filter strength parameter (higher value removes more noise but reduces detail).
        :param template_window_size: Size in pixels of template patch (odd number, e.g., 7).
        :param search_window_size: Size in pixels of search window (odd number, e.g., 21).
        :return: Denoised grayscale image as uint8 numpy array.
        :raises ImageProcessingError: If image is invalid or parameters are out of bounds.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("Denoiser: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for non-local means denoising.")

        # Ensure grayscale array input
        if len(image.shape) == 3:
            logger.info("Denoiser: Converting 3-channel input to 1-channel grayscale for denoise_grayscale.")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        try:
            logger.info(f"Denoiser: Applying cv2.fastNlMeansDenoising (h={h}, template={template_window_size}, search={search_window_size}).")
            denoised = cv2.fastNlMeansDenoising(
                image,
                dst=None,
                h=h,
                templateWindowSize=template_window_size,
                searchWindowSize=search_window_size
            )
            return denoised
        except Exception as ex:
            logger.error(f"Grayscale NL-Means denoising failed: {ex}")
            raise ImageProcessingError(f"Grayscale denoising error: {ex}") from ex

    @staticmethod
    def denoise_color(
        image: np.ndarray,
        h: float = 10.0,
        h_color: float = 10.0,
        template_window_size: int = 7,
        search_window_size: int = 21
    ) -> np.ndarray:
        """
        Applies Fast Non-Local Means Denoising on a 3-channel BGR color image.

        :param image: Input 3-channel BGR image array.
        :param h: Parameter regulating filter strength for luminance component.
        :param h_color: Parameter regulating filter strength for color components (typically same as h).
        :param template_window_size: Size of template patch (odd number, e.g., 7).
        :param search_window_size: Size of search window (odd number, e.g., 21).
        :return: Denoised 3-channel BGR image as uint8 numpy array.
        :raises ImageProcessingError: If image is invalid.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("Denoiser: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for colored non-local means denoising.")

        try:
            logger.info(f"Denoiser: Applying cv2.fastNlMeansDenoisingColored (h={h}, hColor={h_color}).")
            denoised = cv2.fastNlMeansDenoisingColored(
                image,
                dst=None,
                h=h,
                hColor=h_color,
                templateWindowSize=template_window_size,
                searchWindowSize=search_window_size
            )
            return denoised
        except Exception as ex:
            logger.error(f"Color NL-Means denoising failed: {ex}")
            raise ImageProcessingError(f"Color denoising error: {ex}") from ex
