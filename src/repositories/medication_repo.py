from __future__ import annotations

from typing import Optional

from src.models.medication import Medication
from src.repositories.base_repository import BaseRepository


class MedicationRepository(BaseRepository):
    table_name = "medication"
    id_column = "med_id"

    def find_by_id(self, med_id: int) -> Optional[Medication]:
        row = self.fetch_one("SELECT * FROM medication WHERE med_id = %s", (med_id,))
        return Medication.from_row(row)

    def find_all(self) -> list[Medication]:
        rows = self.fetch_all("SELECT * FROM medication ORDER BY name, med_id")
        return [Medication.from_row(row) for row in rows]
