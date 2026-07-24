import cv2
import numpy as np


class ImageResizer:
    # Utility class for resizing images.

    @staticmethod
    def resize(image: np.ndarray,
               width: int = None,
               height: int = None,
               interpolation=cv2.INTER_AREA) -> np.ndarray:
        
        # Resize image while maintaining aspect ratio.

        if width is None and height is None:
            return image.copy()

        h, w = image.shape[:2]

        if width is None:
            ratio = height / h
            width = int(w * ratio)

        elif height is None:
            ratio = width / w
            height = int(h * ratio)

        resized = cv2.resize(
            image,
            (width, height),
            interpolation=interpolation
        )

        return resized

    @staticmethod
    def resize_to_fit(image: np.ndarray,
                      max_width: int,
                      max_height: int) -> np.ndarray:

        # Resize image to fit inside a window while maintaining aspect ratio.

        h, w = image.shape[:2]

        scale = min(max_width / w, max_height / h)

        if scale >= 1:
            return image.copy()

        new_width = int(w * scale)
        new_height = int(h * scale)

        return cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    @staticmethod
    def scale(image: np.ndarray,
              scale_percent: float) -> np.ndarray:
        
        # Resize image by percentage.

        width = int(image.shape[1] * scale_percent / 100)

        height = int(image.shape[0] * scale_percent / 100)

        return cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_LINEAR
        )

    @staticmethod
    def thumbnail(image: np.ndarray,
                  size=(250, 250)) -> np.ndarray:
        
        # Create thumbnail image.

        h, w = image.shape[:2]

        scale = min(size[0] / w, size[1] / h)

        width = int(w * scale)

        height = int(h * scale)

        return cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA
        )

    @staticmethod
    def enlarge(image: np.ndarray,
                factor: float = 2.0) -> np.ndarray:
        
        # Enlarge image.

        h, w = image.shape[:2]

        return cv2.resize(
            image,
            (int(w * factor), int(h * factor)),
            interpolation=cv2.INTER_CUBIC
        )

    @staticmethod
    def shrink(image: np.ndarray,
               factor: float = 0.5) -> np.ndarray:
        
        # Shrink image.

        h, w = image.shape[:2]

        return cv2.resize(
            image,
            (int(w * factor), int(h * factor)),
            interpolation=cv2.INTER_AREA
        )