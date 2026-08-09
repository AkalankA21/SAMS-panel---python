from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from app.models.image_data import ImageData
from app.attendance.attendance_result import (
    AttendanceResult,
)
from app.utils.exceptions import (
    ImageProcessingError,
)


class AttendanceHeatmap:
    
    # Visualize attendance as a heatmap.

    STATUS_VALUES = {

        "Present": 2,

        "Manual Review": 1,

        "Absent": 0,

    }

    STATUS_LABELS = {

        2: "Present",

        1: "Manual Review",

        0: "Absent",

    }

    @staticmethod
    def show(
        image_data: ImageData,
    ) -> None:
        
        # Display attendance heatmap.

        results = (
            image_data.attendance_results
            or []
        )

        if not results:

            print("No attendance results available for heatmap.")
            return

        rows = max(
            result.row
            for result in results
        ) + 1

        cols = max(
            result.column
            for result in results
        ) + 1

        heatmap = np.full(
            (rows, cols),
            np.nan,
        )

        for result in results:

            if not isinstance(
                result,
                AttendanceResult,
            ):
                continue

            heatmap[
                result.row,
                result.column,
            ] = AttendanceHeatmap.STATUS_VALUES[
                result.status
            ]

        plt.figure(
            figsize=(8, 6)
        )

        image = plt.imshow(

            heatmap,

            cmap="RdYlGn",

            interpolation="nearest",

            vmin=0,

            vmax=2,

        )

        plt.title(
            "Attendance Heatmap",
            fontsize=14,
            fontweight="bold",
        )

        plt.xlabel(
            "Column"
        )

        plt.ylabel(
            "Row"
        )

        cbar = plt.colorbar(
            image,
            ticks=[0, 1, 2],
        )

        cbar.ax.set_yticklabels(

            [

                "Absent",

                "Review",

                "Present",

            ]

        )

        plt.grid(
            True,
            color="black",
            linewidth=0.5,
        )

        plt.tight_layout()

        plt.show()

    @staticmethod
    def matrix(
        image_data: ImageData,
    ) -> np.ndarray:
        
        # Return heatmap matrix.

        results = (
            image_data.attendance_results
            or []
        )

        if not results:

            return np.array([])

        rows = max(
            result.row
            for result in results
        ) + 1

        cols = max(
            result.column
            for result in results
        ) + 1

        matrix = np.full(
            (rows, cols),
            np.nan,
        )

        for result in results:

            matrix[
                result.row,
                result.column,
            ] = AttendanceHeatmap.STATUS_VALUES[
                result.status
            ]

        return matrix

    @staticmethod
    def save(
        image_data: ImageData,
        output_file: str,
    ) -> None:
        
        # Save heatmap as an image.

        AttendanceHeatmap.show(
            image_data
        )

        plt.savefig(
            output_file,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()