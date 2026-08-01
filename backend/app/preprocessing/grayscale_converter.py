from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class GrayscaleConverter:
    
    # Converts RGB/BGR images to grayscale.

    @staticmethod
    def convert(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Convert image to grayscale.

        try:

            logger.info(
                "Starting grayscale conversion..."
            )

            if image_data is None:
                raise ImageProcessingError(
                    "ImageData cannot be None."
                )

            if image_data.image is None:
                raise ImageProcessingError(
                    "Image is empty."
                )

            # ---------------------------------
            # Select source image
            # ---------------------------------

            if image_data.perspective_image is not None:

                source = image_data.perspective_image

                logger.info(
                    "Using perspective corrected image."
                )

            else:

                source = image_data.image

                logger.info(
                    "Using original image."
                )

            # ---------------------------------
            # Already grayscale?
            # ---------------------------------

            if len(source.shape) == 2:

                gray = source.copy()

            elif source.shape[2] == 1:

                gray = source[:, :, 0]

            else:

                gray = cv2.cvtColor(
                    source,
                    cv2.COLOR_BGR2GRAY,
                )

            image_data.grayscale_image = gray

            image_data.processing_history[
                "Grayscale"
            ] = gray

            image_data.set_stage(
                "Grayscale Conversion"
            )

            logger.info(
                "Grayscale conversion completed."
            )

            return gray

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                f"Grayscale conversion failed: {ex}"
            ) from ex

    @staticmethod
    def is_grayscale(
        image: np.ndarray,
    ) -> bool:
        
        # Check whether an image is grayscale.

        if image is None:
            return False

        if len(image.shape) == 2:
            return True

        if len(image.shape) == 3 and image.shape[2] == 1:
            return True

        return False

    @staticmethod
    def get_source_image(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return the image that will be converted.

        if image_data.perspective_image is not None:
            return image_data.perspective_image

        return image_data.image

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Remove grayscale result.

        image_data.grayscale_image = None

        image_data.processing_history.pop(
            "Grayscale",
            None,
        )

        logger.info(
            "Grayscale image removed."
        )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return grayscale statistics.

        if image_data.grayscale_image is None:

            raise ImageProcessingError(
                "Grayscale image not found."
            )

        gray = image_data.grayscale_image

        return {

            "Minimum":
                int(gray.min()),

            "Maximum":
                int(gray.max()),

            "Mean":
                round(
                    float(gray.mean()),
                    2,
                ),

            "Standard Deviation":
                round(
                    float(gray.std()),
                    2,
                ),

            "Width":
                gray.shape[1],

            "Height":
                gray.shape[0],
        }

    @staticmethod
    def copy(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return a copy of the grayscale image.

        if image_data.grayscale_image is None:

            raise ImageProcessingError(
                "Grayscale image not available."
            )

        return image_data.grayscale_image.copy()