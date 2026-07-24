from pathlib import Path
import cv2
from app.utils.exceptions import ImageValidationError


class ImageValidator:
    # Validates image files before processing.

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tif",
        ".tiff"
    }

    @staticmethod
    def file_exists(image_path: str | Path) -> bool:
        # Check whether the image file exists.

        return Path(image_path).exists()

    @staticmethod
    def valid_extension(image_path: str | Path) -> bool:
        # Check supported image extensions.

        extension = Path(image_path).suffix.lower()

        return extension in ImageValidator.SUPPORTED_EXTENSIONS

    @staticmethod
    def file_not_empty(image_path: str | Path) -> bool:
        # Ensure file size is greater than zero.

        return Path(image_path).stat().st_size > 0

    @staticmethod
    def readable(image_path: str | Path) -> bool:
        # Check whether OpenCV can read the image.

        image = cv2.imread(str(image_path))

        return image is not None

    @classmethod
    def validate(cls, image_path: str | Path) -> bool:
        # Perform all validation checks.

        path = Path(image_path)

        if not cls.file_exists(path):
            raise ImageValidationError(
                f"Image not found:\n{path}"
            )

        if not cls.valid_extension(path):
            raise ImageValidationError(
                f"Unsupported image format:\n{path.suffix}"
            )

        if not cls.file_not_empty(path):
            raise ImageValidationError(
                "Selected image is empty."
            )

        if not cls.readable(path):
            raise ImageValidationError(
                "OpenCV cannot read this image."
            )

        return True