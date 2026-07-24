from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class ContourDetector:
    
    # Detects the attendance sheet contour.

    @staticmethod
    def find_document_contour(
        image_data: ImageData,
        edges: np.ndarray,
    ) -> np.ndarray:
        
        # Detect the largest rectangular contour using robust direct and convex hull approximation.

        try:

            logger.info(
                "Finding document contour..."
            )

            # Dilate edges to close gaps
            kernel = np.ones((5, 5), np.uint8)
            dilated_edges = cv2.dilate(edges, kernel, iterations=1)

            contours, _ = cv2.findContours(
                dilated_edges,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            if not contours:

                raise ImageProcessingError(
                    "No contours detected."
                )

            contours = sorted(
                contours,
                key=cv2.contourArea,
                reverse=True,
            )

            h_img, w_img = image_data.image.shape[:2]
            img_area = h_img * w_img

            # 1. Try finding direct 4-point contour first for large contours
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 0.05 * img_area:
                    continue
                perimeter = cv2.arcLength(contour, True)
                for eps in [0.02, 0.03, 0.04, 0.05, 0.06]:
                    approximation = cv2.approxPolyDP(
                        contour,
                        eps * perimeter,
                        True,
                    )
                    if len(approximation) == 4:
                        image_data.processing_history[
                            "Document Contour"
                        ] = approximation
                        image_data.set_stage(
                            "Contour Detection"
                        )
                        logger.info(
                            "Direct 4-point document contour found."
                        )
                        return approximation

            # 2. Try using convex hull of the largest contour
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 0.05 * img_area:
                    continue
                hull = cv2.convexHull(contour)
                perimeter = cv2.arcLength(hull, True)
                for eps in [0.02, 0.03, 0.04, 0.05, 0.06]:
                    approximation = cv2.approxPolyDP(
                        hull,
                        eps * perimeter,
                        True,
                    )
                    if len(approximation) == 4:
                        image_data.processing_history[
                            "Document Contour"
                        ] = approximation
                        image_data.set_stage(
                            "Contour Detection"
                        )
                        logger.info(
                            "Convex-hull 4-point document contour found."
                        )
                        return approximation

            # 3. Fallback to whole image borders if no large contour matches
            logger.info("No rectangular document found; falling back to whole image borders.")
            fallback = np.array([
                [[0, 0]],
                [[w_img - 1, 0]],
                [[w_img - 1, h_img - 1]],
                [[0, h_img - 1]]
            ], dtype="int32")
            
            image_data.processing_history[
                "Document Contour"
            ] = fallback
            image_data.set_stage(
                "Contour Detection"
            )
            return fallback

        except Exception as ex:

            logger.error(ex)

            raise ImageProcessingError(
                str(ex)
            ) from ex

    @staticmethod
    def draw_contour(
        image: np.ndarray,
        contour: np.ndarray,
        color=(0, 255, 0),
        thickness=3,
    ) -> np.ndarray:
        
        # Draw contour on image.

        output = image.copy()

        cv2.drawContours(
            output,
            [contour],
            -1,
            color,
            thickness,
        )

        return output

    @staticmethod
    def contour_area(
        contour: np.ndarray,
    ) -> float:
    
        # Return contour area.

        return cv2.contourArea(contour)

    @staticmethod
    def contour_perimeter(
        contour: np.ndarray,
    ) -> float:
        
        # Return contour perimeter.

        return cv2.arcLength(
            contour,
            True,
        )