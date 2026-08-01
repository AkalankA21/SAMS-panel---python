from __future__ import annotations

import matplotlib.pyplot as plt

from app.models.image_data import ImageData


class GrayscaleVisualizer:

    @staticmethod
    def show_original(image_data: ImageData):

        plt.figure(figsize=(7,7))

        plt.imshow(image_data.image[:,:,::-1])

        plt.title("Original")

        plt.axis("off")

        plt.show()

    @staticmethod
    def show_grayscale(image_data: ImageData):

        plt.figure(figsize=(7,7))

        plt.imshow(
            image_data.grayscale_image,
            cmap="gray",
        )

        plt.title("Grayscale")

        plt.axis("off")

        plt.show()

    @staticmethod
    def show_brightness(image_data: ImageData):

        plt.figure(figsize=(7,7))

        plt.imshow(
            image_data.brightness_image,
            cmap="gray",
        )

        plt.title("Brightness")

        plt.axis("off")

        plt.show()

    @staticmethod
    def show_contrast(image_data: ImageData):

        plt.figure(figsize=(7,7))

        plt.imshow(
            image_data.contrast_image,
            cmap="gray",
        )

        plt.title("Contrast")

        plt.axis("off")

        plt.show()

    @staticmethod
    def show_equalized(image_data: ImageData):

        plt.figure(figsize=(7,7))

        plt.imshow(
            image_data.equalized_image,
            cmap="gray",
        )

        plt.title("Histogram Equalization")

        plt.axis("off")

        plt.show()

    @staticmethod
    def show_clahe(image_data: ImageData):

        plt.figure(figsize=(7,7))

        plt.imshow(
            image_data.clahe_image,
            cmap="gray",
        )

        plt.title("CLAHE")

        plt.axis("off")

        plt.show()

    @staticmethod
    def compare(image_data: ImageData):

        fig,axes=plt.subplots(
            2,
            3,
            figsize=(15,10),
        )

        images=[
            ("Original",image_data.image[:,:,::-1],None),
            ("Grayscale",image_data.grayscale_image,"gray"),
            ("Brightness",image_data.brightness_image,"gray"),
            ("Contrast",image_data.contrast_image,"gray"),
            ("Equalized",image_data.equalized_image,"gray"),
            ("CLAHE",image_data.clahe_image,"gray"),
        ]

        for ax,(title,image,cmap) in zip(
            axes.flat,
            images,
        ):

            if image is None:

                ax.set_visible(False)

                continue

            if cmap is None:

                ax.imshow(image)

            else:

                ax.imshow(image,cmap=cmap)

            ax.set_title(title)

            ax.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def processing_summary(image_data: ImageData):

        print("\n========== Image Processing ==========")

        print(f"Filename : {image_data.filename}")

        print(f"Stage : {image_data.processing_stage}")

        print()

        for stage in image_data.processing_history:

            print(f"✓ {stage}")

        print("======================================")