from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class GaussianFilter:
    
    # Gaussian filtering implementation.

    DEFAULT_KERNEL = (5, 5)
    DEFAULT_SIGMA = 1.0

    @staticmethod
    def apply(
        image_data: ImageData,
        kernel_size: tuple[int, int] = DEFAULT_KERNEL,
        sigma: float = DEFAULT_SIGMA,
    ) -> np.ndarray:
        
        # Apply Gaussian Blur.

        try:

            logger.info(
                "Applying Gaussian filter..."
            )

            if image_data is None:
                raise ImageProcessingError(
                    "ImageData cannot be None."
                )

            source = GaussianFilter._get_source_image(
                image_data
            )

            kx, ky = kernel_size

            if kx % 2 == 0:
                kx += 1

            if ky % 2 == 0:
                ky += 1

            kernel_size = (kx, ky)

            filtered = cv2.GaussianBlur(
                source,
                kernel_size,
                sigmaX=sigma,
                sigmaY=sigma,
            )

            image_data.gaussian_image = filtered

            image_data.processing_history[
                "Gaussian"
            ] = filtered

            image_data.set_stage(
                "Gaussian Filtering"
            )

            logger.info(
                "Gaussian filter completed."
            )

            return filtered

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Gaussian filtering failed: {ex}"
            ) from ex

    @staticmethod
    def _get_source_image(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Select the latest available processed image.

        if image_data.median_image is not None:
            return image_data.median_image

        if image_data.clahe_image is not None:
            return image_data.clahe_image

        if image_data.equalized_image is not None:
            return image_data.equalized_image

        if image_data.contrast_image is not None:
            return image_data.contrast_image

        if image_data.brightness_image is not None:
            return image_data.brightness_image

        if image_data.grayscale_image is not None:
            return image_data.grayscale_image

        raise ImageProcessingError(
            "No grayscale image available."
        )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return Gaussian image statistics.

        if image_data.gaussian_image is None:

            raise ImageProcessingError(
                "Gaussian image not found."
            )

        return ImageStatistics.basic(
            image_data.gaussian_image
        )

    @staticmethod
    def compare(
        image_data: ImageData,
    ) -> dict:
        
        # Compare original and Gaussian filtered image.

        if image_data.gaussian_image is None:

            raise ImageProcessingError(
                "Gaussian image missing."
            )

        source = GaussianFilter._get_source_image(
            image_data
        )

        return ImageStatistics.compare(
            source,
            image_data.gaussian_image,
        )

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return preview image.

        if image_data.gaussian_image is None:

            return GaussianFilter.apply(
                image_data
            )

        return image_data.gaussian_image.copy()

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Remove Gaussian filter result.

        image_data.gaussian_image = None

        image_data.processing_history.pop(
            "Gaussian",
            None,
        )

        logger.info(
            "Gaussian filter reset."
        )