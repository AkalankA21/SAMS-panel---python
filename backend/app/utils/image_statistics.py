from __future__ import annotations

from typing import Any

import cv2
import numpy as np

from app.utils.exceptions import ImageProcessingError


class ImageStatistics:
    
    # Utility class for calculating image statistics.

    @staticmethod
    def validate(image: np.ndarray) -> None:
        
        # Validate input image.

        if image is None:
            raise ImageProcessingError(
                "Image cannot be None."
            )

        if not isinstance(image, np.ndarray):
            raise ImageProcessingError(
                "Invalid image type."
            )

        if image.size == 0:
            raise ImageProcessingError(
                "Image is empty."
            )

    @staticmethod
    def basic(image: np.ndarray) -> dict[str, Any]:
        
        # Return basic image statistics.

        ImageStatistics.validate(image)

        return {
            "Minimum": int(np.min(image)),
            "Maximum": int(np.max(image)),
            "Mean": round(float(np.mean(image)), 2),
            "Median": round(float(np.median(image)), 2),
            "Standard Deviation": round(float(np.std(image)), 2),
            "Variance": round(float(np.var(image)), 2),
            "Width": int(image.shape[1]),
            "Height": int(image.shape[0]),
            "Pixels": int(image.size),
            "Data Type": str(image.dtype),
        }

    @staticmethod
    def histogram(image: np.ndarray) -> np.ndarray:
        
        # Calculate histogram.

        ImageStatistics.validate(image)

        histogram = cv2.calcHist(
            [image],
            [0],
            None,
            [256],
            [0, 256],
        )

        return histogram.flatten()

    @staticmethod
    def cumulative_histogram(
        image: np.ndarray,
    ) -> np.ndarray:
        
        # Calculate cumulative histogram.

        hist = ImageStatistics.histogram(image)

        return np.cumsum(hist)

    @staticmethod
    def min_max(image: np.ndarray) -> tuple[int, int]:
        
        # Return minimum and maximum values.

        ImageStatistics.validate(image)

        return (
            int(np.min(image)),
            int(np.max(image)),
        )

    @staticmethod
    def mean(image: np.ndarray) -> float:
        
        # Return mean intensity.

        ImageStatistics.validate(image)

        return round(float(np.mean(image)), 2)

    @staticmethod
    def std(image: np.ndarray) -> float:
        
        # Return standard deviation.

        ImageStatistics.validate(image)

        return round(float(np.std(image)), 2)

    @staticmethod
    def variance(image: np.ndarray) -> float:
        
        # Return variance.

        ImageStatistics.validate(image)

        return round(float(np.var(image)), 2)

    @staticmethod
    def entropy(image: np.ndarray) -> float:
        
        # Calculate image entropy.

        ImageStatistics.validate(image)

        hist = ImageStatistics.histogram(image)

        hist = hist / hist.sum()

        hist = hist[hist > 0]

        entropy = -np.sum(
            hist * np.log2(hist)
        )

        return round(float(entropy), 4)

    @staticmethod
    def compare(
        image1: np.ndarray,
        image2: np.ndarray,
    ) -> dict[str, float]:
        
        # Compare two images statistically.

        ImageStatistics.validate(image1)
        ImageStatistics.validate(image2)

        return {

            "Mean Difference":
                round(
                    float(
                        np.mean(image2) -
                        np.mean(image1)
                    ),
                    2,
                ),

            "Std Difference":
                round(
                    float(
                        np.std(image2) -
                        np.std(image1)
                    ),
                    2,
                ),

            "Variance Difference":
                round(
                    float(
                        np.var(image2) -
                        np.var(image1)
                    ),
                    2,
                ),
        }

    @staticmethod
    def resolution(
        image: np.ndarray,
    ) -> str:
        
        # Return image resolution.

        ImageStatistics.validate(image)

        return f"{image.shape[1]} x {image.shape[0]}"

    @staticmethod
    def channels(
        image: np.ndarray,
    ) -> int:
        
        # Return channel count.

        ImageStatistics.validate(image)

        if len(image.shape) == 2:
            return 1

        return image.shape[2]