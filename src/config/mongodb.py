from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

_client: Optional[MongoClient] = None


def _build_mongo_uri() -> str:
    """Build MongoDB URI from environment variables.

    Docker Compose uses MONGO_HOST=mongodb. Local development usually uses
    MONGO_HOST=localhost. MONGO_URI can override all individual fields.
    """
    explicit_uri = os.getenv("MONGO_URI")
    if explicit_uri:
        return explicit_uri

    host = os.getenv("MONGO_HOST", "localhost")
    port = os.getenv("MONGO_PORT", "27017")
    user = os.getenv("MONGO_USER", "")
    password = os.getenv("MONGO_PASSWORD", "")
    auth_source = os.getenv("MONGO_AUTH_SOURCE", "admin")

    if user and password:
        return f"mongodb://{user}:{password}@{host}:{port}/?authSource={auth_source}"
    return f"mongodb://{host}:{port}"


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(
            _build_mongo_uri(),
            serverSelectionTimeoutMS=int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000")),
            connectTimeoutMS=int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", "5000")),
            retryWrites=True,
        )
    return _client


def get_mongo_database(database_name: str | None = None) -> Database:
    db_name = database_name or os.getenv("MONGO_DB", "healthcare_management")
    return get_mongo_client()[db_name]


def ping_mongodb() -> bool:
    try:
        get_mongo_client().admin.command("ping")
        return True
    except Exception:
        return False


def close_mongo_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
