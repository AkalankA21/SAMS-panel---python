"""
Grayscale Converter Module.

This module provides functionality to convert BGR color images to single-channel
grayscale images using OpenCV. Converting color images to grayscale is a fundamental
preprocessing step in Computer Graphics and Image Processing.

Academic Note (Luminance Equation):
In OpenCV, color images are represented in BGR format by default. Converting to grayscale
calculates the weighted sum (luminance Y) of the R, G, and B channels based on human eye perception:
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    (In BGR order: Y = 0.114 * B + 0.587 * G + 0.299 * R)
Green receives the highest weight because human vision is most sensitive to green wavelengths.

Why Grayscale is essential for Attendance Management Systems (SAMS):
1. Reduces data dimensionality from 3 channels (BGR) to 1 channel (Gray), speeding up computations.
2. Eliminates color variance due to lighting or ink colors, focusing purely on intensity/structure.
3. Simplifies downstream operations like thresholding, edge detection, and cell contour extraction.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class GrayscaleConverter:
    """
    Class responsible for converting BGR images into single-channel grayscale format.
    """

    @staticmethod
    def convert(image: np.ndarray) -> np.ndarray:
        """
        Converts a BGR image to a 1-channel Grayscale image.

        :param image: Input image array (BGR or already Grayscale).
        :return: 1-channel Grayscale image as numpy ndarray.
        :raises ImageProcessingError: If the input image is invalid or empty.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("GrayscaleConverter: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for grayscale conversion.")

        # Check if already grayscale (2D matrix)
        if len(image.shape) == 2:
            logger.info("GrayscaleConverter: Image is already grayscale.")
            return image.copy()

        try:
            logger.info("GrayscaleConverter: Converting BGR image to Grayscale using cv2.COLOR_BGR2GRAY.")
            # OpenCV formula: Y = 0.114*B + 0.587*G + 0.299*R
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray_image
        except Exception as ex:
            logger.error(f"GrayscaleConverter failed: {ex}")
            raise ImageProcessingError(f"Grayscale conversion error: {ex}") from ex

    @staticmethod
    def to_bgr_grayscale(image: np.ndarray) -> np.ndarray:
        """
        Converts a 1-channel Grayscale image into a 3-channel BGR representation.
        Useful when visualization or pipeline components require 3-channel input shapes.

        :param image: Input image array (1-channel Gray or 3-channel BGR).
        :return: 3-channel BGR image.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            raise ImageProcessingError("Invalid image array provided.")

        if len(image.shape) == 3 and image.shape[2] == 3:
            return image.copy()

        try:
            logger.info("GrayscaleConverter: Converting 1-channel Gray to 3-channel BGR representation.")
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        except Exception as ex:
            logger.error(f"Failed to convert grayscale to 3-channel BGR: {ex}")
            raise ImageProcessingError(f"Error converting Gray to BGR: {ex}") from ex
