"""
Enhancement Visualizer Module.

This module provides Matplotlib visualizer tools to compare original images
against enhanced images (brightness/contrast adjusted, equalized, or denoised).
"""

from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class EnhancementVisualizer:
    """
    Class for rendering side-by-side visual comparisons of original and enhanced images.
    """

    @staticmethod
    def plot_comparison(
        original: np.ndarray,
        enhanced: np.ndarray,
        title_orig: str = "Original Image",
        title_enh: str = "Enhanced Image",
        save_path: str | None = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Renders a side-by-side comparison plot of the original and enhanced images.

        :param original: Original image array (BGR or Grayscale).
        :param enhanced: Enhanced image array (BGR or Grayscale).
        :param title_orig: Title for original image subplot.
        :param title_enh: Title for enhanced image subplot.
        :param save_path: Optional path to save figure.
        :param show: If True, calls plt.show().
        :return: Matplotlib Figure instance.
        """
        if original is None or enhanced is None:
            logger.error("EnhancementVisualizer: Image inputs cannot be None.")
            raise ImageProcessingError("Invalid image inputs for EnhancementVisualizer.")

        try:
            logger.info("EnhancementVisualizer: Rendering original vs enhanced comparison plot.")
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Helper to convert image for Matplotlib
            def prep_img(img: np.ndarray) -> tuple[np.ndarray, str | None]:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB), None
                return img, "gray"

            img_orig_disp, cmap_orig = prep_img(original)
            img_enh_disp, cmap_enh = prep_img(enhanced)

            # Subplot 1: Original
            axes[0].imshow(img_orig_disp, cmap=cmap_orig)
            axes[0].set_title(title_orig, fontsize=12, fontweight="bold")
            axes[0].axis("off")

            # Subplot 2: Enhanced
            axes[1].imshow(img_enh_disp, cmap=cmap_enh)
            axes[1].set_title(title_enh, fontsize=12, fontweight="bold")
            axes[1].axis("off")

            plt.tight_layout()

            if save_path:
                logger.info(f"EnhancementVisualizer: Saving figure to {save_path}.")
                fig.savefig(save_path, bbox_inches="tight", dpi=300)

            if show:
                plt.show()

            return fig
        except Exception as ex:
            logger.error(f"EnhancementVisualizer failed: {ex}")
            raise ImageProcessingError(f"Enhancement visualization error: {ex}") from ex
