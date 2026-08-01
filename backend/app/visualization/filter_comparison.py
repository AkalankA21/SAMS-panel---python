from __future__ import annotations

import matplotlib.pyplot as plt

from app.models.image_data import ImageData


class FilterComparison:

    @staticmethod
    def compare(
        image_data: ImageData,
    ):

        images = [

            ("Original",
             image_data.grayscale_image),

            ("Median",
             image_data.median_image),

            ("Gaussian",
             image_data.gaussian_image),

            ("Bilateral",
             image_data.bilateral_image),

            ("Denoised",
             image_data.denoised_image),

            ("Closing",
             image_data.closed_image),
        ]

        fig, axes = plt.subplots(
            2,
            3,
            figsize=(16,10),
        )

        axes = axes.flatten()

        for ax, (title, image) in zip(
            axes,
            images,
        ):

            if image is None:

                ax.axis("off")

                continue

            ax.imshow(
                image,
                cmap="gray",
            )

            ax.set_title(title)

            ax.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def before_after(
        before,
        after,
        before_title="Before",
        after_title="After",
    ):

        fig, axes = plt.subplots(
            1,
            2,
            figsize=(12,6),
        )

        axes[0].imshow(
            before,
            cmap="gray",
        )

        axes[0].set_title(
            before_title,
        )

        axes[0].axis("off")

        axes[1].imshow(
            after,
            cmap="gray",
        )

        axes[1].set_title(
            after_title,
        )

        axes[1].axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def all_filters(
        image_data: ImageData,
    ):

        FilterComparison.compare(
            image_data
        )

    @staticmethod
    def best_result(
        image_data: ImageData,
    ):

        image = image_data.closed_image

        if image is None:

            image = image_data.denoised_image

        if image is None:

            image = image_data.bilateral_image

        if image is None:

            image = image_data.gaussian_image

        if image is None:

            image = image_data.median_image

        if image is None:

            return

        plt.figure(
            figsize=(8,8),
        )

        plt.imshow(
            image,
            cmap="gray",
        )

        plt.title(
            "Final Enhanced Image",
        )

        plt.axis("off")

        plt.tight_layout()

        plt.show()