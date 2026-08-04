from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MatchResult:
    
    # Represents a student match.

    student_id: str

    student_name: str

    row: int

    column: int

    ocr_text: str

    cleaned_text: str

    match_type: str

    match_score: float

    confidence: float

    requires_review: bool = False

    metadata: dict = field(
        default_factory=dict
    )

    @property
    def is_exact(self) -> bool:
        
        # Exact ID or Name match.

        return self.match_type in (
            "ID",
            "Name",
        )

    @property
    def is_fuzzy(self) -> bool:
        
        # Fuzzy match.

        return self.match_type == "Fuzzy"

    @property
    def is_partial(self) -> bool:
        
        # Partial ID/Name match.

        return self.match_type in (
            "Partial ID",
            "Partial Name",
        )

    @property
    def accepted(self) -> bool:
        
        # Accepted match.

        return (

            self.match_score >= 80

            and

            not self.requires_review

        )

    def to_dict(self) -> dict:
        
        # Convert object to dictionary.

        return {

            "student_id":
                self.student_id,

            "student_name":
                self.student_name,

            "row":
                self.row,

            "column":
                self.column,

            "ocr_text":
                self.ocr_text,

            "cleaned_text":
                self.cleaned_text,

            "match_type":
                self.match_type,

            "match_score":
                self.match_score,

            "confidence":
                self.confidence,

            "requires_review":
                self.requires_review,

            "metadata":
                self.metadata,

        }

    @classmethod
    def from_match(
        cls,
        match: dict,
    ) -> "MatchResult":
        
        # Create MatchResult from a matcher dictionary.

        student = match.get(
            "student",
            {},
        )

        ocr = match.get(
            "ocr_result",
            {},
        )

        score = float(
            match.get(
                "match_score",
                0.0,
            )
        )

        return cls(

            student_id=student.get(
                "student_id",
                "",
            ),

            student_name=student.get(
                "name",
                "",
            ),

            row=ocr.get(
                "row",
                0,
            ),

            column=ocr.get(
                "column",
                0,
            ),

            ocr_text=ocr.get(
                "text",
                "",
            ),

            cleaned_text=ocr.get(
                "clean_text",
                "",
            ),

            match_type=match.get(
                "match_type",
                "",
            ),

            match_score=score,

            confidence=float(
                ocr.get(
                    "confidence",
                    0.0,
                )
            ),

            requires_review=(

                score < 90

                or

                match.get(
                    "match_type"
                ) == "Fuzzy"

            ),

            metadata=match.get(
                "metadata",
                {},
            ),

        )

    def __str__(
        self,
    ) -> str:
        
        # String representation.

        return (

            "MatchResult("

            f"id='{self.student_id}', "

            f"name='{self.student_name}', "

            f"type='{self.match_type}', "

            f"score={self.match_score:.2f}, "

            f"review={self.requires_review}"

            ")"

        )

    def __repr__(
        self,
    ) -> str:
        
        # Developer representation.

        return self.__str__()