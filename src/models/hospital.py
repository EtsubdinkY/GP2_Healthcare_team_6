from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Hospital:
    hospital_id: Optional[int]
    facility_type: str
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    bed_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["Hospital"]:
        if row is None:
            return None
        return cls(**row)
