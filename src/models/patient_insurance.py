from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


@dataclass(slots=True)
class PatientInsurance:
    pat_ins_id: Optional[int]
    patient_id: int
    plan_id: int
    policy_number: str
    group_number: Optional[str]
    copay: Decimal
    coverage_type: str
    start_date: date
    end_date: Optional[date]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict | None) -> Optional["PatientInsurance"]:
        if row is None:
            return None
        return cls(**row)
