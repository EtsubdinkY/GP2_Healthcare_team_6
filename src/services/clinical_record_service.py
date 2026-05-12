class ClinicalRecordService:
    """
    Builds a complete patient record using PostgreSQL, MongoDB, and Neo4j.

    PostgreSQL: patient demographics, prescriptions, appointments, labs
    MongoDB: clinical notes, care plans
    Neo4j: medication interaction alerts
    """

    def __init__(
        self,
        patient_service=None,
        prescription_service=None,
        appointment_service=None,
        lab_service=None,
        mongo_notes_repo=None,
        mongo_care_plan_repo=None,
        neo4j_repo=None
    ):
        self.patient_service = patient_service
        self.prescription_service = prescription_service
        self.appointment_service = appointment_service
        self.lab_service = lab_service
        self.mongo_notes_repo = mongo_notes_repo
        self.mongo_care_plan_repo = mongo_care_plan_repo
        self.neo4j_repo = neo4j_repo

    def get_complete_record(self, patient_id, user_id=None, user_role=None):
        patient = None
        medications = []
        appointments = []
        labs = []
        notes = []
        care_plans = []
        safety_alerts = []

        if self.patient_service:
            patient = self.patient_service.get_patient_by_id(patient_id)

        if self.prescription_service:
            all_active = self.prescription_service.get_active_prescriptions()

            filtered = [
                item for item in all_active
                if getattr(item.prescription, "patient_id", None) == patient_id
            ]

            seen = set()

            for item in filtered:
                med_name = item.medication.name if getattr(item, "medication", None) else "Unknown"
                rx = item.prescription

                key = (
                    med_name,
                    rx.dosage,
                    rx.frequency,
                    rx.patient_id
                )

                if key not in seen:
                    seen.add(key)
                    medications.append(item)

        if self.appointment_service:
            all_appointments = self.appointment_service.get_all_appointments()
            appointments = [
                appt for appt in all_appointments
                if getattr(appt, "patient_id", None) == patient_id
            ]

        if self.lab_service:
            labs = self.lab_service.get_labs_by_patient(patient_id)

        if self.mongo_notes_repo:
            notes = self.mongo_notes_repo.find_by_patient(patient_id, limit=10)

        if self.mongo_care_plan_repo:
            care_plans = self.mongo_care_plan_repo.find_active_by_patient(patient_id, limit=5)

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
            "appointments": appointments,
            "labs": labs,
            "clinical_notes": notes,
            "care_plans": care_plans,
            "safety_alerts": safety_alerts,
            "user_id": user_id,
            "user_role": user_role
        }