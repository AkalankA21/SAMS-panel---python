from __future__ import annotations

import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError


class ImageSelector:
    
    # Selects the latest processed image.

    @staticmethod
    def get_latest(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return the latest processed image.

        if image_data is None:

            raise ImageProcessingError(
                "ImageData cannot be None."
            )

        priority = (

            getattr(image_data, "binary_image", None),

            getattr(image_data, "closed_image", None),

            getattr(image_data, "opened_image", None),

            getattr(image_data, "denoised_image", None),

            getattr(image_data, "bilateral_image", None),

            getattr(image_data, "gaussian_image", None),

            getattr(image_data, "median_image", None),

            getattr(image_data, "clahe_image", None),

            getattr(image_data, "equalized_image", None),

            getattr(image_data, "contrast_image", None),

            getattr(image_data, "brightness_image", None),

            getattr(image_data, "grayscale_image", None),

            getattr(image_data, "perspective_image", None),

            image_data.image,
        )

        for image in priority:

            if image is not None:

                return image

        raise ImageProcessingError(
            "No image available."
        )

    @staticmethod
    def get_grayscale(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return latest grayscale image.

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
    def get_color(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return original color image.

        if image_data.image is None:

            raise ImageProcessingError(
                "Original image not available."
            )

        return image_data.image