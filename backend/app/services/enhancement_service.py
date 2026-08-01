from __future__ import annotations

import time

from app.models.image_data import ImageData

from app.preprocessing.median_filter import MedianFilter
from app.preprocessing.gaussian_filter import GaussianFilter
from app.preprocessing.bilateral_filter import BilateralFilter
from app.preprocessing.denoiser import Denoiser
from app.preprocessing.morphology import Morphology

from app.utils.exceptions import ImageProcessingError
from app.utils.image_statistics import ImageStatistics
from app.utils.logger import logger


class EnhancementService:
    
    # Service class for image enhancement.

    @staticmethod
    def process(
        image_data: ImageData,
        use_median: bool = True,
        use_gaussian: bool = True,
        use_bilateral: bool = True,
        use_denoiser: bool = True,
        use_opening: bool = True,
        use_closing: bool = True,
    ) -> ImageData:
        
        # Execute enhancement pipeline.

        try:

            logger.info(
                "Starting enhancement pipeline."
            )

            start = time.perf_counter()

            if use_median:
                MedianFilter.apply(image_data)

            if use_gaussian:
                GaussianFilter.apply(image_data)

            if use_bilateral:
                BilateralFilter.apply(image_data)

            if use_denoiser:
                Denoiser.apply(image_data)

            if use_opening:
                Morphology.opening(image_data)

            if use_closing:
                Morphology.closing(image_data)

            elapsed = (
                time.perf_counter() - start
            )

            logger.info(
                f"Enhancement completed in "
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
        
        # Return all enhancement images.

        return {

            "Median":
                image_data.median_image,

            "Gaussian":
                image_data.gaussian_image,

            "Bilateral":
                image_data.bilateral_image,

            "Denoised":
                image_data.denoised_image,

            "Opening":
                image_data.opened_image,

            "Closing":
                image_data.closed_image,
        }

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return statistics for each stage.

        images = {

            "Median":
                image_data.median_image,

            "Gaussian":
                image_data.gaussian_image,

            "Bilateral":
                image_data.bilateral_image,

            "Denoised":
                image_data.denoised_image,

            "Opening":
                image_data.opened_image,

            "Closing":
                image_data.closed_image,
        }

        results = {}

        for stage, image in images.items():

            if image is not None:

                results[stage] = (
                    ImageStatistics.basic(image)
                )

        return results

    @staticmethod
    def processing_history(
        image_data: ImageData,
    ) -> list[str]:
        
        # Return completed enhancement stages.

        history = []

        for stage in (

            "Median",

            "Gaussian",

            "Bilateral",

            "Denoised",

            "Opening",

            "Closing",
        ):

            if stage in image_data.processing_history:

                history.append(stage)

        return history

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset enhancement pipeline.

        MedianFilter.reset(image_data)

        GaussianFilter.reset(image_data)

        BilateralFilter.reset(image_data)

        Denoiser.reset(image_data)

        Morphology.reset(image_data)

        logger.info(
            "Enhancement pipeline reset."
        )

    @staticmethod
    def is_processed(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether enhancement has been completed.

        return any(

            image is not None

            for image in (

                image_data.median_image,

                image_data.gaussian_image,

                image_data.bilateral_image,

                image_data.denoised_image,

                image_data.opened_image,

                image_data.closed_image,
            )
        )

    @staticmethod
    def latest_image(
        image_data: ImageData,
    ):
        
        # Return latest enhancement result.

        if image_data.closed_image is not None:
            return image_data.closed_image

        if image_data.opened_image is not None:
            return image_data.opened_image

        if image_data.denoised_image is not None:
            return image_data.denoised_image

        if image_data.bilateral_image is not None:
            return image_data.bilateral_image

        if image_data.gaussian_image is not None:
            return image_data.gaussian_image

        if image_data.median_image is not None:
            return image_data.median_image

        return None