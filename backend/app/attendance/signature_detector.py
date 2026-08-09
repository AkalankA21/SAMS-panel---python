from __future__ import annotations

import cv2
import numpy as np

from app.utils.logger import logger


class SignatureDetector:
    
    # Detect signatures using image processing.

    # Percentage of ink pixels required
    # to consider a signature present.
    PRESENT_THRESHOLD = 0.08

    # Percentage below which the cell
    # is considered empty.
    ABSENT_THRESHOLD = 0.02

    @staticmethod
    def detect(
        image_data,
        match,
    ) -> dict:
        
        # Detect whether a signature exists.

        cell = SignatureDetector.get_signature_cell(
            image_data,
            match,
        )

        if cell is None or cell.get("image") is None:

            return {

                "present": False,

                "confidence": 0.0,

                "ink_ratio": 0.0,

                "contour_count": 0,

                "connected_components": 0,

                "review_required": False,

                "bbox": None,

            }

        cell_image = cell["image"]

        binary = SignatureDetector.preprocess(
            cell_image
        )

        cleaned = SignatureDetector.remove_table_lines(
            binary
        )

        # Calculate connected components and filter by area to remove noise
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned)
        MIN_COMPONENT_AREA = 15  # minimum area for a valid stroke component
        filtered_cleaned = np.zeros_like(cleaned)
        connected_components = 0
        largest_area = 0

        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area > largest_area:
                largest_area = area
            if area >= MIN_COMPONENT_AREA:
                connected_components += 1
                filtered_cleaned[labels == i] = 255

        # Calculate contours on the filtered mask
        contours, _ = cv2.findContours(
            filtered_cleaned,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        contour_count = len(contours)

        # Calculate ink ratio on the filtered mask
        ink_ratio = SignatureDetector.calculate_ink_ratio(
            filtered_cleaned
        )

        # Robust mathematical classification boundaries
        if ink_ratio < 0.010 or connected_components <= 2:
            # Clearly Absent
            present = False
            review_required = False
            confidence = (1.0 - (ink_ratio / 0.010)) * 100.0 if ink_ratio < 0.010 else 90.0
        elif ink_ratio >= 0.020 and connected_components >= 5:
            # Clearly Present
            present = True
            review_required = False
            confidence = 80.0 + (ink_ratio * 150.0) + min(connected_components, 10) * 1.0
        else:
            # Genuinely uncertain transition state, requires Manual Review
            present = ink_ratio >= 0.015 or connected_components >= 3
            confidence = 50.0 + (ink_ratio * 300.0)
            review_required = True

        confidence = round(float(np.clip(confidence, 0.0, 100.0)), 2)

        logger.info(
            "Signature detected | "
            "Ink Ratio: %.4f | "
            "Valid Components: %d | "
            "Largest Component Area: %d | "
            "Contour Count: %d | "
            "Confidence: %.2f | "
            "Present: %s | "
            "Review: %s",
            ink_ratio,
            connected_components,
            largest_area,
            contour_count,
            confidence,
            present,
            review_required
        )

        return {

            "present": present,

            "confidence": confidence,

            "ink_ratio": ink_ratio,

            "contour_count": contour_count,

            "connected_components": connected_components,

            "review_required": review_required,

            "image": filtered_cleaned,

            "bbox": cell.get("bbox"),

        }

    @staticmethod
    def get_signature_cell(
        image_data,
        match,
    ):
        
        # Retrieve the signature cell dictionary.

        if hasattr(
            match,
            "metadata",
        ) and match.metadata and "signature_cell" in match.metadata:

            return match.metadata["signature_cell"]

        # Fallback: Find the cell in image_data.cells where row == match.row and column == 5 (or max col)
        row_idx = getattr(match, "row", None)
        if row_idx is not None and hasattr(image_data, "cells") and image_data.cells:
            # Check for column 5 (default signature column)
            for cell in image_data.cells:
                if cell.get("row") == row_idx and cell.get("column") == 5:
                    return cell
            # Check for max column in that row
            row_cells = [c for c in image_data.cells if c.get("row") == row_idx]
            if row_cells:
                return max(row_cells, key=lambda c: c.get("column", 0))

        return None

    @staticmethod
    def preprocess(
        cell,
    ):
        
        # Convert to binary image.

        if len(cell.shape) == 3:

            gray = cv2.cvtColor(

                cell,

                cv2.COLOR_BGR2GRAY,

            )

        else:

            gray = cell.copy()

        binary = cv2.threshold(

            gray,

            0,

            255,

            cv2.THRESH_BINARY_INV
            +
            cv2.THRESH_OTSU,

        )[1]

        return binary

    @staticmethod
    def remove_table_lines(
        binary,
    ):
        
        # Remove horizontal and vertical table borders.

        cleaned = binary.copy()

        horizontal_kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (25, 1),

        )

        horizontal = cv2.morphologyEx(

            cleaned,

            cv2.MORPH_OPEN,

            horizontal_kernel,

        )

        cleaned = cv2.subtract(

            cleaned,

            horizontal,

        )

        vertical_kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (1, 25),

        )

        vertical = cv2.morphologyEx(

            cleaned,

            cv2.MORPH_OPEN,

            vertical_kernel,

        )

        cleaned = cv2.subtract(

            cleaned,

            vertical,

        )

        return cleaned

    @staticmethod
    def calculate_ink_ratio(
        binary,
    ) -> float:
        
        # Calculate percentage of ink pixels.

        foreground = cv2.countNonZero(
            binary
        )

        total = (

            binary.shape[0]

            *

            binary.shape[1]

        )

        if total == 0:

            return 0.0

        return foreground / total

    @staticmethod
    def calculate_confidence(
        ink_ratio,
    ) -> float:
        
        # Estimate confidence.

        if ink_ratio >= SignatureDetector.PRESENT_THRESHOLD:

            confidence = min(

                100.0,

                70 + ink_ratio * 400,

            )

        elif ink_ratio <= SignatureDetector.ABSENT_THRESHOLD:

            confidence = min(

                100.0,

                95 - ink_ratio * 200,

            )

        else:

            confidence = 60.0

        return round(

            confidence,

            2,

        )

    @staticmethod
    def visualize(
        signature,
    ):
        
        # Return processed signature image.

        return signature.get(
            "image"
        )

    @staticmethod
    def is_uncertain(
        signature,
    ) -> bool:
        
        # Determine whether manual review is required.

        return (

            60.0

            <=

            signature["confidence"]

            <

            85.0

        )