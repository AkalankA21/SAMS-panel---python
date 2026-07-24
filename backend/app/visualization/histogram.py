"""
Histogram Visualizer Module.

This module uses OpenCV's cv2.calcHist and Matplotlib to plot color/grayscale intensity distributions
and compare histograms before and after histogram equalization.
"""

from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class HistogramVisualizer:
    """
    Class providing plotting tools for single-channel grayscale and multi-channel color image histograms.
    """

    @staticmethod
    def plot_grayscale_histogram(
        image: np.ndarray,
        title: str = "Grayscale Intensity Histogram",
        save_path: str | None = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plots the 1D intensity histogram of a grayscale image.

        :param image: Input 1-channel grayscale image array.
        :param title: Figure title.
        :param save_path: Optional path to save figure.
        :param show: If True, calls plt.show().
        :return: Matplotlib Figure.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ImageProcessingError("Invalid image provided for grayscale histogram plot.")

        if len(image.shape) == 3:
            logger.info("HistogramVisualizer: Converting color image to grayscale for 1D histogram plot.")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        try:
            logger.info("HistogramVisualizer: Calculating grayscale histogram via cv2.calcHist.")
            # cv2.calcHist(images, channels, mask, histSize, ranges)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(hist, color="black", linewidth=1.5)
            ax.set_title(title, fontsize=12, fontweight="bold")
            ax.set_xlabel("Pixel Intensity Value [0 - 255]")
            ax.set_ylabel("Pixel Frequency")
            ax.set_xlim([0, 256])
            ax.grid(True, linestyle="--", alpha=0.5)

            plt.tight_layout()

            if save_path:
                fig.savefig(save_path, bbox_inches="tight", dpi=300)

            if show:
                plt.show()

            return fig
        except Exception as ex:
            logger.error(f"Grayscale histogram plotting failed: {ex}")
            raise ImageProcessingError(f"Grayscale histogram error: {ex}") from ex

    @staticmethod
    def plot_color_histogram(
        image: np.ndarray,
        title: str = "Color Channels Histogram (BGR)",
        save_path: str | None = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plots overlapping color histograms for Blue, Green, and Red channels of a BGR image.

        :param image: Input 3-channel BGR image array.
        :param title: Figure title.
        :param save_path: Optional path to save figure.
        :param show: If True, calls plt.show().
        :return: Matplotlib Figure.
        """
        if image is None or not isinstance(image, np.ndarray) or len(image.shape) != 3:
            raise ImageProcessingError("Input image must be a 3-channel color image for color histogram plotting.")

        try:
            logger.info("HistogramVisualizer: Calculating BGR color channel histograms.")
            fig, ax = plt.subplots(figsize=(8, 4))
            colors = ("b", "g", "r")
            channel_names = ("Blue Channel", "Green Channel", "Red Channel")

            for i, (color, name) in enumerate(zip(colors, channel_names)):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                ax.plot(hist, color=color, label=name, linewidth=1.5)

            ax.set_title(title, fontsize=12, fontweight="bold")
            ax.set_xlabel("Pixel Intensity Value [0 - 255]")
            ax.set_ylabel("Pixel Frequency")
            ax.set_xlim([0, 256])
            ax.legend(loc="upper right")
            ax.grid(True, linestyle="--", alpha=0.5)

            plt.tight_layout()

            if save_path:
                fig.savefig(save_path, bbox_inches="tight", dpi=300)

            if show:
                plt.show()

            return fig
        except Exception as ex:
            logger.error(f"Color histogram plotting failed: {ex}")
            raise ImageProcessingError(f"Color histogram error: {ex}") from ex

    @staticmethod
    def plot_equalization_comparison(
        original: np.ndarray,
        equalized: np.ndarray,
        save_path: str | None = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Creates a 2x2 grid comparing original vs equalized images alongside their intensity histograms.

        :param original: Original image array.
        :param equalized: Equalized image array.
        :param save_path: Optional output file path.
        :param show: If True, calls plt.show().
        :return: Matplotlib Figure.
        """
        if original is None or equalized is None:
            raise ImageProcessingError("Image inputs for equalization comparison plot cannot be None.")

        try:
            logger.info("HistogramVisualizer: Rendering 2x2 equalization comparison grid.")
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))

            # Helper for grayscale array conversion
            orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) if len(original.shape) == 3 else original
            eq_gray = cv2.cvtColor(equalized, cv2.COLOR_BGR2GRAY) if len(equalized.shape) == 3 else equalized

            # (0, 0) Original Image
            axes[0, 0].imshow(orig_gray, cmap="gray")
            axes[0, 0].set_title("Original Image", fontweight="bold")
            axes[0, 0].axis("off")

            # (0, 1) Equalized Image
            axes[0, 1].imshow(eq_gray, cmap="gray")
            axes[0, 1].set_title("Equalized Image", fontweight="bold")
            axes[0, 1].axis("off")

            # (1, 0) Original Histogram
            hist_orig = cv2.calcHist([orig_gray], [0], None, [256], [0, 256])
            axes[1, 0].plot(hist_orig, color="crimson")
            axes[1, 0].set_title("Original Histogram", fontweight="bold")
            axes[1, 0].set_xlim([0, 256])
            axes[1, 0].grid(True, linestyle="--", alpha=0.5)

            # (1, 1) Equalized Histogram
            hist_eq = cv2.calcHist([eq_gray], [0], None, [256], [0, 256])
            axes[1, 1].plot(hist_eq, color="seagreen")
            axes[1, 1].set_title("Equalized Histogram", fontweight="bold")
            axes[1, 1].set_xlim([0, 256])
            axes[1, 1].grid(True, linestyle="--", alpha=0.5)

            plt.tight_layout()

            if save_path:
                fig.savefig(save_path, bbox_inches="tight", dpi=300)

            if show:
                plt.show()

            return fig
        except Exception as ex:
            logger.error(f"Equalization comparison plot failed: {ex}")
            raise ImageProcessingError(f"Equalization comparison error: {ex}") from ex
