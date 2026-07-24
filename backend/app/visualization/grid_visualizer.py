from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.models.image_data import ImageData
from app.preprocessing.grid_generator import GridGenerator
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class GridVisualizer:
    
    # Grid visualization utilities.

    @staticmethod
    def grid(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return generated grid image.

        if image_data.grid_image is None:

            return GridGenerator.create_grid_image(
                image_data
            )

        return image_data.grid_image.copy()

    @staticmethod
    def intersections(
        image_data: ImageData,
        radius: int = 4,
    ) -> np.ndarray:
        
        # Draw detected intersections.

        if image_data.image is None:

            raise ImageProcessingError(
                "Original image unavailable."
            )

        if image_data.intersections is None:

            raise ImageProcessingError(
                "Intersections unavailable."
            )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        image = image.copy()

        for x, y in image_data.intersections:

            cv2.circle(
                image,
                (x, y),
                radius,
                (0, 0, 255),
                -1,
            )

        return image

    @staticmethod
    def cells(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Draw every detected cell.

        if image_data.image is None:

            raise ImageProcessingError(
                "Original image unavailable."
            )

        if image_data.table_cells is None:

            raise ImageProcessingError(
                "Cells unavailable."
            )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        image = image.copy()

        for cell in image_data.table_cells:

            x, y, w, h = cell["bbox"]

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )

        return image

    @staticmethod
    def numbered_cells(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Draw numbered cells.

        if image_data.image is None:

            raise ImageProcessingError(
                "Original image unavailable."
            )

        if image_data.table_cells is None:

            raise ImageProcessingError(
                "Cells unavailable."
            )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        image = image.copy()

        for index, cell in enumerate(
            image_data.table_cells,
            start=1,
        ):

            x, y, w, h = cell["bbox"]

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2,
            )

            cv2.putText(
                image,
                str(index),
                (x + 5, y + 18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
            )

        return image

    @staticmethod
    def overlay(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Grid overlay.

        return GridGenerator.overlay(
            image_data
        )

    @staticmethod
    def comparison(
        image_data: ImageData,
    ) -> None:
        
        # Display visualization comparison.

        images = [

            (
                image_data.perspective_image if image_data.perspective_image is not None else image_data.image,
                "Original",
            ),

            (
                GridVisualizer.grid(
                    image_data
                ),
                "Grid",
            ),

            (
                GridVisualizer.intersections(
                    image_data
                ),
                "Intersections",
            ),

            (
                GridVisualizer.numbered_cells(
                    image_data
                ),
                "Cells",
            ),

        ]

        plt.figure(figsize=(14, 10))

        for i, (img, title) in enumerate(
            images,
            start=1,
        ):

            plt.subplot(
                2,
                2,
                i,
            )

            if len(img.shape) == 2:

                plt.imshow(
                    img,
                    cmap="gray",
                )

            else:

                plt.imshow(

                    cv2.cvtColor(

                        img,

                        cv2.COLOR_BGR2RGB,

                    )

                )

            plt.title(title)

            plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def save(
        image: np.ndarray,
        output_path: str | Path,
    ) -> None:
        
        # Save visualization.

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(output_path),
            image,
        )

        logger.info(
            f"Saved -> {output_path}"
        )

    @staticmethod
    def save_all(
        image_data: ImageData,
        output_directory: str | Path,
    ) -> None:
        
        # Save every visualization.

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        images = {

            "01_grid.png":

                GridVisualizer.grid(
                    image_data
                ),

            "02_intersections.png":

                GridVisualizer.intersections(
                    image_data
                ),

            "03_cells.png":

                GridVisualizer.cells(
                    image_data
                ),

            "04_numbered_cells.png":

                GridVisualizer.numbered_cells(
                    image_data
                ),

            "05_overlay.png":

                GridVisualizer.overlay(
                    image_data
                ),

        }

        for filename, image in images.items():

            cv2.imwrite(

                str(

                    output_directory /
                    filename

                ),

                image,

            )

        logger.info(
            "Grid visualizations saved."
        )

    @staticmethod
    def information(
        image_data: ImageData,
    ) -> dict:
        
        # Grid information.

        return {

            "Rows":

                len(
                    image_data.grid_rows
                )
                if image_data.grid_rows
                else 0,

            "Columns":

                len(
                    image_data.grid_columns
                )
                if image_data.grid_columns
                else 0,

            "Intersections":

                len(
                    image_data.intersections
                )
                if image_data.intersections
                else 0,

            "Cells":

                len(
                    image_data.table_cells
                )
                if image_data.table_cells
                else 0,

            "Grid Valid":

                GridGenerator.validate(
                    image_data
                ),

        }

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> None:
        
        # Print grid summary.

        info = GridVisualizer.information(image_data)
        for key, value in info.items():
            print(f"{key:<25}: {value}")

    @staticmethod
    def show(
        image: np.ndarray,
        title="Grid Visualization",
    ) -> None:
        
        # Display image.

        plt.figure(figsize=(8, 6))

        if len(image.shape) == 2:

            plt.imshow(
                image,
                cmap="gray",
            )

        else:

            plt.imshow(

                cv2.cvtColor(

                    image,

                    cv2.COLOR_BGR2RGB,

                )

            )

        plt.title(title)

        plt.axis("off")

        plt.tight_layout()

        plt.show()