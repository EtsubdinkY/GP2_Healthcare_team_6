from __future__ import annotations

from typing import Any, Iterable, Optional

from src.config.database import get_connection


class BaseRepository:
    table_name: str = ""
    id_column: str = "id"

    def execute_non_query(self, query: str, params: Optional[Iterable[Any]] = None) -> None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()

    def fetch_one(self, query: str, params: Optional[Iterable[Any]] = None) -> Optional[dict[str, Any]]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchone()

    def fetch_all(self, query: str, params: Optional[Iterable[Any]] = None) -> list[dict[str, Any]]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                rows = cur.fetchall()
                return list(rows)

    def delete_by_id(self, record_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE {self.id_column} = %s"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (record_id,))
                deleted = cur.rowcount > 0
            conn.commit()
        return deleted
