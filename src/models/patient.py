from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(slots=True)
class Patient:
    patient_id: Optional[int]
    mrn: str
    ssn: Optional[str]
    first_name: str
    last_name: str
    dob: date
    gender: str
    phone: Optional[str]
    email: Optional[str]
    address: str
    city: str
    state: str
    zip_code: str
    comm_pref: str
    pref_pharmacy: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["Patient"]:
        if row is None:
            return None
        return cls(**row)
