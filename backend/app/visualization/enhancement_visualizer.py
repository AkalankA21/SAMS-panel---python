from __future__ import annotations

import matplotlib.pyplot as plt

from app.models.image_data import ImageData


class EnhancementVisualizer:
    
    # Visualize enhancement pipeline.

    @staticmethod
    def _show(image, title):

        if image is None:
            return

        plt.figure(figsize=(6,6))

        plt.imshow(
            image,
            cmap="gray",
        )

        plt.title(title)

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def median(image_data: ImageData):

        EnhancementVisualizer._show(
            image_data.median_image,
            "Median Filter",
        )

    @staticmethod
    def gaussian(image_data: ImageData):

        EnhancementVisualizer._show(
            image_data.gaussian_image,
            "Gaussian Filter",
        )

    @staticmethod
    def bilateral(image_data: ImageData):

        EnhancementVisualizer._show(
            image_data.bilateral_image,
            "Bilateral Filter",
        )

    @staticmethod
    def denoised(image_data: ImageData):

        EnhancementVisualizer._show(
            image_data.denoised_image,
            "Non Local Means",
        )

    @staticmethod
    def opening(image_data: ImageData):

        EnhancementVisualizer._show(
            image_data.opened_image,
            "Morphological Opening",
        )

    @staticmethod
    def closing(image_data: ImageData):

        EnhancementVisualizer._show(
            image_data.closed_image,
            "Morphological Closing",
        )

    @staticmethod
    def pipeline(image_data: ImageData):

        images = [

            ("Median",
             image_data.median_image),

            ("Gaussian",
             image_data.gaussian_image),

            ("Bilateral",
             image_data.bilateral_image),

            ("Denoised",
             image_data.denoised_image),

            ("Opening",
             image_data.opened_image),

            ("Closing",
             image_data.closed_image),
        ]

        valid = [
            (t, i)
            for t, i in images
            if i is not None
        ]

        if not valid:
            return

        fig, axes = plt.subplots(
            2,
            3,
            figsize=(15,9),
        )

        axes = axes.flatten()

        for ax in axes:
            ax.axis("off")

        for ax, (title, image) in zip(
            axes,
            valid,
        ):

            ax.imshow(
                image,
                cmap="gray",
            )

            ax.set_title(title)

            ax.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def summary(
        image_data: ImageData,
    ):

        print()

        print("=" * 50)

        print("Enhancement Pipeline")

        print("=" * 50)

        for stage in (

            "Median",

            "Gaussian",

            "Bilateral",

            "Denoised",

            "Opening",

            "Closing",
        ):

            if stage in image_data.processing_history:

                print(f"✓ {stage}")

        print("=" * 50)