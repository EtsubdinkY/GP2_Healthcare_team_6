from __future__ import annotations

from datetime import date, datetime
from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

from src.config.mongodb import get_mongo_database


class BaseMongoRepository:
    """Small helper base class for MongoDB repositories."""

    collection_name: str = ""

    def __init__(self, database=None):
        self.db = database or get_mongo_database()
        self.collection: Collection = self.db[self.collection_name]

    @classmethod
    def _clean_value(cls, value: Any) -> Any:
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, list):
            return [cls._clean_value(item) for item in value]
        if isinstance(value, dict):
            return {key: cls._clean_value(item) for key, item in value.items()}
        return value

    @classmethod
    def serialize(cls, document: dict[str, Any] | None) -> dict[str, Any] | None:
        if document is None:
            return None
        return cls._clean_value(document)

    @classmethod
    def serialize_many(cls, documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [cls.serialize(document) for document in documents]
