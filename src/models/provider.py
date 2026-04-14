from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(slots=True)
class Provider:
    provider_id: Optional[int]
    dept_id: int
    npi: str
    dea_number: Optional[str]
    first_name: str
    last_name: str
    speciality: str
    license_no: str
    licence_exp: date
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["Provider"]:
        if row is None:
            return None
        return cls(**row)
