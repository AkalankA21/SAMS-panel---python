from pathlib import Path

import cv2

from app.models.image_data import ImageData
from app.preprocessing.image_validator import ImageValidator
from app.utils.exceptions import ImageLoadingError
from app.utils.helpers import format_file_size
from app.utils.logger import logger


class ImageLoader:
    """
    Handles loading of attendance sheet images.
    """

    @staticmethod
    def load(image_path: str | Path) -> ImageData:
        
        # Load an image and return an ImageData object.

        try:
            logger.info(f"Validating image: {image_path}")

            ImageValidator.validate(image_path)

            path = Path(image_path)

            logger.info("Loading image using OpenCV...")

            image = cv2.imread(str(path))

            if image is None:
                raise ImageLoadingError(
                    "OpenCV failed to load the image."
                )

            rgb_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            height, width = image.shape[:2]

            channels = 1 if len(image.shape) == 2 else image.shape[2]

            file_size = format_file_size(
                path.stat().st_size
            )

            image_data = ImageData(
                image=image,
                rgb_image=rgb_image,
                path=path,
                filename=path.name,
                extension=path.suffix.lower(),
                width=width,
                height=height,
                channels=channels,
                file_size=file_size,
            )

            logger.info(
                f"Image Loaded Successfully | "
                f"{image_data.filename} | "
                f"{image_data.resolution}"
            )

            return image_data

        except Exception as ex:

            logger.error(
                f"Image loading failed: {ex}"
            )

            raise ImageLoadingError(
                str(ex)
            ) from ex

    @staticmethod
    def load_grayscale(image_path: str | Path):
        
        # Load image directly as grayscale.

        try:

            ImageValidator.validate(image_path)

            logger.info(
                f"Loading grayscale image: {image_path}"
            )

            image = cv2.imread(
                str(image_path),
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                raise ImageLoadingError(
                    "Unable to load grayscale image."
                )

            return image

        except Exception as ex:

            logger.error(ex)

            raise ImageLoadingError(
                str(ex)
            ) from ex

    @staticmethod
    def load_color(image_path: str | Path):
        
        # Load image in BGR format.

        try:

            ImageValidator.validate(image_path)

            logger.info(
                f"Loading color image: {image_path}"
            )

            image = cv2.imread(
                str(image_path),
                cv2.IMREAD_COLOR
            )

            if image is None:
                raise ImageLoadingError(
                    "Unable to load color image."
                )

            return image

        except Exception as ex:

            logger.error(ex)

            raise ImageLoadingError(
                str(ex)
            ) from ex