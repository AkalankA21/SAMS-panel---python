from __future__ import annotations

import statistics

from app.models.image_data import ImageData
from app.utils.logger import logger


class CellStatistics:
    
    # Calculate statistics for extracted cells.

    @staticmethod
    def calculate(
        image_data: ImageData,
    ) -> dict:
        
        # Calculate cell statistics.

        if image_data.valid_cells is None:

            stats = {

                "Total Cells": 0,
                "Average Width": 0,
                "Average Height": 0,
                "Average Area": 0,
                "Minimum Area": 0,
                "Maximum Area": 0,
                "Rows": 0,
                "Columns": 0,

            }

            image_data.cell_statistics = stats

            return stats

        widths = []
        heights = []
        areas = []

        rows = set()
        columns = set()

        for cell in image_data.valid_cells:

            _, _, width, height = cell["bbox"]

            widths.append(width)

            heights.append(height)

            areas.append(width * height)

            rows.add(cell["row"])

            columns.add(cell["column"])

        if not widths:
            stats = {
                "Total Cells": 0,
                "Rows": 0,
                "Columns": 0,
                "Average Width": 0,
                "Average Height": 0,
                "Average Area": 0,
                "Minimum Area": 0,
                "Maximum Area": 0,
                "Median Width": 0,
                "Median Height": 0,
                "Median Area": 0,
                "Width Std Dev": 0,
                "Height Std Dev": 0,
                "Area Std Dev": 0,
            }
        else:
            stats = {
                "Total Cells": len(image_data.valid_cells),
                "Rows": len(rows),
                "Columns": len(columns),
                "Average Width": round(
                    statistics.mean(widths), 2
                ),
                "Average Height": round(
                    statistics.mean(heights), 2
                ),
                "Average Area": round(
                    statistics.mean(areas), 2
                ),
                "Minimum Area": min(areas),
                "Maximum Area": max(areas),
                "Median Width": round(
                    statistics.median(widths), 2
                ),
                "Median Height": round(
                    statistics.median(heights), 2
                ),
                "Median Area": round(
                    statistics.median(areas), 2
                ),
                "Width Std Dev": round(
                    statistics.pstdev(widths), 2
                ),
                "Height Std Dev": round(
                    statistics.pstdev(heights), 2
                ),
                "Area Std Dev": round(
                    statistics.pstdev(areas), 2
                ),
            }

        image_data.cell_statistics = stats

        logger.info(
            "Cell statistics calculated."
        )

        return stats

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted statistics.

        stats = CellStatistics.calculate(
            image_data
        )

        return (
            "\n"
            "========== Cell Statistics ==========\n"
            f"Total Cells     : {stats['Total Cells']}\n"
            f"Rows            : {stats['Rows']}\n"
            f"Columns         : {stats['Columns']}\n"
            f"Average Width   : {stats['Average Width']}\n"
            f"Average Height  : {stats['Average Height']}\n"
            f"Average Area    : {stats['Average Area']}\n"
            f"Minimum Area    : {stats['Minimum Area']}\n"
            f"Maximum Area    : {stats['Maximum Area']}\n"
            f"Width Std Dev   : {stats['Width Std Dev']}\n"
            f"Height Std Dev  : {stats['Height Std Dev']}\n"
            f"Area Std Dev    : {stats['Area Std Dev']}\n"
        )

    @staticmethod
    def print(
        image_data: ImageData,
    ) -> None:
        
        # Print statistics.

        print(
            CellStatistics.summary(
                image_data
            )
        )

    @staticmethod
    def export(
        image_data: ImageData,
    ) -> dict:
        
        # Return cached statistics.

        if image_data.cell_statistics is None:

            return CellStatistics.calculate(
                image_data
            )

        return image_data.cell_statistics

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset statistics.

        image_data.cell_statistics = None

        logger.info(
            "Cell statistics reset."
        )