class PrescriptionSafetyService:
    """
    Checks prescription safety before creating a prescription.

    PostgreSQL:
    - validates patient
    - gets active medications
    - inserts prescription if safe

    Neo4j:
    - checks drug interactions
    """

    def __init__(self, patient_service=None, prescription_service=None, neo4j_repo=None):
        self.patient_service = patient_service
        self.prescription_service = prescription_service
        self.neo4j_repo = neo4j_repo

    def check_prescription_safety(self, patient_id, new_medication_name):
        patient = None
        active_medications = []
        interaction_alerts = []

        if self.patient_service:
            patient = self.patient_service.get_patient_by_id(patient_id)

        if not patient:
            return {
                "safe": False,
                "message": "Patient not found.",
                "interaction_alerts": []
            }

        if self.prescription_service:
            all_active = self.prescription_service.get_active_prescriptions()
            active_medications = [
                item for item in all_active
                if getattr(item.prescription, "patient_id", None) == patient_id
            ]

        med_names = []

        for item in active_medications:
            if getattr(item, "medication", None):
                med_names.append(item.medication.name)

        med_names.append(new_medication_name)

        if self.neo4j_repo:
            interaction_alerts = self.neo4j_repo.check_interactions(med_names)

        if interaction_alerts:
            return {
                "safe": False,
                "message": "Unsafe prescription. Interaction warning found.",
                "interaction_alerts": interaction_alerts
            }

        return {
            "safe": True,
            "message": "No interaction warnings found. Prescription appears safe.",
            "interaction_alerts": []
        }