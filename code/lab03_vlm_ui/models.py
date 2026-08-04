from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class UIAction:
    target_id: str
    label: str
    action: str
    bounds: list[int]
    confidence: float
    reason: str
    requires_confirmation: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
