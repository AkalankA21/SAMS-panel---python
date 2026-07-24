"""
Brightness Adjuster Module.

This module provides functionality to modify the overall brightness of an image.
Brightness control alters the overall lightness or darkness of pixel values.

Academic Note (Linear Brightness Transformation):
Brightness adjustment is mathematically represented as a scalar addition/subtraction to pixel intensity:
    g(x, y) = f(x, y) + beta

Where:
- f(x, y) is the original pixel intensity at location (x, y).
- beta (scalar offset) > 0 increases brightness (lightens image).
- beta (scalar offset) < 0 decreases brightness (darkens image).
- g(x, y) is clipped to valid uint8 intensity bounds: [0, 255].

OpenCV Implementation:
cv2.convertScaleAbs(image, alpha=1.0, beta=beta) applies this linear transformation efficiently
with built-in saturation arithmetic (preventing underflow below 0 or overflow above 255).
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class BrightnessAdjuster:
    """
    Class providing methods to adjust image brightness using spatial intensity scaling
    or color space transformations.
    """

    @staticmethod
    def adjust(image: np.ndarray, beta: int = 30) -> np.ndarray:
        """
        Adjusts brightness of an image by adding/subtracting scalar offset beta.

        :param image: Input image (Grayscale or BGR).
        :param beta: Brightness offset value (-255 to 255). Positive brightens, negative darkens.
        :return: Brightness-adjusted uint8 image.
        :raises ImageProcessingError: If image is invalid.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("BrightnessAdjuster: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for brightness adjustment.")

        try:
            logger.info(f"BrightnessAdjuster: Adjusting brightness with beta={beta}.")
            # alpha=1.0 keeps contrast unchanged, beta shifts intensity values up/down
            adjusted_image = cv2.convertScaleAbs(image, alpha=1.0, beta=beta)
            return adjusted_image
        except Exception as ex:
            logger.error(f"BrightnessAdjuster failed: {ex}")
            raise ImageProcessingError(f"Brightness adjustment error: {ex}") from ex

    @staticmethod
    def adjust_hsv(image: np.ndarray, beta: int = 30) -> np.ndarray:
        """
        Adjusts brightness specifically in the HSV color space by altering the V (Value/Brightness) channel.
        Preserves original hue and saturation attributes better than direct BGR addition.

        :param image: Input 3-channel BGR image.
        :param beta: Brightness offset (-255 to 255).
        :return: Brightness-adjusted 3-channel BGR image.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            raise ImageProcessingError("Invalid image array provided for HSV brightness adjustment.")

        if len(image.shape) != 3 or image.shape[2] != 3:
            logger.warning("BrightnessAdjuster: Input is not a 3-channel BGR image. Falling back to standard adjust.")
            return BrightnessAdjuster.adjust(image, beta=beta)

        try:
            logger.info(f"BrightnessAdjuster: Adjusting brightness in HSV space with beta={beta}.")
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)

            # Adjust V channel with clipping
            v_adjusted = cv2.convertScaleAbs(v, alpha=1.0, beta=beta)

            hsv_adjusted = cv2.merge([h, s, v_adjusted])
            bgr_result = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2BGR)
            return bgr_result
        except Exception as ex:
            logger.error(f"HSV brightness adjustment failed: {ex}")
            raise ImageProcessingError(f"HSV brightness adjustment error: {ex}") from ex
