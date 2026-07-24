from __future__ import annotations

import numpy as np

from app.models.image_data import ImageData
from app.preprocessing.edge_detector import EdgeDetector
from app.preprocessing.contour_detector import ContourDetector
from app.preprocessing.warp_transform import WarpTransform
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class PerspectiveCorrector:
    
    # Complete perspective correction pipeline.

    @staticmethod
    def correct(
        image_data: ImageData,
        auto_threshold: bool = True,
    ) -> ImageData:
        
        # Detect and correct the perspective of the attendance sheet.

        try:

            logger.info(
                "========== Perspective Correction =========="
            )

            # ---------------------------------------
            # Edge Detection
            # ---------------------------------------

            if auto_threshold:

                edges = EdgeDetector.auto_detect(
                    image_data
                )

            else:

                edges = EdgeDetector.detect(
                    image_data
                )

            image_data.processing_history["Edges"] = edges

            logger.info(
                "Edge detection completed."
            )

            # ---------------------------------------
            # Contour Detection
            # ---------------------------------------

            contour = (
                ContourDetector.find_document_contour(
                    image_data,
                    edges,
                )
            )

            image_data.document_contour = contour

            logger.info(
                "Document contour detected."
            )

            # ---------------------------------------
            # Draw Contour
            # ---------------------------------------

            contour_preview = (
                ContourDetector.draw_contour(
                    image_data.image,
                    contour,
                )
            )

            image_data.processing_history[
                "Contour"
            ] = contour_preview

            # ---------------------------------------
            # Draw Corners
            # ---------------------------------------

            corner_preview = (
                WarpTransform.draw_corners(
                    image_data.image,
                    contour,
                )
            )

            image_data.processing_history[
                "Corners"
            ] = corner_preview

            # ---------------------------------------
            # Perspective Warp
            # ---------------------------------------

            corrected = WarpTransform.warp(
                image_data,
                contour,
            )

            image_data.processing_history[
                "Perspective"
            ] = corrected

            image_data.set_stage(
                "Perspective Correction"
            )

            logger.info(
                "Perspective correction finished."
            )

            return image_data

        except Exception as ex:

            logger.error(ex)

            raise ImageProcessingError(
                f"Perspective correction failed : {ex}"
            ) from ex

    @staticmethod
    def preview(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return corrected image for GUI preview.

        if image_data.perspective_image is None:

            PerspectiveCorrector.correct(
                image_data
            )

        return image_data.perspective_image

    @staticmethod
    def is_corrected(
        image_data: ImageData,
    ) -> bool:
        
        # Check whether perspective correction has already been performed.

        return (
            image_data.perspective_image
            is not None
        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        """
        Remove perspective correction results.
        """

        image_data.perspective_image = None
        image_data.document_contour = None
        image_data.ordered_corners = None

        image_data.processing_history.pop(
            "Perspective",
            None,
        )

        image_data.processing_history.pop(
            "Contour",
            None,
        )

        image_data.processing_history.pop(
            "Corners",
            None,
        )

        image_data.set_stage("Original")

        logger.info(
            "Perspective correction reset."
        )