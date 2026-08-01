from __future__ import annotations

import time

from app.models.image_data import ImageData
from app.preprocessing.brightness_adjuster import (
    BrightnessAdjuster,
)
from app.preprocessing.contrast_enhancer import (
    ContrastEnhancer,
)
from app.preprocessing.grayscale_converter import (
    GrayscaleConverter,
)
from app.preprocessing.histogram_equalizer import (
    HistogramEqualizer,
)
from app.utils.exceptions import ImageProcessingError
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class GrayscaleService:
    
    # Service layer for grayscale processing.

    @staticmethod
    def process(
        image_data: ImageData,
    ) -> ImageData:
        
        # Execute the complete grayscale pipeline.

        try:

            logger.info(
                "Starting grayscale pipeline."
            )

            start = time.perf_counter()

            GrayscaleConverter.convert(
                image_data
            )

            BrightnessAdjuster.adjust(
                image_data
            )

            ContrastEnhancer.enhance(
                image_data
            )

            HistogramEqualizer.equalize(
                image_data
            )

            HistogramEqualizer.clahe(
                image_data
            )

            elapsed = (
                time.perf_counter() - start
            )

            logger.info(
                f"Pipeline completed in "
                f"{elapsed:.3f} seconds."
            )

            return image_data

        except Exception as ex:

            logger.exception(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> dict:
        
        # Return processed images for the GUI.

        return {

            "Original":
                image_data.image,

            "Perspective":
                image_data.perspective_image,

            "Grayscale":
                image_data.grayscale_image,

            "Brightness":
                image_data.brightness_image,

            "Contrast":
                image_data.contrast_image,

            "Equalized":
                image_data.equalized_image,

            "CLAHE":
                image_data.clahe_image,
        }

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return statistics for each stage.

        images = {
            "Grayscale": image_data.grayscale_image,
            "Brightness": image_data.brightness_image,
            "Contrast": image_data.contrast_image,
            "Equalized": image_data.equalized_image,
            "CLAHE": image_data.clahe_image,
        }

        return {
            name: ImageStatistics.basic(img)
            for name, img in images.items()
            if img is not None
        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset all grayscale processing results.

        image_data.grayscale_image = None
        image_data.brightness_image = None
        image_data.contrast_image = None
        image_data.equalized_image = None
        image_data.clahe_image = None

        for key in (
            "Grayscale",
            "Brightness",
            "Contrast",
            "Equalization",
            "CLAHE",
        ):
            image_data.processing_history.pop(
                key,
                None,
            )

        image_data.set_stage("Perspective Correction")

        logger.info(
            "Grayscale pipeline reset."
        )

    @staticmethod
    def is_processed(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether grayscale conversion has been completed.

        return image_data.grayscale_image is not None