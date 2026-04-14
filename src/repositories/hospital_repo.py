from __future__ import annotations

from typing import Optional

from src.models.hospital import Hospital
from src.repositories.base_repository import BaseRepository


class HospitalRepository(BaseRepository):
    table_name = "hospital"
    id_column = "hospital_id"

    def find_by_id(self, hospital_id: int) -> Optional[Hospital]:
        row = self.fetch_one("SELECT * FROM hospital WHERE hospital_id = %s", (hospital_id,))
        return Hospital.from_row(row)

    def find_all(self) -> list[Hospital]:
        rows = self.fetch_all("SELECT * FROM hospital ORDER BY name, hospital_id")
        return [Hospital.from_row(row) for row in rows]
