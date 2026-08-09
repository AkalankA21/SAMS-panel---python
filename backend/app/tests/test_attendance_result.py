from app.attendance.attendance_result import AttendanceResult
from app.matching.match_result import MatchResult

def test_attendance_result_dict_interface():
    # Setup mock match and signature dictionary
    match_obj = MatchResult(
        student_id="20210001",
        student_name="Kasun Perera",
        row=3,
        column=2,
        ocr_text="Kasun Perera",
        cleaned_text="Kasun Perera",
        match_type="Name",
        match_score=95.0,
        confidence=0.9,
    )

    signature_dict = {
        "present": True,
        "confidence": 0.98,
        "ink_ratio": 0.15,
        "bbox": (100, 200, 50, 20),
    }

    detection = {
        "match": match_obj,
        "signature": signature_dict,
        "status": "Present",
    }

    # Build AttendanceResult from the detection dictionary
    record = AttendanceResult.from_detection(detection)

    # Assert standard attributes are set
    assert record.student_id == "20210001"
    assert record.student_name == "Kasun Perera"
    assert record.status == "Present"
    assert record.signature_detected is True
    assert record.row == 3
    assert record.column == 2

    # Assert dict-like access via .get() works
    assert record.get("match") is match_obj
    assert record.get("signature") == signature_dict
    assert record.get("status") == "Present"
    assert record.get("student_id") == "20210001"
    assert record.get("nonexistent", "default_val") == "default_val"
