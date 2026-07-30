from pathlib import Path

import cv2
import matplotlib.pyplot as plt

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class ExtractionVisualizer:
    
    # Visualize extraction pipeline.

    @staticmethod
    def comparison(
        image_data: ImageData,
    ) -> None:
        
        # Show original image and extracted cells.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "No extracted cells available."
            )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        image = image.copy()

        for cell in image_data.valid_cells:

            x, y, w, h = cell["bbox"]

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        fig = plt.figure(
            figsize=(14, 7)
        )

        plt.imshow(image)

        plt.title(
            f"Detected Cells ({len(image_data.valid_cells)})"
        )

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def numbered_cells(
        image_data: ImageData,
    ) -> None:
        
        # Draw row and column numbers.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "No extracted cells available."
            )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        image = image.copy()

        for cell in image_data.valid_cells:

            x, y, w, h = cell["bbox"]

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2,
            )

            label = (
                f"{cell['row']},"
                f"{cell['column']}"
            )

            cv2.putText(

                image,

                label,

                (x + 3, y + 18),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.45,

                (0, 0, 255),

                1,

                cv2.LINE_AA,

            )

        image = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB,

        )

        plt.figure(figsize=(14, 8))

        plt.imshow(image)

        plt.title("Cell Coordinates")

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def save_pipeline(
        image_data: ImageData,
        output_directory: str | Path,
    ) -> None:
        
        # Save extraction visualization.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "No extracted cells available."
            )

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        image = image_data.perspective_image if image_data.perspective_image is not None else image_data.image
        image = image.copy()

        for cell in image_data.valid_cells:

            x, y, w, h = cell["bbox"]

            cv2.rectangle(

                image,

                (x, y),

                (x + w, y + h),

                (0, 255, 0),

                2,

            )

            cv2.putText(

                image,

                str(cell["id"]),

                (x + 2, y + 18),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.45,

                (255, 0, 0),

                1,

                cv2.LINE_AA,

            )

        cv2.imwrite(

            str(

                output_directory /

                "extraction_pipeline.png"

            ),

            image,

        )

        logger.info(
            "Extraction visualization saved."
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> dict:
        
        # Return extraction summary.

        if image_data.valid_cells is None:

            return {}

        return {

            "Extracted Cells":
                len(
                    image_data.valid_cells
                ),

            "Rows":
                len({

                    c["row"]

                    for c in image_data.valid_cells

                }),

            "Columns":
                len({

                    c["column"]

                    for c in image_data.valid_cells

                }),

            "Image Size":
                f"{image_data.width} × {image_data.height}",

        }

    @staticmethod
    def print_summary(
        image_data: ImageData,
    ) -> None:
        
        # Print extraction summary.

        summary = ExtractionVisualizer.summary(
            image_data
        )

        print()

        print("=" * 50)

        print("CELL EXTRACTION SUMMARY")

        print("=" * 50)

        for key, value in summary.items():

            print(f"{key:20}: {value}")

        print()

    @staticmethod
    def save_cells(
        image_data: ImageData,
        output_directory: str | Path,
    ) -> None:
        
        # Save every validated cell.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "No extracted cells available."
            )

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

                f"{cell['id']:04d}.png"

            )

            cv2.imwrite(

                str(

                    output_directory /

                    filename

                ),

                cell["image"],

            )

        logger.info(
            "All extracted cells saved."
        )