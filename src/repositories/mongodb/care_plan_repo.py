from __future__ import annotations

from typing import Any

from src.repositories.mongodb.base_mongo_repository import BaseMongoRepository


class CarePlanRepository(BaseMongoRepository):
    """MongoDB repository for care plan documents."""

    collection_name = "care_plans"

    def find_active_by_patient(self, patient_id: int, limit: int = 10) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"patient_id": int(patient_id), "status": "active"})
            .sort("last_reviewed", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def find_by_icd10(self, icd10_code: str, limit: int = 25) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"primary_diagnosis.icd10": icd10_code})
            .sort("last_reviewed", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def goal_progress_summary(self) -> list[dict[str, Any]]:
        pipeline = [
            {"$match": {"status": "active"}},
            {"$unwind": "$goals"},
            {
                "$group": {
                    "_id": {"goal_status": "$goals.status", "diagnosis": "$primary_diagnosis.name"},
                    "goal_count": {"$sum": 1},
                    "avg_progress_percent": {"$avg": "$goals.progress_percent"},
                    "patients": {"$addToSet": "$patient_id"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "diagnosis": "$_id.diagnosis",
                    "goal_status": "$_id.goal_status",
                    "goal_count": 1,
                    "avg_progress_percent": {"$round": ["$avg_progress_percent", 1]},
                    "patient_count": {"$size": "$patients"},
                }
            },
            {"$sort": {"goal_status": 1, "diagnosis": 1}},
        ]
        return self.serialize_many(list(self.collection.aggregate(pipeline)))
