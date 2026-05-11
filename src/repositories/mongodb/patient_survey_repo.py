from __future__ import annotations

from typing import Any

from src.repositories.mongodb.base_mongo_repository import BaseMongoRepository


class PatientSurveyRepository(BaseMongoRepository):
    """MongoDB repository for patient-reported outcome surveys."""

    collection_name = "patient_surveys"

    def find_by_patient(self, patient_id: int, survey_type: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        query: dict[str, Any] = {"patient_id": int(patient_id)}
        if survey_type:
            query["survey_type"] = survey_type
        cursor = self.collection.find(query).sort("completed_at", -1).limit(int(limit))
        return self.serialize_many(list(cursor))

    def find_elevated_responses(self, question_code: str, minimum_score: int = 1, limit: int = 25) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find(
                {"responses": {"$elemMatch": {"question_code": question_code, "score": {"$gte": int(minimum_score)}}}}
            )
            .sort("completed_at", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def monthly_score_trends(self, limit: int = 50) -> list[dict[str, Any]]:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "patient_id": "$patient_id",
                        "survey_type": "$survey_type",
                        "month": {"$dateToString": {"format": "%Y-%m", "date": "$completed_at"}},
                    },
                    "avg_score": {"$avg": "$score.total"},
                    "latest_completed_at": {"$max": "$completed_at"},
                    "surveys_completed": {"$sum": 1},
                    "latest_severity": {"$last": "$score.severity"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "patient_id": "$_id.patient_id",
                    "survey_type": "$_id.survey_type",
                    "month": "$_id.month",
                    "avg_score": {"$round": ["$avg_score", 1]},
                    "surveys_completed": 1,
                    "latest_severity": 1,
                    "latest_completed_at": 1,
                }
            },
            {"$sort": {"patient_id": 1, "survey_type": 1, "month": 1}},
            {"$limit": int(limit)},
        ]
        return self.serialize_many(list(self.collection.aggregate(pipeline)))
