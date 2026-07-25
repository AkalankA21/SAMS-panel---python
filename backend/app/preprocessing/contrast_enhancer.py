"""
Contrast Enhancer Module.

This module provides functionality to enhance image contrast using basic linear scaling
(gain and bias) as well as min-max contrast stretching.

Academic Note (Linear Contrast Transformation):
Contrast represents the difference in visual properties that makes an object distinguishable
from other objects and background. Mathematically, contrast scaling is defined as:
    g(x, y) = alpha * f(x, y) + beta

Where:
- alpha (gain) controls contrast:
    - alpha > 1.0 increases contrast (expands dynamic range).
    - 0 < alpha < 1.0 decreases contrast (compresses dynamic range).
- beta (bias) controls brightness offset.
- Saturation arithmetic clips results to [0, 255].

Linear Contrast Stretching (Normalization):
Rescales the pixel intensities from the input range [I_min, I_max] to the full dynamic range [0, 255]:
    P_out = (P_in - I_min) * (255 / (I_max - I_min))
This enhances subtle intensity variations in low-contrast attendance sheet captures.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class ContrastEnhancer:
    """
    Class providing methods to scale contrast linearly and stretch intensity ranges.
    """

    @staticmethod
    def adjust(image: np.ndarray, alpha: float = 1.5, beta: float = 0.0) -> np.ndarray:
        """
        Enhances image contrast using linear alpha/beta scaling.

        :param image: Input image array (Grayscale or BGR).
        :param alpha: Contrast multiplier (alpha > 1.0 increases contrast, e.g., 1.2 to 2.0).
        :param beta: Brightness offset (default 0.0).
        :return: Contrast-enhanced uint8 image.
        :raises ImageProcessingError: If image array is invalid or alpha is non-positive.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("ContrastEnhancer: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for contrast adjustment.")

        if alpha <= 0:
            logger.error("ContrastEnhancer: Alpha parameter must be strictly positive.")
            raise ImageProcessingError("Alpha parameter for contrast scaling must be greater than 0.")

        try:
            logger.info(f"ContrastEnhancer: Adjusting contrast with alpha={alpha}, beta={beta}.")
            # cv2.convertScaleAbs performs g(x,y) = saturate_cast<uchar>(alpha*f(x,y) + beta)
            enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
            return enhanced
        except Exception as ex:
            logger.error(f"ContrastEnhancer failed: {ex}")
            raise ImageProcessingError(f"Contrast enhancement error: {ex}") from ex

    @staticmethod
    def stretch(image: np.ndarray) -> np.ndarray:
        """
        Performs linear min-max contrast stretching to expand pixel intensity values
        across the full [0, 255] dynamic range.

        :param image: Input image array.
        :return: Contrast-stretched uint8 image.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            raise ImageProcessingError("Invalid image array provided for contrast stretching.")

        try:
            logger.info("ContrastEnhancer: Applying min-max linear contrast stretching using cv2.normalize.")
            stretched = cv2.normalize(
                image,
                dst=None,
                alpha=0,
                beta=255,
                norm_type=cv2.NORM_MINMAX,
                dtype=cv2.CV_8U
            )
            return stretched
        except Exception as ex:
            logger.error(f"Contrast stretching failed: {ex}")
            raise ImageProcessingError(f"Contrast stretching error: {ex}") from ex
