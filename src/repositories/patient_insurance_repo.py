from __future__ import annotations

from typing import Optional

from src.models.patient_insurance import PatientInsurance
from src.repositories.base_repository import BaseRepository


class PatientInsuranceRepository(BaseRepository):
    table_name = "patient_insurance"
    id_column = "pat_ins_id"

    def find_by_id(self, pat_ins_id: int) -> Optional[PatientInsurance]:
        row = self.fetch_one("SELECT * FROM patient_insurance WHERE pat_ins_id = %s", (pat_ins_id,))
        return PatientInsurance.from_row(row)

    def find_all(self) -> list[PatientInsurance]:
        rows = self.fetch_all("SELECT * FROM patient_insurance ORDER BY patient_id, pat_ins_id")
        return [PatientInsurance.from_row(row) for row in rows]

    def find_by_patient_id(self, patient_id: int) -> list[PatientInsurance]:
        rows = self.fetch_all(
            "SELECT * FROM patient_insurance WHERE patient_id = %s ORDER BY coverage_type, pat_ins_id",
            (patient_id,),
        )
        return [PatientInsurance.from_row(row) for row in rows]
