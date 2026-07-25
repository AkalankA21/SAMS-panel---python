"""
Grayscale Visualizer Module.

This module provides Matplotlib-based visualizer utilities to compare original BGR color images
with their converted grayscale counterparts side-by-side.
"""

from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class GrayscaleVisualizer:
    """
    Class for rendering side-by-side comparisons of original BGR images and grayscale conversions.
    """

    @staticmethod
    def plot_comparison(
        original_bgr: np.ndarray,
        gray_image: np.ndarray,
        title_orig: str = "Original Image (BGR)",
        title_gray: str = "Grayscale Image",
        save_path: str | None = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Displays original BGR image and Grayscale image side-by-side using Matplotlib.

        :param original_bgr: Original BGR image array.
        :param gray_image: Grayscale image array (1-channel).
        :param title_orig: Subplot title for original image.
        :param title_gray: Subplot title for grayscale image.
        :param save_path: Optional path to save the output figure to disk.
        :param show: If True, calls plt.show() to display plot window.
        :return: Matplotlib Figure instance.
        """
        if original_bgr is None or gray_image is None:
            logger.error("GrayscaleVisualizer: Received None for image parameters.")
            raise ImageProcessingError("Invalid image input for GrayscaleVisualizer.")

        try:
            logger.info("GrayscaleVisualizer: Creating side-by-side grayscale comparison plot.")
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))

            # Matplotlib expects RGB format for 3-channel images
            if len(original_bgr.shape) == 3 and original_bgr.shape[2] == 3:
                rgb_orig = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)
            else:
                rgb_orig = original_bgr

            # Plot original
            axes[0].imshow(rgb_orig)
            axes[0].set_title(title_orig, fontsize=12, fontweight="bold")
            axes[0].axis("off")

            # Plot grayscale
            if len(gray_image.shape) == 2:
                axes[1].imshow(gray_image, cmap="gray")
            else:
                axes[1].imshow(gray_image)
            axes[1].set_title(title_gray, fontsize=12, fontweight="bold")
            axes[1].axis("off")

            plt.tight_layout()

            if save_path:
                logger.info(f"GrayscaleVisualizer: Saving figure to {save_path}.")
                fig.savefig(save_path, bbox_inches="tight", dpi=300)

            if show:
                plt.show()

            return fig
        except Exception as ex:
            logger.error(f"GrayscaleVisualizer failed: {ex}")
            raise ImageProcessingError(f"Grayscale visualization error: {ex}") from ex
