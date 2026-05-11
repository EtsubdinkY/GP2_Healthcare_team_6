from __future__ import annotations

from typing import Any

from src.repositories.mongodb.base_mongo_repository import BaseMongoRepository


class ImagingRepository(BaseMongoRepository):
    """MongoDB repository for medical imaging metadata."""

    collection_name = "medical_images_metadata"

    def find_by_patient(self, patient_id: int, limit: int = 10) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"patient_id": int(patient_id)})
            .sort("study_date", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def find_critical_findings(self, limit: int = 25) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"radiologist_report.critical_finding": True})
            .sort("study_date", -1)
            .limit(int(limit))
        )
        return self.serialize_many(list(cursor))

    def volume_by_modality(self) -> list[dict[str, Any]]:
        pipeline = [
            {
                "$group": {
                    "_id": "$modality",
                    "study_count": {"$sum": 1},
                    "critical_findings": {
                        "$sum": {"$cond": [{"$eq": ["$radiologist_report.critical_finding", True]}, 1, 0]}
                    },
                    "avg_image_count": {"$avg": "$dicom_metadata.image_count"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "modality": "$_id",
                    "study_count": 1,
                    "critical_findings": 1,
                    "critical_rate": {"$round": [{"$divide": ["$critical_findings", "$study_count"]}, 3]},
                    "avg_image_count": {"$round": ["$avg_image_count", 1]},
                }
            },
            {"$sort": {"critical_rate": -1, "study_count": -1}},
        ]
        return self.serialize_many(list(self.collection.aggregate(pipeline)))
