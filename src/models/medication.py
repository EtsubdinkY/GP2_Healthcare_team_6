from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Medication:
    med_id: Optional[int]
    name: str
    generic_name: str
    drug_class: str
    controlled_substance_schedule: Optional[str]
    form: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["Medication"]:
        if row is None:
            return None
        return cls(**row)
