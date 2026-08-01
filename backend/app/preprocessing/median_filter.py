from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class MedianFilter:
    
    # Median filtering implementation.

    DEFAULT_KERNEL_SIZE = 5

    @staticmethod
    def apply(
        image_data: ImageData,
        kernel_size: int = DEFAULT_KERNEL_SIZE,
    ) -> np.ndarray:
        
        # Apply median filtering.

        try:

            logger.info(
                "Applying median filter..."
            )

            if image_data is None:

                raise ImageProcessingError(
                    "ImageData cannot be None."
                )

            # -----------------------------
            # Select latest available image
            # -----------------------------

            source = None

            if image_data.clahe_image is not None:
                source = image_data.clahe_image
            elif image_data.equalized_image is not None:
                source = image_data.equalized_image
            elif image_data.contrast_image is not None:
                source = image_data.contrast_image
            elif image_data.brightness_image is not None:
                source = image_data.brightness_image
            elif image_data.grayscale_image is not None:
                source = image_data.grayscale_image
            elif image_data.image is not None:
                source = image_data.image
            else:
                raise ImageProcessingError(
                    "No grayscale image available."
                )

            # -----------------------------
            # Validate kernel
            # -----------------------------

            if kernel_size < 3:

                kernel_size = 3

            if kernel_size % 2 == 0:

                kernel_size += 1

            filtered = cv2.medianBlur(
                source,
                kernel_size,
            )

            image_data.median_image = filtered

            image_data.processing_history[
                "Median"
            ] = filtered

            image_data.set_stage(
                "Median Filtering"
            )

            logger.info(
                "Median filter completed."
            )

            return filtered

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Median filtering failed: {ex}"
            ) from ex

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return median image statistics.

        if image_data.median_image is None:

            raise ImageProcessingError(
                "Median image not found."
            )

        return ImageStatistics.basic(
            image_data.median_image
        )

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:
        
        # Compare before and after filtering.

        if image_data.median_image is None:

            raise ImageProcessingError(
                "Median image missing."
            )

        if image_data.clahe_image is not None:

            original = image_data.clahe_image

        elif image_data.equalized_image is not None:

            original = image_data.equalized_image

        else:

            original = image_data.grayscale_image

        return ImageStatistics.compare(
            original,
            image_data.median_image,
        )

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return preview image.

        if image_data.median_image is None:

            return MedianFilter.apply(
                image_data
            )

        return image_data.median_image.copy()

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Remove median filter result.

        image_data.median_image = None

        image_data.processing_history.pop(
            "Median",
            None,
        )

        logger.info(
            "Median filter reset."
        )