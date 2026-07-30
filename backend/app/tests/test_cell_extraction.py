import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.preprocessing.image_loader import ImageLoader
from app.services.perspective_service import PerspectiveService
from app.services.grayscale_service import GrayscaleService
from app.services.enhancement_service import EnhancementService
from app.services.threshold_service import ThresholdService
from app.services.table_service import TableService
from app.services.extraction_service import ExtractionService

from app.visualization.cell_visualizer import CellVisualizer
from app.visualization.extraction_visualizer import (
    ExtractionVisualizer,
)


def main():

    image_path = Path(
        "data/images/2.jpeg"
    )

    image_data = ImageLoader.load(
        image_path
    )

    print("\nLoading Image...")
    print(image_data)

    print("\nPerspective Correction...")
    PerspectiveService.process(
        image_data
    )

    print("\nGrayscale Processing...")
    GrayscaleService.process(
        image_data
    )

    print("\nImage Enhancement...")
    EnhancementService.process(
        image_data
    )

    print("\nThresholding...")
    ThresholdService.process(
        image_data
    )

    print("\nTable Detection...")
    TableService.process(
        image_data
    )

    print("\nCell Extraction...")
    ExtractionService.process(
        image_data
    )

    print(
        "\nExtraction Summary"
    )

    print(
        ExtractionService.summary(
            image_data
        )
    )

    print(
        "\nExtraction Statistics"
    )

    statistics = ExtractionService.statistics(
        image_data
    )

    for key, value in statistics.items():

        print(
            f"{key:20}: {value}"
        )

    print(
        "\nTotal Valid Cells:",
        ExtractionService.count(
            image_data
        ),
    )

    print(
        "\nDisplaying first cell..."
    )

    CellVisualizer.show(
        image_data,
        0,
    )

    print(
        "Displaying cell grid..."
    )

    CellVisualizer.grid(
        image_data
    )

    print(
        "Displaying extraction visualization..."
    )

    ExtractionVisualizer.comparison(
        image_data
    )

    ExtractionVisualizer.numbered_cells(
        image_data
    )

    output_directory = Path(
        "results/cells"
    )

    print(
        "\nSaving extracted cells..."
    )

    ExtractionService.export_images(
        image_data,
        output_directory,
    )

    ExtractionService.export_metadata(
        image_data,
        output_directory /
        "cells.csv",
    )

    ExtractionVisualizer.save_pipeline(
        image_data,
        "results",
    )

    ExtractionVisualizer.save_cells(
        image_data,
        output_directory,
    )

    print(
        "\nPhase 8 completed successfully."
    )


if __name__ == "__main__":

    main()