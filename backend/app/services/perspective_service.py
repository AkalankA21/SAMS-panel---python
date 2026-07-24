from __future__ import annotations

import time

from app.models.image_data import ImageData
from app.preprocessing.perspective_corrector import (
    PerspectiveCorrector,
)
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class PerspectiveService:
    
    # Service layer for perspective correction.

    @staticmethod
    def process(
        image_data: ImageData,
    ) -> ImageData:
        
        # Perform perspective correction.

        logger.info(
            "Perspective Service Started."
        )

        start = time.perf_counter()

        try:

            result = PerspectiveCorrector.correct(
                image_data
            )

            elapsed = (
                time.perf_counter() - start
            )

            logger.info(
                f"Perspective correction completed "
                f"in {elapsed:.3f} seconds."
            )

            return result

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def preview(
        image_data: ImageData,
    ):
        
        # Return corrected image for GUI.

        logger.info(
            "Generating perspective preview."
        )

        if (
            image_data.perspective_image
            is None
        ):

            PerspectiveCorrector.correct(
                image_data
            )

        return image_data.perspective_image

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset perspective correction.

        logger.info(
            "Resetting perspective correction."
        )

        PerspectiveCorrector.reset(
            image_data
        )

    @staticmethod
    def is_processed(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether perspective correction has already been performed.

        return (
            image_data.perspective_image
            is not None
        )

    @staticmethod
    def get_processing_stage(
        image_data: ImageData,
    ) -> str:
        
        # Return current processing stage.

        return image_data.processing_stage

    @staticmethod
    def get_preview_images(
        image_data: ImageData,
    ) -> dict:
        
        # Return all perspective related images. Useful for visualization.

        return {

            "Original":
                image_data.image,

            "Grayscale":
                image_data.grayscale_image,

            "Blur":
                image_data.blurred_image,

            "Edges":
                image_data.processing_history.get(
                    "Edges"
                ),

            "Contour":
                image_data.processing_history.get(
                    "Contour"
                ),

            "Corners":
                image_data.processing_history.get(
                    "Corners"
                ),

            "Perspective":
                image_data.perspective_image,
        }

    @staticmethod
    def processing_summary(
        image_data: ImageData,
    ) -> dict:
        
        # Return processing information.

        return {

            "Filename":
                image_data.filename,

            "Resolution":
                image_data.resolution,

            "Stage":
                image_data.processing_stage,

            "Perspective Corrected":
                image_data.perspective_image
                is not None,

            "Contour Detected":
                image_data.document_contour
                is not None,

            "History":
                list(
                    image_data.processing_history.keys()
                ),
        }