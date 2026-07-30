from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class CellValidator:
    
    # Validate extracted cells.

    MIN_WIDTH = 20
    MIN_HEIGHT = 20
    MIN_AREA = 400
    MIN_VARIANCE = 20.0

    @staticmethod
    def validate(
        image_data: ImageData,
    ) -> list:
        
        # Validate all cropped cells.

        logger.info(
            "Validating extracted cells..."
        )

        if image_data.cells is None:

            raise ImageProcessingError(
                "Cells have not been extracted."
            )

        valid_cells = []

        for cell in image_data.cells:

            image = cell["image"]
            cell_id = cell.get("id", 0)

            is_cell_valid, reason = CellValidator.is_valid_with_reason(image)
            if is_cell_valid:

                cell["valid"] = True

                valid_cells.append(cell)

            else:

                cell["valid"] = False
                logger.info("Cell %d rejected: %s", cell_id, reason)

        image_data.valid_cells = valid_cells

        image_data.processing_history[
            "Cell Validation"
        ] = len(valid_cells)

        image_data.set_stage(
            "Cell Validation"
        )

        logger.info(
            "%d valid cells detected.",
            len(valid_cells),
        )

        return valid_cells

    @staticmethod
    def is_valid_with_reason(
        image: np.ndarray,
    ) -> tuple[bool, str]:
        
        # Validate a single cell image and return reason.

        if image is None:

            return False, "image is None"

        if image.size == 0:

            return False, "image size is 0"

        h, w = image.shape[:2]

        if w < CellValidator.MIN_WIDTH:

            return False, f"width {w} < MIN_WIDTH {CellValidator.MIN_WIDTH}"

        if h < CellValidator.MIN_HEIGHT:

            return False, f"height {h} < MIN_HEIGHT {CellValidator.MIN_HEIGHT}"

        if w * h < CellValidator.MIN_AREA:

            return False, f"area {w * h} < MIN_AREA {CellValidator.MIN_AREA}"

        # Safe conversion to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        std_val = np.std(gray)
        if std_val < 5:

            return False, f"blank cell (std {std_val:.2f} < 5)"

        variance = cv2.Laplacian(
            gray,
            cv2.CV_64F,
        ).var()
        if variance < CellValidator.MIN_VARIANCE:

            return False, f"blurry cell (variance {variance:.2f} < {CellValidator.MIN_VARIANCE})"

        return True, "Valid"

    @staticmethod
    def is_valid(
        image: np.ndarray,
    ) -> bool:
        valid, _ = CellValidator.is_valid_with_reason(image)
        return valid

    @staticmethod
    def is_blank(
        image: np.ndarray,
    ) -> bool:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        return np.std(gray) < 5

    @staticmethod
    def is_blurry(
        image: np.ndarray,
    ) -> bool:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        variance = cv2.Laplacian(
            gray,
            cv2.CV_64F,
        ).var()
        return variance < CellValidator.MIN_VARIANCE

    @staticmethod
    def rejected(
        image_data: ImageData,
    ) -> list:
        
        # Return rejected cells.

        if image_data.cells is None:

            return []

        return [

            cell

            for cell in image_data.cells

            if not cell.get(
                "valid",
                False,
            )

        ]

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Validation statistics.

        total = (
            len(image_data.cells)
            if image_data.cells
            else 0
        )

        valid = (
            len(image_data.valid_cells)
            if image_data.valid_cells
            else 0
        )

        rejected = total - valid

        accuracy = 0.0

        if total > 0:

            accuracy = round(
                valid / total * 100,
                2,
            )

        return {

            "Total Cells": total,

            "Valid Cells": valid,

            "Rejected Cells": rejected,

            "Validation Rate (%)": accuracy,

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset validation.

        image_data.valid_cells = None

        if image_data.cells:

            for cell in image_data.cells:

                cell.pop(
                    "valid",
                    None,
                )

        image_data.processing_history.pop(
            "Cell Validation",
            None,
        )

        logger.info(
            "Cell validation reset."
        )