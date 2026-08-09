from pathlib import Path

from app.preprocessing.image_loader import ImageLoader

from app.services.perspective_service import PerspectiveService
from app.services.grayscale_service import GrayscaleService
from app.services.enhancement_service import EnhancementService
from app.services.threshold_service import ThresholdService
from app.services.table_service import TableService
from app.services.extraction_service import ExtractionService
from app.services.ocr_service import OCRService
from app.services.matching_service import MatchingService
from app.services.attendance_service import AttendanceService

from app.attendance.attendance_exporter import (
    AttendanceExporter,
)

from app.visualization.attendance_visualizer import (
    AttendanceVisualizer,
)

from app.visualization.attendance_heatmap import (
    AttendanceHeatmap,
)


def load_student_records():
    
    # Sample student records.

    return [

        {

            "student_id": "20210001",

            "name": "John Silva",

        },

        {

            "student_id": "20210002",

            "name": "Kasun Perera",

        },

        {

            "student_id": "20210003",

            "name": "Nimal Fernando",

        },

        {

            "student_id": "20210004",

            "name": "Ashan Peris",

        },

    ]


def main():

    image_path = Path(
        "data/images/1.jpeg"
    )

    print("\nLoading image...")

    image_data = ImageLoader.load(
        image_path
    )

    print("Perspective correction...")
    PerspectiveService.process(
        image_data
    )

    print("Grayscale conversion...")
    GrayscaleService.process(
        image_data
    )

    print("Image enhancement...")
    EnhancementService.process(
        image_data
    )

    print("Thresholding...")
    ThresholdService.process(
        image_data
    )

    print("Table detection...")
    TableService.process(
        image_data
    )

    print("Cell extraction...")
    ExtractionService.process(
        image_data
    )

    print("OCR...")
    OCRService.process(
        image_data
    )

    print("Student matching...")

    MatchingService.process(

        image_data,

        load_student_records(),

    )

    print("Attendance detection...")

    AttendanceService.process(
        image_data
    )

    print()

    AttendanceVisualizer.summary(
        image_data
    )

    AttendanceVisualizer.statistics(
        image_data
    )

    AttendanceVisualizer.show_all(
        image_data
    )

    AttendanceVisualizer.present_students(
        image_data
    )

    AttendanceVisualizer.absent_students(
        image_data
    )

    AttendanceVisualizer.manual_review(
        image_data
    )

    if AttendanceService.has_results(
        image_data
    ):

        AttendanceVisualizer.show_record(

            image_data,

            0,

        )

    print()

    print("Generating attendance heatmap...")

    AttendanceHeatmap.show(
        image_data
    )

    output_directory = Path(
        "results/attendance"
    )

    output_directory.mkdir(

        parents=True,

        exist_ok=True,

    )

    AttendanceExporter.export_csv(

        image_data,

        output_directory
        /
        "attendance_report.csv",

    )

    AttendanceHeatmap.save(

        image_data,

        output_directory
        /
        "attendance_heatmap.png",

    )

    print()

    print(
        "Attendance report exported."
    )

    print(
        "Heatmap exported."
    )

    print()

    print(
        "Phase 11 completed successfully."
    )


if __name__ == "__main__":

    main()