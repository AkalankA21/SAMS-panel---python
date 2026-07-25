"""
Enhancement Service Module.

This service coordinates brightness adjustment, contrast scaling, histogram equalization
(standard & CLAHE), spatial filtering (median, gaussian, bilateral), and non-local means denoising.
It also provides pre-configured image enhancement pipelines for processing attendance sheets.
"""

from __future__ import annotations

import numpy as np

from app.preprocessing.bilateral_filter import BilateralFilter
from app.preprocessing.brightness_adjuster import BrightnessAdjuster
from app.preprocessing.contrast_enhancer import ContrastEnhancer
from app.preprocessing.denoiser import Denoiser
from app.preprocessing.grayscale_converter import GrayscaleConverter
from app.preprocessing.guassian_filter import GaussianFilter
from app.preprocessing.histogram_equalizer import HistogramEqualizer
from app.preprocessing.median_filter import MedianFilter
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class EnhancementService:
    """
    Service class to coordinate all image enhancement, filtering, and denoising operations.
    """

    @staticmethod
    def adjust_brightness(image: np.ndarray, beta: int = 30, use_hsv: bool = False) -> np.ndarray:
        """
        Adjusts image brightness.

        :param image: Input image array.
        :param beta: Brightness offset (-255 to 255).
        :param use_hsv: If True and 3-channel, performs brightness adjustment in HSV space.
        :return: Brightness-adjusted image array.
        """
        logger.info(f"EnhancementService: Adjusting brightness (beta={beta}, use_hsv={use_hsv}).")
        if use_hsv and len(image.shape) == 3 and image.shape[2] == 3:
            return BrightnessAdjuster.adjust_hsv(image, beta=beta)
        return BrightnessAdjuster.adjust(image, beta=beta)

    @staticmethod
    def adjust_contrast(image: np.ndarray, alpha: float = 1.5, beta: float = 0.0) -> np.ndarray:
        """
        Adjusts image contrast using linear gain and bias scaling.

        :param image: Input image array.
        :param alpha: Gain multiplier (>1.0 increases contrast).
        :param beta: Bias offset.
        :return: Contrast-enhanced image array.
        """
        logger.info(f"EnhancementService: Adjusting contrast (alpha={alpha}, beta={beta}).")
        return ContrastEnhancer.adjust(image, alpha=alpha, beta=beta)

    @staticmethod
    def stretch_contrast(image: np.ndarray) -> np.ndarray:
        """
        Performs min-max contrast stretching across [0, 255].

        :param image: Input image array.
        :return: Contrast-stretched image array.
        """
        logger.info("EnhancementService: Performing contrast stretching.")
        return ContrastEnhancer.stretch(image)

    @staticmethod
    def equalize_histogram(
        image: np.ndarray,
        use_clahe: bool = True,
        clip_limit: float = 2.0,
        tile_grid_size: tuple[int, int] = (8, 8)
    ) -> np.ndarray:
        """
        Equalizes image histogram using global histogram equalization or CLAHE.

        :param image: Input image array.
        :param use_clahe: If True, applies CLAHE; otherwise applies global histogram equalization.
        :param clip_limit: CLAHE clip limit.
        :param tile_grid_size: CLAHE tile grid dimensions.
        :return: Equalized image array.
        """
        if use_clahe:
            logger.info("EnhancementService: Applying CLAHE histogram equalization.")
            return HistogramEqualizer.apply_clahe(image, clip_limit=clip_limit, tile_grid_size=tile_grid_size)
        logger.info("EnhancementService: Applying Global Histogram Equalization.")
        return HistogramEqualizer.equalize(image)

    @staticmethod
    def apply_filter(image: np.ndarray, method: str = "gaussian", **kwargs) -> np.ndarray:
        """
        Applies a spatial filter to the image.

        :param image: Input image array.
        :param method: Filtering method ('median', 'gaussian', 'bilateral').
        :param kwargs: Additional filter parameters (e.g. kernel_size, d, sigma_color, sigma_space).
        :return: Filtered image array.
        :raises ImageProcessingError: If filter method is unsupported.
        """
        method_lower = method.lower().strip()
        logger.info(f"EnhancementService: Applying spatial filter method '{method_lower}'.")

        if method_lower == "median":
            kernel_size = kwargs.get("kernel_size", 3)
            return MedianFilter.apply(image, kernel_size=kernel_size)
        elif method_lower == "gaussian":
            kernel_size = kwargs.get("kernel_size", (5, 5))
            sigma_x = kwargs.get("sigma_x", 0.0)
            sigma_y = kwargs.get("sigma_y", 0.0)
            return GaussianFilter.apply(image, kernel_size=kernel_size, sigma_x=sigma_x, sigma_y=sigma_y)
        elif method_lower == "bilateral":
            d = kwargs.get("d", 9)
            sigma_color = kwargs.get("sigma_color", 75.0)
            sigma_space = kwargs.get("sigma_space", 75.0)
            return BilateralFilter.apply(image, d=d, sigma_color=sigma_color, sigma_space=sigma_space)
        else:
            logger.error(f"EnhancementService: Unsupported filter method '{method}'.")
            raise ImageProcessingError(f"Unsupported filter method '{method}'. Choose from 'median', 'gaussian', or 'bilateral'.")

    @staticmethod
    def denoise(image: np.ndarray, is_color: bool = False, **kwargs) -> np.ndarray:
        """
        Applies Fast Non-Local Means Denoising.

        :param image: Input image array.
        :param is_color: True if image is 3-channel color, False if 1-channel grayscale.
        :param kwargs: Additional parameters (h, h_color, template_window_size, search_window_size).
        :return: Denoised image array.
        """
        h = kwargs.get("h", 10.0)
        template_window_size = kwargs.get("template_window_size", 7)
        search_window_size = kwargs.get("search_window_size", 21)

        if is_color or (len(image.shape) == 3 and image.shape[2] == 3):
            h_color = kwargs.get("h_color", h)
            logger.info("EnhancementService: Denoising color image using Fast NL-Means.")
            return Denoiser.denoise_color(
                image,
                h=h,
                h_color=h_color,
                template_window_size=template_window_size,
                search_window_size=search_window_size
            )

        logger.info("EnhancementService: Denoising grayscale image using Fast NL-Means.")
        return Denoiser.denoise_grayscale(
            image,
            h=h,
            template_window_size=template_window_size,
            search_window_size=search_window_size
        )

    @staticmethod
    def enhance_attendance_sheet(image: np.ndarray) -> np.ndarray:
        """
        Complete pre-configured enhancement pipeline optimized for attendance sheet analysis.
        Steps:
        1. Convert to 1-channel Grayscale.
        2. Apply CLAHE for local contrast normalization across shadowed paper areas.
        3. Apply Bilateral Filtering for edge-preserving noise reduction (smoothing paper texture while preserving grid lines & marks).

        :param image: Raw input attendance sheet image array (BGR or Gray).
        :return: Enhanced grayscale image ready for cell detection and signature analysis.
        """
        logger.info("EnhancementService: Running complete attendance sheet enhancement pipeline.")
        # Step 1: Grayscale conversion
        gray = GrayscaleConverter.convert(image)

        # Step 2: CLAHE for adaptive contrast enhancement
        clahe_enhanced = HistogramEqualizer.apply_clahe(gray, clip_limit=2.0, tile_grid_size=(8, 8))

        # Step 3: Bilateral Filter for edge preservation
        final_enhanced = BilateralFilter.apply(clahe_enhanced, d=9, sigma_color=75.0, sigma_space=75.0)

        logger.info("EnhancementService: Attendance sheet enhancement pipeline completed successfully.")
        return final_enhanced
