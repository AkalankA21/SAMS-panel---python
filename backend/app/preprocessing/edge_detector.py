from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class EdgeDetector:
    
    # Performs edge detection on attendance sheet images.

    DEFAULT_BLUR_KERNEL = (5, 5)
    DEFAULT_THRESHOLD1 = 50
    DEFAULT_THRESHOLD2 = 150

    @staticmethod
    def detect(
        image_data: ImageData,
        threshold1: int = DEFAULT_THRESHOLD1,
        threshold2: int = DEFAULT_THRESHOLD2,
        blur_kernel: tuple[int, int] = DEFAULT_BLUR_KERNEL,
    ) -> np.ndarray:
        
        # Detect edges using Canny.

        try:

            logger.info("Starting edge detection.")

            if image_data.image is None:
                raise ImageProcessingError(
                    "No image available."
                )

            image = image_data.image.copy()

            # ----------------------------
            # Convert to grayscale
            # ----------------------------

            if len(image.shape) == 3:

                gray = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2GRAY,
                )

            else:

                gray = image

            image_data.grayscale_image = gray

            logger.info("Grayscale conversion completed.")

            # ----------------------------
            # Gaussian Blur
            # ----------------------------

            blurred = cv2.GaussianBlur(
                gray,
                blur_kernel,
                0,
            )

            image_data.blurred_image = blurred

            logger.info("Gaussian blur applied.")

            # ----------------------------
            # Canny
            # ----------------------------

            edges = cv2.Canny(
                blurred,
                threshold1,
                threshold2,
            )

            image_data.processing_history["Edges"] = edges

            image_data.set_stage("Edge Detection")

            logger.info(
                "Edge detection completed."
            )

            return edges

        except Exception as ex:

            logger.error(ex)

            raise ImageProcessingError(
                f"Edge detection failed: {ex}"
            ) from ex

    @staticmethod
    def auto_detect(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Automatic edge detection using image median.

        try:

            image = image_data.image

            if len(image.shape) == 3:

                gray = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2GRAY,
                )

            else:

                gray = image

            median = np.median(gray)

            lower = int(
                max(
                    0,
                    0.66 * median,
                )
            )

            upper = int(
                min(
                    255,
                    1.33 * median,
                )
            )

            logger.info(
                f"Auto thresholds : {lower} {upper}"
            )

            return EdgeDetector.detect(
                image_data,
                threshold1=lower,
                threshold2=upper,
            )

        except Exception as ex:

            logger.error(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def dilate(
        edges: np.ndarray,
        iterations: int = 1,
    ) -> np.ndarray:
        
        # Dilate edges.

        kernel = np.ones(
            (3, 3),
            np.uint8,
        )

        return cv2.dilate(
            edges,
            kernel,
            iterations=iterations,
        )

    @staticmethod
    def erode(
        edges: np.ndarray,
        iterations: int = 1,
    ) -> np.ndarray:
        """
        Erode edges.
        """

        kernel = np.ones(
            (3, 3),
            np.uint8,
        )

        return cv2.erode(
            edges,
            kernel,
            iterations=iterations,
        )