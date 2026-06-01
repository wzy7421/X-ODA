from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Any


IDENTIFIER_PATTERNS = [
    re.compile(r"\b\d{15,18}\b"),
    re.compile(r"\b\d{3}[- ]?\d{3,4}[- ]?\d{4}\b"),
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
]


@dataclass(frozen=True)
class VisualEvidence:
    anatomical_zone: str
    lesion_area_ratio: float
    activation_intensity: str
    heatmap_focus: str


@dataclass(frozen=True)
class LLMPayload:
    case_id: str
    cnn_prediction: str
    prediction_confidence: float
    cam_visual_evidence: VisualEvidence
    non_identifying_note: str = ""


def contains_identifier(text: str) -> bool:
    return any(pattern.search(text) for pattern in IDENTIFIER_PATTERNS)


def build_llm_payload(
    *,
    case_id: str,
    cnn_prediction: str,
    prediction_confidence: float,
    cam_visual_evidence: dict[str, Any],
    non_identifying_note: str = "",
) -> dict[str, Any]:
    """Build the minimal de-identified payload allowed for external LLM calls."""
    joined = " ".join([case_id, cnn_prediction, non_identifying_note, str(cam_visual_evidence)])
    if contains_identifier(joined):
        raise ValueError("Potential patient identifier detected; external payload rejected.")
    if not 0.0 <= prediction_confidence <= 1.0:
        raise ValueError("prediction_confidence must be in [0, 1].")
    evidence = VisualEvidence(**cam_visual_evidence)
    payload = LLMPayload(
        case_id=case_id,
        cnn_prediction=cnn_prediction,
        prediction_confidence=prediction_confidence,
        cam_visual_evidence=evidence,
        non_identifying_note=non_identifying_note,
    )
    return asdict(payload)

