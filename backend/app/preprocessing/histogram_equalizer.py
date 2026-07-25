"""
Histogram Equalizer Module.

This module implements standard global Histogram Equalization and CLAHE
(Contrast Limited Adaptive Histogram Equalization).

Academic Note (Histogram Equalization Mathematics):
Histogram Equalization improves image contrast by re-distributing pixel intensity values
so that the output intensity distribution (histogram) approaches a uniform distribution.

1. Global Histogram Equalization (GHE):
   Calculates the normalized Cumulative Distribution Function (CDF) of image intensities:
       T(k) = round( (CDF(k) - CDF_min) / (Total_Pixels - CDF_min) * (L - 1) )
   Where L = 256 for 8-bit images.
   Limitations: GHE operates globally across the entire image. If an attendance sheet has uneven
   shadows or lighting, GHE can over-amplify noise or wash out regions with high brightness contrast.

2. Contrast Limited Adaptive Histogram Equalization (CLAHE):
   Addresses GHE limitations by dividing the image into small contextual regions called "tiles"
   (e.g., 8x8 blocks) and equalizing each tile individually.
   - Contrast Limiting: A clip limit (e.g., 2.0) prevents over-amplification of noise in homogeneous tiles.
     Any histogram bin exceeding the clip limit is redistributed among all bins before CDF computation.
   - Bilinear Interpolation: Smoothly blends boundaries between adjacent tiles to prevent artifact seams.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class HistogramEqualizer:
    """
    Class implementing global Histogram Equalization and CLAHE algorithms.
    """

    @staticmethod
    def equalize(image: np.ndarray) -> np.ndarray:
        """
        Applies standard Global Histogram Equalization.
        If a 3-channel BGR image is passed, equalization is applied to the Y (Luminance) channel
        in the YCrCb color space to preserve color balance.

        :param image: Input image array (Grayscale or BGR).
        :return: Histogram-equalized uint8 image.
        :raises ImageProcessingError: If image array is invalid.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("HistogramEqualizer: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for histogram equalization.")

        try:
            if len(image.shape) == 2:
                logger.info("HistogramEqualizer: Applying standard cv2.equalizeHist on grayscale image.")
                return cv2.equalizeHist(image)

            # For 3-channel color image, convert to YCrCb and equalize Y channel
            logger.info("HistogramEqualizer: Applying equalization on Y channel in YCrCb color space.")
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(ycrcb)

            y_eq = cv2.equalizeHist(y)

            ycrcb_eq = cv2.merge([y_eq, cr, cb])
            return cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)
        except Exception as ex:
            logger.error(f"Global histogram equalization failed: {ex}")
            raise ImageProcessingError(f"Histogram equalization error: {ex}") from ex

    @staticmethod
    def apply_clahe(
        image: np.ndarray,
        clip_limit: float = 2.0,
        tile_grid_size: tuple[int, int] = (8, 8)
    ) -> np.ndarray:
        """
        Applies Contrast Limited Adaptive Histogram Equalization (CLAHE).

        :param image: Input image array (Grayscale or BGR).
        :param clip_limit: Threshold for contrast clipping (default 2.0). Higher values increase contrast.
        :param tile_grid_size: Grid size for contextual tile division (default 8x8).
        :return: CLAHE-enhanced uint8 image.
        :raises ImageProcessingError: If input parameters are invalid.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("HistogramEqualizer: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image array provided for CLAHE.")

        try:
            logger.info(f"HistogramEqualizer: Applying CLAHE (clip_limit={clip_limit}, tile_grid_size={tile_grid_size}).")
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

            if len(image.shape) == 2:
                return clahe.apply(image)

            # Color image handling: apply CLAHE on LAB L (Lightness) channel
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)

            l_clahe = clahe.apply(l)

            lab_clahe = cv2.merge([l_clahe, a, b])
            return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
        except Exception as ex:
            logger.error(f"CLAHE application failed: {ex}")
            raise ImageProcessingError(f"CLAHE error: {ex}") from ex
