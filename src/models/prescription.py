from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(slots=True)
class Prescription:
    rx_id: Optional[int]
    patient_id: int
    provider_id: int
    med_id: int
    date_written: date
    dosage: str
    frequency: str
    quantity: int
    refills: int
    is_controlled: bool
    controlled_substance_schedule: Optional[str]
    prescriber_dea_number: Optional[str]
    status: str
    start_date: date | None = None
    end_date: date | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["Prescription"]:
        if row is None:
            return None
        return cls(**row)
