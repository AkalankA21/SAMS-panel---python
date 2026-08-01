from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class HistogramEqualizer:
    
    # Performs histogram equalization and CLAHE.

    @staticmethod
    def equalize(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Apply standard histogram equalization.

        try:

            logger.info(
                "Starting histogram equalization."
            )

            if image_data.grayscale_image is None:

                raise ImageProcessingError(
                    "Grayscale image not found."
                )

            equalized = cv2.equalizeHist(
                image_data.grayscale_image
            )

            image_data.equalized_image = equalized

            image_data.processing_history[
                "Equalization"
            ] = equalized

            image_data.set_stage(
                "Histogram Equalization"
            )

            logger.info(
                "Histogram equalization completed."
            )

            return equalized

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def clahe(
        image_data: ImageData,
        clip_limit: float = 2.0,
        tile_grid_size: tuple[int, int] = (8, 8),
    ) -> np.ndarray:
        
        # Apply CLAHE.

        try:

            logger.info(
                "Applying CLAHE."
            )

            if image_data.grayscale_image is None:

                raise ImageProcessingError(
                    "Grayscale image not found."
                )

            clahe = cv2.createCLAHE(
                clipLimit=clip_limit,
                tileGridSize=tile_grid_size,
            )

            result = clahe.apply(
                image_data.grayscale_image
            )

            image_data.clahe_image = result

            image_data.processing_history[
                "CLAHE"
            ] = result

            image_data.set_stage(
                "CLAHE"
            )

            logger.info(
                "CLAHE completed."
            )

            return result

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def histogram(
        image: np.ndarray,
    ) -> np.ndarray:
        
        # Calculate image histogram.

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

        hist = HistogramEqualizer.histogram(
            image
        )

        return np.cumsum(hist)

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:
        
        # Compare original and enhanced images.

        if image_data.equalized_image is None:

            raise ImageProcessingError(
                "Equalized image not found."
            )

        original = image_data.grayscale_image
        equalized = image_data.equalized_image

        return {

            "Original Mean":
                round(
                    float(original.mean()),
                    2,
                ),

            "Equalized Mean":
                round(
                    float(equalized.mean()),
                    2,
                ),

            "Original Std":
                round(
                    float(original.std()),
                    2,
                ),

            "Equalized Std":
                round(
                    float(equalized.std()),
                    2,
                ),
        }

    @staticmethod
    def statistics(
        image: np.ndarray,
    ) -> dict:
        
        # Return image statistics.

        return {

            "Minimum":
                int(image.min()),

            "Maximum":
                int(image.max()),

            "Mean":
                round(
                    float(image.mean()),
                    2,
                ),

            "Median":
                round(
                    float(np.median(image)),
                    2,
                ),

            "Standard Deviation":
                round(
                    float(image.std()),
                    2,
                ),
        }

    @staticmethod
    def preview(
        image_data: ImageData,
        mode: str = "equalized",
    ) -> np.ndarray:
        
        # Return preview image.

        if mode.lower() == "clahe":

            if image_data.clahe_image is None:

                return HistogramEqualizer.clahe(
                    image_data
                )

            return image_data.clahe_image.copy()

        if image_data.equalized_image is None:

            return HistogramEqualizer.equalize(
                image_data
            )

        return image_data.equalized_image.copy()

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset histogram processing.

        image_data.equalized_image = None
        image_data.clahe_image = None

        image_data.processing_history.pop(
            "Equalization",
            None,
        )

        image_data.processing_history.pop(
            "CLAHE",
            None,
        )

        logger.info(
            "Histogram processing reset."
        )