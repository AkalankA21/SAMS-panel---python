"""
Filter Comparison Visualizer Module.

This module provides Matplotlib visualization tools to render side-by-side comparisons
of Median, Gaussian, and Bilateral spatial filters applied to the same input image.
"""

from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.preprocessing.bilateral_filter import BilateralFilter
from app.preprocessing.guassian_filter import GaussianFilter
from app.preprocessing.median_filter import MedianFilter
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class FilterComparisonVisualizer:
    """
    Class for rendering side-by-side comparative subplots of different filtering techniques.
    """

    @staticmethod
    def compare_filters(
        image: np.ndarray,
        median_kernel: int = 5,
        gaussian_kernel: tuple[int, int] = (5, 5),
        bilateral_d: int = 9,
        save_path: str | None = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Applies Median, Gaussian, and Bilateral filters to an input image and displays
        all results in a 2x2 grid comparison alongside the original image.

        :param image: Input image array (BGR or Grayscale).
        :param median_kernel: Kernel size for Median filter (odd integer > 1).
        :param gaussian_kernel: Kernel dimensions for Gaussian blur tuple (w, h).
        :param bilateral_d: Pixel neighborhood diameter for Bilateral filter.
        :param save_path: Optional file path to save figure.
        :param show: If True, calls plt.show().
        :return: Matplotlib Figure instance.
        """
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            logger.error("FilterComparisonVisualizer: Input image is empty or invalid.")
            raise ImageProcessingError("Invalid image input for filter comparison visualization.")

        try:
            logger.info("FilterComparisonVisualizer: Generating filter comparison results...")
            # Compute filtered images
            img_median = MedianFilter.apply(image, kernel_size=median_kernel)
            img_gaussian = GaussianFilter.apply(image, kernel_size=gaussian_kernel)
            img_bilateral = BilateralFilter.apply(image, d=bilateral_d, sigma_color=75.0, sigma_space=75.0)

            # Helper for displaying BGR or Grayscale images properly in Matplotlib
            def prep_for_plot(img: np.ndarray) -> tuple[np.ndarray, str | None]:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB), None
                return img, "gray"

            fig, axes = plt.subplots(2, 2, figsize=(12, 10))

            # Subplot 0,0: Original
            disp_orig, cmap_orig = prep_for_plot(image)
            axes[0, 0].imshow(disp_orig, cmap=cmap_orig)
            axes[0, 0].set_title("Original Image", fontsize=11, fontweight="bold")
            axes[0, 0].axis("off")

            # Subplot 0,1: Median Filter
            disp_med, cmap_med = prep_for_plot(img_median)
            axes[0, 1].imshow(disp_med, cmap=cmap_med)
            axes[0, 1].set_title(f"Median Filter (k={median_kernel})\n[Salt & Pepper Noise Removal]", fontsize=11, fontweight="bold")
            axes[0, 1].axis("off")

            # Subplot 1,0: Gaussian Blur
            disp_gauss, cmap_gauss = prep_for_plot(img_gaussian)
            axes[1, 0].imshow(disp_gauss, cmap=cmap_gauss)
            axes[1, 0].set_title(f"Gaussian Blur (k={gaussian_kernel})\n[Low-Pass Smoothing]", fontsize=11, fontweight="bold")
            axes[1, 0].axis("off")

            # Subplot 1,1: Bilateral Filter
            disp_bilat, cmap_bilat = prep_for_plot(img_bilateral)
            axes[1, 1].imshow(disp_bilat, cmap=cmap_bilat)
            axes[1, 1].set_title(f"Bilateral Filter (d={bilateral_d})\n[Edge-Preserving Smoothing]", fontsize=11, fontweight="bold")
            axes[1, 1].axis("off")

            plt.tight_layout()

            if save_path:
                logger.info(f"FilterComparisonVisualizer: Saving plot figure to {save_path}.")
                fig.savefig(save_path, bbox_inches="tight", dpi=300)

            if show:
                plt.show()

            return fig
        except Exception as ex:
            logger.error(f"FilterComparisonVisualizer failed: {ex}")
            raise ImageProcessingError(f"Filter comparison visualization error: {ex}") from ex
