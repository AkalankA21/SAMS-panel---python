from __future__ import annotations

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class CellSorter:
    
    # Sort extracted cells.

    @staticmethod
    def sort(
        image_data: ImageData,
    ) -> list:
        
        # Sort cells by row and column.

        logger.info(
            "Sorting extracted cells..."
        )

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        sorted_cells = sorted(

            image_data.valid_cells,

            key=lambda cell: (

                cell["row"],

                cell["column"],

            ),

        )

        image_data.valid_cells = sorted_cells

        image_data.processing_history[
            "Cell Sorting"
        ] = len(sorted_cells)

        image_data.set_stage(
            "Cell Sorting"
        )

        logger.info(
            "%d cells sorted.",
            len(sorted_cells),
        )

        return sorted_cells

    @staticmethod
    def sort_by_position(
        image_data: ImageData,
    ) -> list:
        
        # Sort cells using bounding box position.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        sorted_cells = sorted(

            image_data.valid_cells,

            key=lambda cell: (

                cell["bbox"][1],

                cell["bbox"][0],

            ),

        )

        return sorted_cells

    @staticmethod
    def group_rows(
        image_data: ImageData,
    ) -> list:
        
        # Group cells into rows.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        rows = {}

        for cell in image_data.valid_cells:

            row = cell["row"]

            rows.setdefault(
                row,
                [],
            ).append(cell)

        grouped = []

        for row in sorted(rows):

            grouped.append(

                sorted(

                    rows[row],

                    key=lambda c: c["column"],

                )

            )

        return grouped

    @staticmethod
    def group_columns(
        image_data: ImageData,
    ) -> list:
        
        # Group cells into columns.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        columns = {}

        for cell in image_data.valid_cells:

            column = cell["column"]

            columns.setdefault(
                column,
                [],
            ).append(cell)

        grouped = []

        for column in sorted(columns):

            grouped.append(

                sorted(

                    columns[column],

                    key=lambda c: c["row"],

                )

            )

        return grouped

    @staticmethod
    def first_cell(
        image_data: ImageData,
    ):
        
        # Return first sorted cell.

        if not image_data.valid_cells:

            return None

        return image_data.valid_cells[0]

    @staticmethod
    def last_cell(
        image_data: ImageData,
    ):
        
        # Return last sorted cell.

        if not image_data.valid_cells:

            return None

        return image_data.valid_cells[-1]

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Cell sorting statistics.

        if image_data.valid_cells is None:

            return {

                "Rows": 0,

                "Columns": 0,

                "Cells": 0,

            }

        rows = len({

            cell["row"]

            for cell in image_data.valid_cells

        })

        columns = len({

            cell["column"]

            for cell in image_data.valid_cells

        })

        cells = len(
            image_data.valid_cells
        )

        return {

            "Rows": rows,

            "Columns": columns,

            "Cells": cells,

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset sorting stage.

        image_data.processing_history.pop(

            "Cell Sorting",

            None,

        )

        logger.info(
            "Cell sorting reset."
        )