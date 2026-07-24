from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from app.models.image_data import ImageData
from app.preprocessing.grid_generator import GridGenerator
from app.preprocessing.table_detector import TableDetector
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class TableVisualizer:
    
    # Visualize detected attendance table.

    @staticmethod
    def original(
        image_data: ImageData,
    ) -> np.ndarray:

        if image_data.image is None:

            raise ImageProcessingError(
                "Original image not available."
            )

        return image_data.image.copy()

    @staticmethod
    def contour(
        image_data: ImageData,
    ) -> np.ndarray:

        return TableDetector.overlay(
            image_data
        )

    @staticmethod
    def bounding_box(
        image_data: ImageData,
    ) -> np.ndarray:

        return TableDetector.draw_bbox(
            image_data
        )

    @staticmethod
    def grid(
        image_data: ImageData,
    ) -> np.ndarray:

        return GridGenerator.overlay(
            image_data
        )

    @staticmethod
    def cropped_table(
        image_data: ImageData,
    ) -> np.ndarray:

        return TableDetector.extract(
            image_data
        )

    @staticmethod
    def mask(
        image_data: ImageData,
    ) -> np.ndarray:

        if image_data.table_mask is None:

            raise ImageProcessingError(
                "Table mask unavailable."
            )

        return image_data.table_mask.copy()

    @staticmethod
    def show(
        image: np.ndarray,
        title: str = "Visualization",
        figsize=(8, 6),
    ) -> None:

        plt.figure(figsize=figsize)

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

    @staticmethod
    def comparison(
        image_data: ImageData,
    ) -> None:

        original = TableVisualizer.original(
            image_data
        )

        contour = TableVisualizer.contour(
            image_data
        )

        bbox = TableVisualizer.bounding_box(
            image_data
        )

        grid = TableVisualizer.grid(
            image_data
        )

        plt.figure(figsize=(14, 10))

        plt.subplot(221)

        plt.imshow(
            cv2.cvtColor(
                original,
                cv2.COLOR_BGR2RGB,
            )
        )

        plt.title("Original")

        plt.axis("off")

        plt.subplot(222)

        plt.imshow(
            cv2.cvtColor(
                contour,
                cv2.COLOR_BGR2RGB,
            )
        )

        plt.title("Detected Contour")

        plt.axis("off")

        plt.subplot(223)

        plt.imshow(
            cv2.cvtColor(
                bbox,
                cv2.COLOR_BGR2RGB,
            )
        )

        plt.title("Bounding Box")

        plt.axis("off")

        plt.subplot(224)

        plt.imshow(
            cv2.cvtColor(
                grid,
                cv2.COLOR_BGR2RGB,
            )
        )

        plt.title("Generated Grid")

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def save(
        image: np.ndarray,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(output_path),
            image,
        )

        logger.info(
            f"Saved visualization -> {output_path}"
        )

    @staticmethod
    def save_all(
        image_data: ImageData,
        output_directory: str | Path,
    ) -> None:

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        images = {

            "01_original.png":
                TableVisualizer.original(
                    image_data
                ),

            "02_contour.png":
                TableVisualizer.contour(
                    image_data
                ),

            "03_bbox.png":
                TableVisualizer.bounding_box(
                    image_data
                ),

            "04_grid.png":
                TableVisualizer.grid(
                    image_data
                ),

            "05_table.png":
                TableVisualizer.cropped_table(
                    image_data
                ),

            "06_mask.png":
                TableVisualizer.mask(
                    image_data
                ),

        }

        for name, image in images.items():

            cv2.imwrite(

                str(
                    output_directory / name
                ),

                image,

            )

        logger.info(
            "All table visualizations saved."
        )

    @staticmethod
    def information(
        image_data: ImageData,
    ) -> dict:

        stats = TableDetector.statistics(
            image_data
        )

        stats["Grid Valid"] = (
            GridGenerator.validate(
                image_data
            )
        )

        stats["Cells"] = (
            GridGenerator.cell_count(
                image_data
            )
        )

        return stats

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> None:
        
        # Print table summary.

        info = TableVisualizer.information(image_data)
        for key, value in info.items():
            print(f"{key:<25}: {value}")