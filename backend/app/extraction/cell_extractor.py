from __future__ import annotations

from typing import Any

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class CellExtractor:
    
    # Extract individual cells from the detected attendance table.

    MIN_CELL_WIDTH = 10
    MIN_CELL_HEIGHT = 10

    @staticmethod
    def extract(
        image_data: ImageData,
    ) -> list[dict[str, Any]]:
        
        # Extract all table cells.

        logger.info(
            "Starting cell extraction..."
        )

        if image_data.image is None:

            raise ImageProcessingError(
                "Original image unavailable."
            )

        if image_data.table_cells is None:

            raise ImageProcessingError(
                "No table cells found."
            )

        extracted_cells = []

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image

        for index, cell in enumerate(
            image_data.table_cells,
            start=1,
        ):

            bbox = cell["bbox"]

            x, y, w, h = bbox

            if (
                w < CellExtractor.MIN_CELL_WIDTH
                or
                h < CellExtractor.MIN_CELL_HEIGHT
            ):
                continue

            roi = image[
                y:y + h,
                x:x + w,
            ].copy()

            extracted_cells.append(
                {
                    "id": index,
                    "row": cell.get("row", CellExtractor._row(
                        image_data,
                        cell,
                    )),
                    "column": cell.get("column", CellExtractor._column(
                        image_data,
                        cell,
                    )),
                    "bbox": bbox,
                    "image": roi,
                    "width": w,
                    "height": h,
                    "area": w * h,
                }
            )

        image_data.cells = extracted_cells
        image_data.cropped_cells = [
            cell["image"]
            for cell in extracted_cells
        ]

        image_data.processing_history[
            "Cell Extraction"
        ] = len(extracted_cells)

        image_data.set_stage(
            "Cell Extraction"
        )

        logger.info(
            "%d cells extracted.",
            len(extracted_cells),
        )

        return extracted_cells

    @staticmethod
    def extract_single(
        image_data: ImageData,
        index: int,
    ) -> np.ndarray:
        
        # Return one extracted cell image.

        if image_data.cells is None:

            raise ImageProcessingError(
                "Cells have not been extracted."
            )

        if (
            index < 0
            or
            index >= len(image_data.cells)
        ):

            raise IndexError(
                "Invalid cell index."
            )

        return image_data.cells[index][
            "image"
        ]

    @staticmethod
    def _row(
        image_data: ImageData,
        cell: dict,
    ) -> int:
        
        # Estimate row index.

        if image_data.grid_rows is None:

            return -1

        _, y, _, h = cell["bbox"]

        center = y + h // 2

        for index, row in enumerate(
            image_data.grid_rows
        ):

            row_y = int(
                sum(
                    point[1]
                    for point in row
                ) / len(row)
            )

            if abs(center - row_y) <= 10:

                return index

        return -1

    @staticmethod
    def _column(
        image_data: ImageData,
        cell: dict,
    ) -> int:
        
        # Estimate column index.

        if image_data.grid_columns is None:

            return -1

        x, _, w, _ = cell["bbox"]

        center = x + w // 2

        for index, column in enumerate(
            image_data.grid_columns
        ):

            column_x = int(
                sum(
                    point[0]
                    for point in column
                ) / len(column)
            )

            if abs(center - column_x) <= 10:

                return index

        return -1

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Return extracted cell count.

        if image_data.cells is None:

            return 0

        return len(image_data.cells)

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset extracted cells.

        image_data.cells = None
        image_data.cropped_cells = None

        image_data.processing_history.pop(
            "Cell Extraction",
            None,
        )

        logger.info(
            "Cell extraction reset."
        )