from __future__ import annotations

from typing import Any

from src.repositories.mongodb.base_mongo_repository import BaseMongoRepository


class ClinicalNotesRepository(BaseMongoRepository):
    """MongoDB repository for clinical note documents."""

    collection_name = "clinical_notes"

    def find_by_patient(self, patient_id: int, limit: int = 10) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"patient_id": int(patient_id)})
            .sort("encounter_date", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def find_by_provider(self, provider_id: int, limit: int = 25) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"provider_id": int(provider_id)})
            .sort("encounter_date", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def find_unsigned_by_provider(self, provider_id: int, limit: int = 25) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"provider_id": int(provider_id), "signed": False})
            .sort("encounter_date", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def find_by_icd10(self, icd10_code: str, limit: int = 25) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"icd10_codes": {"$elemMatch": {"$eq": icd10_code}}})
            .sort("encounter_date", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def search_text(self, search_terms: str, limit: int = 10) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find(
                {"$text": {"$search": search_terms}},
                {"score": {"$meta": "textScore"}, "patient_id": 1, "provider_id": 1,
                 "encounter_date": 1, "note_type": 1, "chief_complaint": 1,
                 "assessment": 1, "plan": 1, "findings": 1, "recommendations": 1}
            )
            .sort([("score", {"$meta": "textScore"}), ("encounter_date", -1)])
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def create_note(self, note: dict[str, Any]) -> str:
        result = self.collection.insert_one(note)
        return str(result.inserted_id)

    def documentation_volume_by_provider(self) -> list[dict[str, Any]]:
        pipeline = [
            {
                "$group": {
                    "_id": {"provider_id": "$provider_id", "note_type": "$note_type"},
                    "note_count": {"$sum": 1},
                    "unsigned_count": {"$sum": {"$cond": [{"$eq": ["$signed", False]}, 1, 0]}},
                    "most_recent_note": {"$max": "$encounter_date"},
                }
            },
            {"$sort": {"_id.provider_id": 1, "_id.note_type": 1}},
            {
                "$project": {
                    "_id": 0,
                    "provider_id": "$_id.provider_id",
                    "note_type": "$_id.note_type",
                    "note_count": 1,
                    "unsigned_count": 1,
                    "most_recent_note": 1,
                }
            },
        ]
        return self.serialize_many(list(self.collection.aggregate(pipeline)))
