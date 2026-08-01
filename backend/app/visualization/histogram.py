from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.utils.image_statistics import ImageStatistics


class HistogramVisualizer:
    
    # Generates histogram visualizations.

    @staticmethod
    def calculate(image: np.ndarray) -> np.ndarray:
        
        # Calculate histogram.

        return ImageStatistics.histogram(image)

    @staticmethod
    def show(
        image: np.ndarray,
        title: str = "Histogram",
    ) -> None:
        """
        Display histogram.
        """

        histogram = ImageStatistics.histogram(image)

        plt.figure(figsize=(8, 4))
        plt.title(title)
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.xlim([0, 255])
        plt.plot(histogram)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def compare(
        original: np.ndarray,
        processed: np.ndarray,
        original_title="Original",
        processed_title="Processed",
    ):
        
        # Compare two histograms.

        hist1 = ImageStatistics.histogram(original)
        hist2 = ImageStatistics.histogram(processed)

        plt.figure(figsize=(9,5))

        plt.plot(hist1,label=original_title)
        plt.plot(hist2,label=processed_title)

        plt.title("Histogram Comparison")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def save(
        image: np.ndarray,
        filepath: str,
        title="Histogram",
    ):

        hist = ImageStatistics.histogram(image)

        plt.figure(figsize=(8,4))

        plt.plot(hist)

        plt.title(title)

        plt.xlabel("Pixel")

        plt.ylabel("Frequency")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(filepath)

        plt.close()

    @staticmethod
    def cumulative(image: np.ndarray):

        hist = ImageStatistics.cumulative_histogram(image)

        plt.figure(figsize=(8,4))

        plt.plot(hist)

        plt.title("Cumulative Histogram")

        plt.xlabel("Pixel")

        plt.ylabel("Cumulative Frequency")

        plt.grid(True)

        plt.tight_layout()

        plt.show()

    @staticmethod
    def rgb(image: np.ndarray):

        colors=("b","g","r")

        plt.figure(figsize=(8,4))

        for i,color in enumerate(colors):

            hist=cv2.calcHist(
                [image],
                [i],
                None,
                [256],
                [0,256],
            )

            plt.plot(hist,color=color)

        plt.title("RGB Histogram")

        plt.xlabel("Pixel")

        plt.ylabel("Frequency")

        plt.grid(True)

        plt.tight_layout()

        plt.show()