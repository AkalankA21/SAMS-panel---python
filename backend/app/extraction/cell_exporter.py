from __future__ import annotations

from pathlib import Path
import csv

import cv2

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class CellExporter:
    
    # Export validated cells.

    @staticmethod
    def export(
        image_data: ImageData,
    ) -> list:
        
        # Return exported cells.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        logger.info(
            "Exporting cells..."
        )

        return image_data.valid_cells

    @staticmethod
    def export_images(
        image_data: ImageData,
        output_directory: str | Path,
        prefix: str = "cell",
    ) -> int:
        
        # Save every validated cell as an image.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        count = 0

        for cell in image_data.valid_cells:

            image = cell["image"]

            filename = (

                f"{prefix}_"

                f"{cell['row']:02d}_"

                f"{cell['column']:02d}.png"

            )

            cv2.imwrite(

                str(
                    output_directory /
                    filename
                ),

                image,

            )

            count += 1

        logger.info(
            "%d cell images exported.",
            count,
        )

        return count

    @staticmethod
    def export_metadata(
        image_data: ImageData,
        output_file: str | Path,
    ) -> None:
        
        # Export metadata to CSV.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(

            output_file,

            "w",

            newline="",

            encoding="utf-8",

        ) as csv_file:

            writer = csv.writer(
                csv_file
            )

            writer.writerow(

                [

                    "ID",

                    "Row",

                    "Column",

                    "Width",

                    "Height",

                    "Area",

                ]

            )

            for cell in image_data.valid_cells:

                x, y, w, h = cell["bbox"]

                writer.writerow(

                    [

                        cell["id"],

                        cell["row"],

                        cell["column"],

                        w,

                        h,

                        w * h,

                    ]

                )

        logger.info(
            "Metadata exported."
        )

    @staticmethod
    def export_dictionary(
        image_data: ImageData,
    ) -> dict:
        
        # Export dictionary.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        return {

            cell["id"]: {

                "row": cell["row"],

                "column": cell["column"],

                "bbox": cell["bbox"],

                "width": cell["width"],

                "height": cell["height"],

                "area": cell["area"],

            }

            for cell in image_data.valid_cells

        }

    @staticmethod
    def export_summary(
        image_data: ImageData,
    ) -> dict:
        
        # Export summary information.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        rows = len({

            cell["row"]

            for cell in image_data.valid_cells

        })

        columns = len({

            cell["column"]

            for cell in image_data.valid_cells

        })

        return {

            "Total Cells":

                len(
                    image_data.valid_cells
                ),

            "Rows":

                rows,

            "Columns":

                columns,

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset exporter.

        logger.info(
            "Cell exporter reset."
        )