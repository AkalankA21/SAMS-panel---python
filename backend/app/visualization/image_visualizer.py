from __future__ import annotations

from app.models.image_data import ImageData


class ImageVisualizer:
    """Simple image visualization helpers used by the app entry points."""

    @staticmethod
    def summary(image_data: ImageData) -> None:
        print(f"Filename: {image_data.filename}")
        print(f"Resolution: {image_data.resolution}")
        print(f"Channels: {image_data.channels}")
        print(f"Processing stage: {image_data.processing_stage}")

    @staticmethod
    def show(image_data: ImageData) -> None:
        print("Image preview unavailable in headless mode.")
