class ClinicalRecordService:
    """
    Builds a complete patient record using PostgreSQL, MongoDB, and Neo4j.

    PostgreSQL: patient demographics, prescriptions, appointments
    MongoDB: clinical notes, care plans
    Neo4j: medication interaction alerts
    """

    def __init__(self, patient_service=None, prescription_service=None, mongo_notes_repo=None, neo4j_repo=None):
        self.patient_service = patient_service
        self.prescription_service = prescription_service
        self.mongo_notes_repo = mongo_notes_repo
        self.neo4j_repo = neo4j_repo

    def get_complete_record(self, patient_id, user_id=None, user_role=None):
        patient = None
        medications = []
        notes = []
        safety_alerts = []

        if self.patient_service:
            patient = self.patient_service.get_patient_by_id(patient_id)

        if self.prescription_service:
            all_active = self.prescription_service.get_active_prescriptions()
            medications = [
                item for item in all_active
                if getattr(item.prescription, "patient_id", None) == patient_id
            ]

        if self.mongo_notes_repo:
            notes = self.mongo_notes_repo.find_by_patient(patient_id, limit=10)

        if self.neo4j_repo:
            med_names = []
            for item in medications:
                if getattr(item, "medication", None):
                    med_names.append(item.medication.name)

            if med_names:
                safety_alerts = self.neo4j_repo.check_interactions(med_names)

        return {
            "demographics": patient,
            "active_medications": medications,
            "clinical_notes": notes,
            "safety_alerts": safety_alerts,
            "user_id": user_id,
            "user_role": user_role
        }