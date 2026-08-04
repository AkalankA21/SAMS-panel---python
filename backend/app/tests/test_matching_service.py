import numpy as np

from app.models.image_data import ImageData
from app.services import matching_service


def test_matching_service_uses_image_data_student_records_when_not_provided(monkeypatch):
    image_data = ImageData(image=np.zeros((10, 10, 3), dtype=np.uint8))
    image_data.student_records = [
        {"student_id": "20210001", "name": "Alice"},
    ]

    captured = {}

    def fake_match(image_data_arg, student_records, fuzzy_threshold):
        captured["records"] = student_records
        return []

    monkeypatch.setattr(matching_service.StudentMatcher, "match", fake_match)
    monkeypatch.setattr(matching_service.MatchValidator, "validate", lambda matches: ([], []))
    monkeypatch.setattr(matching_service.MatchingStatistics, "calculate", lambda image_data_arg: {})

    results = matching_service.MatchingService.process(image_data)

    assert results == []
    assert captured["records"] == image_data.student_records


def test_matching_statistics_calculate():
    from app.matching.matching_statistics import MatchingStatistics
    from app.matching.match_result import MatchResult

    image_data = ImageData(image=np.zeros((10, 10, 3), dtype=np.uint8))
    image_data.ocr_results = [
        {"text": "20210001", "confidence": 0.95},
        {"text": "Fuzzy Name", "confidence": 0.85},
    ]

    # Create one MatchResult object and one dict match for coverage
    res1 = MatchResult(
        student_id="20210001",
        student_name="Alice",
        row=1,
        column=1,
        ocr_text="20210001",
        cleaned_text="20210001",
        match_type="ID",
        match_score=100.0,
        confidence=0.95,
        requires_review=False
    )

    res2 = {
        "match_type": "Fuzzy",
        "match_score": 85.0,
    }

    image_data.matched_students = [res1, res2]
    image_data.unmatched_results = []

    stats = MatchingStatistics.calculate(image_data)

    assert stats["Total OCR Results"] == 2
    assert stats["Matched Students"] == 2
    assert stats["Exact Matches"] == 1
    assert stats["Fuzzy Matches"] == 1
    assert stats["Manual Review"] == 1


def test_results_endpoint_returns_redesigned_json(monkeypatch):
    from app.api.routers import results
    from unittest.mock import MagicMock
    from fastapi import Request

    mock_session = MagicMock()
    mock_session.id = "test-job-id"
    mock_session.status = "success"
    mock_session.attendance_rate = 95.5
    mock_session.present_students = 19
    mock_session.absent_students = 1
    mock_session.manual_review = 0
    mock_session.student_list = '[{"student_id": "20210001", "student_name": "Kasun"}]'
    mock_session.ocr_results = '[{"text": "Kasun", "confidence": 0.98}]'
    mock_session.statistics = MagicMock(
        tables_detected=1,
        cells_detected=20,
        cells_valid=20,
        ocr_texts=20,
        matched_students=19,
        signatures=19
    )

    monkeypatch.setattr(results.SessionRepository, "get_session", lambda db, session_id: mock_session)
    
    mock_request = MagicMock(spec=Request)
    mock_request.base_url = "http://localhost:8000/"

    res = results.get_attendance_results(session_id="test-job-id", request=mock_request, db=MagicMock())
    
    assert res["job_id"] == "test-job-id"
    assert res["status"] == "completed"
    assert res["attendance"]["attendance_rate"] == 95.5
    assert len(res["students"]) == 1
    assert res["students"][0]["student_id"] == "20210001"
    assert len(res["ocr"]) == 1
    assert res["statistics"]["signatures"] == 19

