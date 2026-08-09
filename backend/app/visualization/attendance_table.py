from __future__ import annotations

from app.models.image_data import ImageData
from app.utils.exceptions import (
    ImageProcessingError,
)


class AttendanceTable:
    
    # Display merged attendance records.

    @staticmethod
    def show(
        image_data: ImageData,
    ) -> None:
        
        # Display complete attendance table.

        records = (
            image_data.merged_records
            or []
        )

        if not records:

            raise ImageProcessingError(
                "No merged records available."
            )

        print()

        print("=" * 125)

        print(
            "FINAL ATTENDANCE TABLE"
        )

        print("=" * 125)

        print(

            f"{'Student ID':<15}"

            f"{'Student Name':<30}"

            f"{'Status':<18}"

            f"{'Signature':<12}"

            f"{'Confidence':<12}"

            f"{'Ink Ratio':<12}"

            f"{'Review'}"

        )

        print("=" * 125)

        for record in records:

            print(

                f"{record['student_id']:<15}"

                f"{record['student_name']:<30}"

                f"{record['status']:<18}"

                f"{'Yes' if record['signature_detected'] else 'No':<12}"

                f"{record['confidence']:<12.2f}"

                f"{record['ink_ratio']:<12.4f}"

                f"{'Yes' if record['requires_review'] else 'No'}"

            )

        print("=" * 125)

        print(
            f"Total Students : {len(records)}"
        )

    @staticmethod
    def show_present(
        image_data: ImageData,
    ) -> None:
        
        # Display present students.

        AttendanceTable._show_status(
            image_data,
            "Present",
        )

    @staticmethod
    def show_absent(
        image_data: ImageData,
    ) -> None:
        
        # Display absent students.

        AttendanceTable._show_status(
            image_data,
            "Absent",
        )

    @staticmethod
    def show_review(
        image_data: ImageData,
    ) -> None:
        
        # Display manual review students.

        AttendanceTable._show_status(
            image_data,
            "Manual Review",
        )

    @staticmethod
    def _show_status(
        image_data: ImageData,
        status: str,
    ) -> None:
        
        # Display records filtered by attendance status.

        records = [

            record

            for record in (
                image_data.merged_records
                or []
            )

            if record["status"] == status

        ]

        print()

        print("=" * 80)

        print(status.upper())

        print("=" * 80)

        if not records:

            print(
                "No records found."
            )

            return

        for record in records:

            print(

                f"{record['student_id']:<15}"

                f"{record['student_name']}"

            )

        print()

        print(
            f"Total {status}: {len(records)}"
        )

    @staticmethod
    def show_student(
        image_data: ImageData,
        student_id: str,
    ) -> None:
        
        # Display one student's attendance record.

        records = (
            image_data.merged_records
            or []
        )

        for record in records:

            if (

                record["student_id"]

                ==

                student_id

            ):

                print()

                print("=" * 60)

                print(
                    "STUDENT RECORD"
                )

                print("=" * 60)

                for key, value in record.items():

                    print(

                        f"{key:<22}: {value}"

                    )

                print("=" * 60)

                return

        raise ImageProcessingError(

            f"Student '{student_id}' not found."

        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> None:
        
        # Display attendance summary.

        stats = (
            image_data.xml_statistics
            or {}
        )

        print()

        print("=" * 60)

        print(
            "ATTENDANCE SUMMARY"
        )

        print("=" * 60)

        for key, value in stats.items():

            print(

                f"{key:<25}: {value}"

            )

        print("=" * 60)