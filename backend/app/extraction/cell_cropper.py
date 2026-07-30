from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class CellCropper:
    
    # Crop and refine extracted cells.

    DEFAULT_PADDING = 3

    @staticmethod
    def crop(
        image_data: ImageData,
        padding: int = DEFAULT_PADDING,
    ) -> list:
        
        # Crop every detected cell.

        logger.info("Cropping extracted cells...")

        if image_data.image is None:
            raise ImageProcessingError(
                "Original image unavailable."
            )

        if image_data.cells is None:
            raise ImageProcessingError(
                "Cells have not been extracted."
            )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image

        height, width = image.shape[:2]

        cropped_cells = []

        for cell in image_data.cells:

            x, y, w, h = cell["bbox"]

            x1 = max(0, x + padding)
            y1 = max(0, y + padding)

            x2 = min(width, x + w - padding)
            y2 = min(height, y + h - padding)

            roi = image[
                y1:y2,
                x1:x2
            ].copy()

            cell["image"] = roi

            cell["crop_bbox"] = (
                x1,
                y1,
                x2 - x1,
                y2 - y1,
            )

            cropped_cells.append(roi)

        image_data.cropped_cells = cropped_cells

        image_data.processing_history[
            "Cell Cropping"
        ] = len(cropped_cells)

        image_data.set_stage(
            "Cell Cropping"
        )

        logger.info(
            "%d cells cropped.",
            len(cropped_cells),
        )

        return cropped_cells

    @staticmethod
    def resize(
        image,
        width: int = 128,
        height: int = 64,
    ):
        
        # Resize a cell.

        return cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )

    @staticmethod
    def resize_all(
        image_data: ImageData,
        width: int = 128,
        height: int = 64,
    ):
        
        # Resize every cropped cell.

        if image_data.cropped_cells is None:

            raise ImageProcessingError(
                "No cropped cells available."
            )

        resized = []

        for image in image_data.cropped_cells:

            resized.append(

                CellCropper.resize(
                    image,
                    width,
                    height,
                )

            )

        image_data.cropped_cells = resized

        logger.info(
            "All cells resized."
        )

        return resized

    @staticmethod
    def remove_border(
        image,
        pixels: int = 2,
    ):
        
        # Remove outer border from a cell.

        h, w = image.shape[:2]

        return image[
            pixels:h - pixels,
            pixels:w - pixels,
        ]

    @staticmethod
    def remove_borders(
        image_data: ImageData,
        pixels: int = 2,
    ):
        
        # Remove borders from every cell.

        if image_data.cropped_cells is None:

            raise ImageProcessingError(
                "No cropped cells available."
            )

        cleaned = []

        for image in image_data.cropped_cells:

            cleaned.append(

                CellCropper.remove_border(
                    image,
                    pixels,
                )

            )

        image_data.cropped_cells = cleaned

        logger.info(
            "Borders removed from all cells."
        )

        return cleaned

    @staticmethod
    def dimensions(
        image,
    ) -> tuple:
        
        # Return image dimensions.

        h, w = image.shape[:2]

        return w, h

    @staticmethod
    def average_size(
        image_data: ImageData,
    ) -> tuple:
        
        # Average cell size.

        if image_data.cropped_cells is None:

            return 0, 0

        widths = []
        heights = []

        for image in image_data.cropped_cells:

            w, h = CellCropper.dimensions(
                image
            )

            widths.append(w)

            heights.append(h)

        return (

            round(sum(widths) / len(widths), 2),

            round(sum(heights) / len(heights), 2),

        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ):
        
        # Reset cropped cells.

        image_data.cropped_cells = None

        image_data.processing_history.pop(
            "Cell Cropping",
            None,
        )

        logger.info(
            "Cell cropping reset."
        )