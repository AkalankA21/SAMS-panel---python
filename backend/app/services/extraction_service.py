from __future__ import annotations

from app.extraction.cell_cropper import CellCropper
from app.extraction.cell_exporter import CellExporter
from app.extraction.cell_extractor import CellExtractor
from app.extraction.cell_sorter import CellSorter
from app.extraction.cell_statistics import CellStatistics
from app.extraction.cell_validator import CellValidator
from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class ExtractionService:
    
    # Cell extraction service.

    @staticmethod
    def process(
        image_data: ImageData,
    ) -> list:
        
        # Execute the complete extraction pipeline.

        logger.info(
            "Starting cell extraction pipeline..."
        )

        CellExtractor.extract(
            image_data
        )

        CellCropper.crop(
            image_data
        )

        CellValidator.validate(
            image_data
        )

        CellSorter.sort(
            image_data
        )

        CellStatistics.calculate(
            image_data
        )

        logger.info(
            "Cell extraction pipeline completed."
        )

        return image_data.valid_cells

    @staticmethod
    def extract(
        image_data: ImageData,
    ):
        
        # Extract cells only.

        return CellExtractor.extract(
            image_data
        )

    @staticmethod
    def crop(
        image_data: ImageData,
        padding: int = 3,
    ):
        
        # Crop extracted cells.

        return CellCropper.crop(
            image_data,
            padding,
        )

    @staticmethod
    def validate(
        image_data: ImageData,
    ):
        
        # Validate extracted cells.

        return CellValidator.validate(
            image_data
        )

    @staticmethod
    def sort(
        image_data: ImageData,
    ):
        
        # Sort validated cells.

        return CellSorter.sort(
            image_data
        )

    @staticmethod
    def export(
        image_data: ImageData,
    ):
        
        # Export validated cells.

        return CellExporter.export(
            image_data
        )

    @staticmethod
    def export_images(
        image_data: ImageData,
        output_directory: str,
    ):
        
        # Export cell images.

        return CellExporter.export_images(
            image_data,
            output_directory,
        )

    @staticmethod
    def export_metadata(
        image_data: ImageData,
        output_file: str,
    ):
        
        # Export metadata.

        CellExporter.export_metadata(
            image_data,
            output_file,
        )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return extraction statistics.

        return CellStatistics.calculate(
            image_data
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        return CellStatistics.summary(
            image_data
        )

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Number of valid cells.

        if image_data.valid_cells is None:

            return 0

        return len(
            image_data.valid_cells
        )

    @staticmethod
    def get_cell(
        image_data: ImageData,
        index: int,
    ):
        
        # Return a single validated cell.

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        if (
            index < 0
            or
            index >= len(
                image_data.valid_cells
            )
        ):

            raise IndexError(
                "Cell index out of range."
            )

        return image_data.valid_cells[
            index
        ]

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset Previous methods

        CellExtractor.reset(
            image_data
        )

        CellCropper.reset(
            image_data
        )

        CellValidator.reset(
            image_data
        )

        CellSorter.reset(
            image_data
        )

        CellStatistics.reset(
            image_data
        )

        logger.info(
            "Extraction service reset."
        )

    @staticmethod
    def validate_pipeline(
        image_data: ImageData,
    ) -> bool:
        
        # Verify extraction pipeline output.

        if image_data.valid_cells is None:

            return False

        if len(
            image_data.valid_cells
        ) == 0:

            return False

        return True