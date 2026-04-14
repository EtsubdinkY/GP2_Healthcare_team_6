from __future__ import annotations

from typing import Optional

from src.models.provider import Provider
from src.repositories.base_repository import BaseRepository


class ProviderRepository(BaseRepository):
    table_name = "provider"
    id_column = "provider_id"

    def find_by_id(self, provider_id: int) -> Optional[Provider]:
        row = self.fetch_one("SELECT * FROM provider WHERE provider_id = %s", (provider_id,))
        return Provider.from_row(row)

    def find_all(self) -> list[Provider]:
        rows = self.fetch_all("SELECT * FROM provider ORDER BY last_name, first_name, provider_id")
        return [Provider.from_row(row) for row in rows]
