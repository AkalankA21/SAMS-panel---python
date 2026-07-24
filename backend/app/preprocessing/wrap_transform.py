from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class WarpTransform:
    
    # Performs perspective transformation using four detected document corners.

    @staticmethod
    def order_points(points: np.ndarray) -> np.ndarray:
        
        # Order four points as: Top Left, Top Right, Bottom Right, Bottom Left

        points = points.reshape(4, 2).astype("float32")

        ordered = np.zeros((4, 2), dtype="float32")

        s = points.sum(axis=1)

        ordered[0] = points[np.argmin(s)]     # Top Left
        ordered[2] = points[np.argmax(s)]     # Bottom Right

        diff = np.diff(points, axis=1)

        ordered[1] = points[np.argmin(diff)]  # Top Right
        ordered[3] = points[np.argmax(diff)]  # Bottom Left

        return ordered

    @staticmethod
    def calculate_output_size(
        ordered_points: np.ndarray,
    ) -> tuple[int, int]:
        
        # Calculate output width and height.

        (tl, tr, br, bl) = ordered_points

        width_top = np.linalg.norm(tr - tl)
        width_bottom = np.linalg.norm(br - bl)

        max_width = int(max(width_top, width_bottom))

        height_left = np.linalg.norm(bl - tl)
        height_right = np.linalg.norm(br - tr)

        max_height = int(max(height_left, height_right))

        return max_width, max_height

    @staticmethod
    def get_destination_points(
        width: int,
        height: int,
    ) -> np.ndarray:
        
        # Create destination rectangle.

        return np.array(
            [
                [0, 0],
                [width - 1, 0],
                [width - 1, height - 1],
                [0, height - 1],
            ],
            dtype="float32",
        )

    @staticmethod
    def warp(
        image_data: ImageData,
        contour: np.ndarray,
    ) -> np.ndarray:
        
        # Apply perspective transformation.

        try:

            logger.info(
                "Starting perspective transformation..."
            )

            ordered = WarpTransform.order_points(
                contour
            )

            width, height = (
                WarpTransform.calculate_output_size(
                    ordered
                )
            )

            destination = (
                WarpTransform.get_destination_points(
                    width,
                    height,
                )
            )

            matrix = cv2.getPerspectiveTransform(
                ordered,
                destination,
            )

            warped = cv2.warpPerspective(
                image_data.image,
                matrix,
                (width, height),
                flags=cv2.INTER_LINEAR,
            )

            image_data.perspective_image = warped

            image_data.processing_history[
                "Perspective"
            ] = warped

            image_data.set_stage(
                "Perspective Correction"
            )

            logger.info(
                "Perspective correction completed."
            )

            return warped

        except Exception as ex:

            logger.error(ex)

            raise ImageProcessingError(
                f"Perspective transformation failed: {ex}"
            ) from ex

    @staticmethod
    def draw_corners(
        image: np.ndarray,
        contour: np.ndarray,
    ) -> np.ndarray:
        
        # Draw detected corner points.

        output = image.copy()

        ordered = WarpTransform.order_points(
            contour
        )

        colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
        ]

        for point, color in zip(ordered, colors):

            x = int(point[0])
            y = int(point[1])

            cv2.circle(
                output,
                (x, y),
                8,
                color,
                -1,
            )

        return output

    @staticmethod
    def draw_polygon(
        image: np.ndarray,
        contour: np.ndarray,
    ) -> np.ndarray:
        
        # Draw detected document polygon.

        output = image.copy()

        cv2.polylines(
            output,
            [contour.astype(int)],
            True,
            (0, 255, 0),
            3,
        )

        return output