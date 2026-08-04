import numpy as np

from app.models.image_data import ImageData


def test_image_data_supports_matching_fields() -> None:
    image_data = ImageData(image=np.zeros((2, 2, 3), dtype=np.uint8))

    image_data.matched_students = []
    image_data.unmatched_results = []
    image_data.invalid_matches = []
    image_data.matching_statistics = {}

    assert image_data.matched_students == []
    assert image_data.unmatched_results == []
    assert image_data.invalid_matches == []
    assert image_data.matching_statistics == {}