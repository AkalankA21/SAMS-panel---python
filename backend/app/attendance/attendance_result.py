from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AttendanceResult:
    
    # Represents a student's attendance result.

    student_id: str

    student_name: str

    status: str

    signature_detected: bool

    confidence: float

    ink_ratio: float

    row: int

    column: int

    requires_review: bool = False

    metadata: dict = field(
        default_factory=dict
    )

    match: any = None

    signature: any = None

    def get(self, key: str, default: any = None) -> any:
        if key == "match":
            return self.match
        elif key == "signature":
            return self.signature
        elif key == "status":
            return self.status
        try:
            return getattr(self, key)
        except AttributeError:
            return default


    @property
    def is_present(
        self,
    ) -> bool:
        
        # Check whether the student is present.

        return self.status == "Present"

    @property
    def is_absent(
        self,
    ) -> bool:
        
        # Check whether the student is absent.

        return self.status == "Absent"

    @property
    def is_manual_review(
        self,
    ) -> bool:
        
        # Check whether manual review is required.

        return self.status == "Manual Review"

    def to_dict(
        self,
    ) -> dict:
        
        # Convert object to dictionary.

        return {

            "student_id":
                self.student_id,

            "student_name":
                self.student_name,

            "status":
                self.status,

            "signature_detected":
                self.signature_detected,

            "confidence":
                self.confidence,

            "ink_ratio":
                self.ink_ratio,

            "row":
                self.row,

            "column":
                self.column,

            "requires_review":
                self.requires_review,

            "metadata":
                self.metadata,

        }

    @classmethod
    def from_detection(
        cls,
        attendance: dict,
    ) -> "AttendanceResult":
        
        # Create AttendanceResult from AttendanceDetector output.

        match = attendance.get(
            "match"
        )

        signature = attendance.get(
            "signature",
            {},
        )

        status = attendance.get(
            "status",
            "Manual Review",
        )

        return cls(

            student_id=getattr(
                match,
                "student_id",
                "",
            ),

            student_name=getattr(
                match,
                "student_name",
                "",
            ),

            status=status,

            signature_detected=signature.get(
                "present",
                False,
            ),

            confidence=float(
                signature.get(
                    "confidence",
                    0.0,
                )
            ),

            ink_ratio=float(
                signature.get(
                    "ink_ratio",
                    0.0,
                )
            ),

            row=getattr(
                match,
                "row",
                0,
            ),

            column=getattr(
                match,
                "column",
                0,
            ),

            requires_review=(
                status == "Manual Review"
            ),

            metadata=signature,

            match=match,

            signature=signature,

        )

    def __str__(
        self,
    ) -> str:
        
        # String representation.

        return (

            "AttendanceResult("

            f"id='{self.student_id}', "

            f"name='{self.student_name}', "

            f"status='{self.status}', "

            f"confidence={self.confidence:.2f}, "

            f"review={self.requires_review}"

            ")"

        )

    def __repr__(
        self,
    ) -> str:
        
        # Developer representation.

        return self.__str__()