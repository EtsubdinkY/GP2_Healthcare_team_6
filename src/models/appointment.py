from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional


@dataclass(slots=True)
class Appointment:
    appt_id: Optional[int]
    patient_id: int
    provider_id: int
    appt_date: date
    appt_time: time
    duration: int
    status: str
    appt_type: str
    reason: str
    notes: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["Appointment"]:
        if row is None:
            return None
        return cls(**row)
