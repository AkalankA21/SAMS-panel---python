from pathlib import Path

import cv2
import matplotlib.pyplot as plt

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class CellVisualizer:
    
    # Visualize extracted cells.

    @staticmethod
    def show(
        image_data: ImageData,
        index: int,
    ) -> None:
        
        # Display a single extracted cell.

        if image_data.valid_cells is None:

            logger.warning("No extracted cells available for display.")
            return

        if index >= len(image_data.valid_cells):

            logger.warning("Invalid cell index for display; no cell shown.")
            return

        cell = image_data.valid_cells[index]

        image = cv2.cvtColor(
            cell["image"],
            cv2.COLOR_BGR2RGB,
        )

        plt.figure(figsize=(4, 4))

        plt.imshow(image)

        plt.title(

            f"Row {cell['row']}  "
            f"Column {cell['column']}"

        )

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def grid(
        image_data: ImageData,
        columns: int = 5,
    ) -> None:
        
        # Display all extracted cells.

        if image_data.valid_cells is None:

            logger.warning("No extracted cells available for grid view.")
            return

        cells = image_data.valid_cells

        total = len(cells)

        rows = (total + columns - 1) // columns

        plt.figure(
            figsize=(
                columns * 3,
                rows * 3,
            )
        )

        for index, cell in enumerate(cells):

            plt.subplot(
                rows,
                columns,
                index + 1,
            )

            image = cv2.cvtColor(
                cell["image"],
                cv2.COLOR_BGR2RGB,
            )

            plt.imshow(image)

            plt.title(
                f"{cell['row']},{cell['column']}"
            )

            plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def comparison(
        image_data: ImageData,
        index: int,
    ) -> None:
        
        # Compare original image and cropped cell.

        if image_data.cells is None:

            raise ImageProcessingError(
                "Cells unavailable."
            )

        cell = image_data.cells[index]

        original = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        original = original.copy()

        x, y, w, h = cell["bbox"]

        cv2.rectangle(

            original,

            (x, y),

            (x + w, y + h),

            (0, 255, 0),

            2,

        )

        original = cv2.cvtColor(

            original,

            cv2.COLOR_BGR2RGB,

        )

        cropped = cv2.cvtColor(

            cell["image"],

            cv2.COLOR_BGR2RGB,

        )

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)

        plt.imshow(original)

        plt.title("Original")

        plt.axis("off")

        plt.subplot(1, 2, 2)

        plt.imshow(cropped)

        plt.title("Extracted Cell")

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def save_all(
        image_data: ImageData,
        output_directory: str | Path,
    ) -> None:
        
        # Save all extracted cells.

        if image_data.valid_cells is None:

            logger.warning("No extracted cells available for saving.")
            return

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        for cell in image_data.valid_cells:

            filename = (

                f"cell_"

                f"{cell['row']:02d}_"

                f"{cell['column']:02d}.png"

            )

            cv2.imwrite(

                str(
                    output_directory /
                    filename
                ),

                cell["image"],

            )

        logger.info(
            "Extracted cells saved."
        )

    @staticmethod
    def information(
        image_data: ImageData,
    ) -> dict:
        
        # Return extraction information.

        if image_data.valid_cells is None:

            return {"Cells": 0, "Rows": 0, "Columns": 0}

        return {

            "Cells":
                len(
                    image_data.valid_cells
                ),

            "Rows":
                len({

                    cell["row"]

                    for cell in image_data.valid_cells

                }),

            "Columns":
                len({

                    cell["column"]

                    for cell in image_data.valid_cells

                }),

        }

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> None:
        
        # Print cells summary.

        info = CellVisualizer.information(image_data)
        for key, value in info.items():
            print(f"{key:<25}: {value}")