from pathlib import Path

import numpy as np

from app.models.image_data import ImageData
from app.preprocessing.image_loader import ImageLoader
from app.preprocessing.image_resizer import ImageResizer


class ImageService:
    
    # Service class for image operations.

    @staticmethod
    def load_image(image_path: str | Path) -> ImageData:
        
        # Load an image from disk.

        return ImageLoader.load(image_path)

    @staticmethod
    def resize_image(
        image: np.ndarray,
        width: int = None,
        height: int = None
    ) -> np.ndarray:
        
        # Resize image while preserving aspect ratio.

        return ImageResizer.resize(
            image=image,
            width=width,
            height=height
        )

    @staticmethod
    def create_thumbnail(
        image: np.ndarray,
        size=(250, 250)
    ) -> np.ndarray:
        
        # Create thumbnail image.

        return ImageResizer.thumbnail(
            image=image,
            size=size
        )

    @staticmethod
    def resize_for_display(
        image: np.ndarray,
        max_width: int,
        max_height: int
    ) -> np.ndarray:
        
        # Resize image to fit inside GUI.

        return ImageResizer.resize_to_fit(
            image=image,
            max_width=max_width,
            max_height=max_height
        )

    @staticmethod
    def enlarge_image(
        image: np.ndarray,
        factor: float = 2.0
    ) -> np.ndarray:
        """
        Enlarge image.
        """

        return ImageResizer.enlarge(
            image=image,
            factor=factor
        )

    @staticmethod
    def shrink_image(
        image: np.ndarray,
        factor: float = 0.5
    ) -> np.ndarray:
        
        # Shrink image.

        return ImageResizer.shrink(
            image=image,
            factor=factor
        )

    @staticmethod
    def get_image_summary(image_data: ImageData) -> dict:
        
        # Return image information.

        return image_data.summary()