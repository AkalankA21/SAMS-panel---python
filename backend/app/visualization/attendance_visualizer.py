from __future__ import annotations

from app.models.image_data import ImageData
from app.attendance.attendance_result import (
    AttendanceResult,
)
from app.utils.exceptions import (
    ImageProcessingError,
)


class AttendanceVisualizer:
    
    # Visualize attendance results.

    @staticmethod
    def show_all(
        image_data: ImageData,
    ) -> None:
        
        # Display all attendance records.

        results = image_data.attendance_results or []

        if not results:

            print("No attendance results available.")
            return

        print()

        print("=" * 115)

        print("ATTENDANCE RESULTS")

        print("=" * 115)

        print(

            f"{'ID':<12}"

            f"{'Student Name':<30}"

            f"{'Status':<18}"

            f"{'Confidence':<12}"

            f"{'Ink Ratio':<12}"

            f"{'Review'}"

        )

        print("=" * 115)

        for record in results:

            print(

                f"{record.student_id:<12}"

                f"{record.student_name:<30}"

                f"{record.status:<18}"

                f"{record.confidence:<12.2f}"

                f"{record.ink_ratio:<12.4f}"

                f"{'Yes' if record.requires_review else 'No'}"

            )

        print("=" * 115)

    @staticmethod
    def present_students(
        image_data: ImageData,
    ) -> None:
        
        # Display present students.

        results = [

            r

            for r in (
                image_data.attendance_results
                or []
            )

            if r.is_present

        ]

        print()

        print("=" * 80)

        print("PRESENT STUDENTS")

        print("=" * 80)

        for student in results:

            print(

                f"{student.student_id:<12}"

                f"{student.student_name}"

            )

        print()

        print(

            f"Total Present : {len(results)}"

        )

    @staticmethod
    def absent_students(
        image_data: ImageData,
    ) -> None:
        
        # Display absent students.

        results = [

            r

            for r in (
                image_data.attendance_results
                or []
            )

            if r.is_absent

        ]

        print()

        print("=" * 80)

        print("ABSENT STUDENTS")

        print("=" * 80)

        for student in results:

            print(

                f"{student.student_id:<12}"

                f"{student.student_name}"

            )

        print()

        print(

            f"Total Absent : {len(results)}"

        )

    @staticmethod
    def manual_review(
        image_data: ImageData,
    ) -> None:
        
        # Display manual review records.

        review = [

            r

            for r in (
                image_data.attendance_results
                or []
            )

            if r.is_manual_review

        ]

        print()

        print("=" * 90)

        print("MANUAL REVIEW")

        print("=" * 90)

        if not review:

            print(
                "No manual review required."
            )

            return

        for record in review:

            print(

                f"{record.student_id:<12}"

                f"{record.student_name:<30}"

                f"{record.confidence:6.2f}%"

            )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> None:
        
        # Display attendance statistics.

        stats = (
            image_data.attendance_statistics
            or {}
        )

        print()

        print("=" * 60)

        print("ATTENDANCE STATISTICS")

        print("=" * 60)

        for key, value in stats.items():

            print(

                f"{key:<30}: {value}"

            )

        print("=" * 60)

    @staticmethod
    def show_record(
        image_data: ImageData,
        index: int,
    ) -> None:
        
        # Display one attendance record.

        results = (
            image_data.attendance_results
            or []
        )

        if not results:

            print("No attendance results available.")
            return

        if (

            index < 0

            or

            index >= len(results)

        ):

            raise IndexError(
                "Attendance index out of range."
            )

        record: AttendanceResult = (
            results[index]
        )

        print()

        print("=" * 60)

        print("ATTENDANCE RECORD")

        print("=" * 60)

        print(
            f"Student ID          : {record.student_id}"
        )

        print(
            f"Student Name        : {record.student_name}"
        )

        print(
            f"Status              : {record.status}"
        )

        print(
            f"Signature Detected  : {record.signature_detected}"
        )

        print(
            f"Confidence          : {record.confidence:.2f}%"
        )

        print(
            f"Ink Ratio           : {record.ink_ratio:.4f}"
        )

        print(
            f"Requires Review     : {record.requires_review}"
        )

        print("=" * 60)

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> None:
        
        # Display summary.

        total = len(
            image_data.attendance_results
            or []
        )

        present = len(
            image_data.present_students
            or []
        )

        absent = len(
            image_data.absent_students
            or []
        )

        review = len(

            [

                r

                for r in (

                    image_data.attendance_results
                    or []

                )

                if r.is_manual_review

            ]

        )

        print()

        print("=" * 50)

        print("ATTENDANCE SUMMARY")

        print("=" * 50)

        print(
            f"Total Students : {total}"
        )

        print(
            f"Present        : {present}"
        )

        print(
            f"Absent         : {absent}"
        )

        print(
            f"Manual Review  : {review}"
        )

        print("=" * 50)