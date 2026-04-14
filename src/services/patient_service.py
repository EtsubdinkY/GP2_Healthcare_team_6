from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.models import Patient, PatientInsurance, Prescription, Appointment
from src.repositories import (
    PatientRepository,
    PatientInsuranceRepository,
    PrescriptionRepository,
    AppointmentRepository,
)


@dataclass
class PatientDashboard:
    patient: Patient
    insurance_coverage: list[PatientInsurance]
    active_prescriptions: list[Prescription]
    upcoming_appointments: list[Appointment]


class PatientService:
    def __init__(self) -> None:
        self.patient_repo = PatientRepository()
        self.insurance_repo = PatientInsuranceRepository()
        self.prescription_repo = PrescriptionRepository()
        self.appointment_repo = AppointmentRepository()

    def get_all_patients(self) -> list[Patient]:
        return self.patient_repo.find_all()

    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.patient_repo.find_by_id(patient_id)

    def create_patient(self, patient: Patient) -> Patient:
        return self.patient_repo.create(patient)

    def update_patient(self, patient_id: int, patient: Patient) -> Optional[Patient]:
        return self.patient_repo.update(patient_id, patient)

    def delete_patient(self, patient_id: int) -> bool:
        return self.patient_repo.delete(patient_id)

    def get_patient_dashboard(self, patient_id: int) -> Optional[PatientDashboard]:
        patient = self.patient_repo.find_by_id(patient_id)
        if patient is None:
            return None

        # Get insurance coverage
        insurance_list = self.insurance_repo.find_by_patient_id(patient_id)

        # Filter to active coverage (end_date is null or in the future)
        today = date.today()
        active_insurance = [
            ins for ins in insurance_list
            if ins.end_date is None or ins.end_date >= today
        ]

        # Get all prescriptions and filter to active ones
        all_prescriptions = self.prescription_repo.find_all()
        active_prescriptions = [
            rx for rx in all_prescriptions
            if rx.patient_id == patient_id and rx.status == 'active'
        ]

        # Get all appointments and filter to upcoming ones for this patient
        all_appointments = self.appointment_repo.find_all()
        upcoming_appointments = [
            appt for appt in all_appointments
            if appt.patient_id == patient_id
            and appt.appt_date >= today
            and appt.status == 'scheduled'
        ]

        return PatientDashboard(
            patient=patient,
            insurance_coverage=active_insurance,
            active_prescriptions=active_prescriptions,
            upcoming_appointments=upcoming_appointments,
        )

    def get_polypharmacy_patients(self, threshold: int = 5) -> list[tuple[Patient, int]]:
        all_prescriptions = self.prescription_repo.find_all()
        all_patients = self.patient_repo.find_all()

        # Count active prescriptions per patient
        prescription_counts: dict[int, int] = {}
        for rx in all_prescriptions:
            if rx.status == 'active':
                prescription_counts[rx.patient_id] = prescription_counts.get(rx.patient_id, 0) + 1

        # Filter patients with >= threshold prescriptions
        result = []
        for patient in all_patients:
            count = prescription_counts.get(patient.patient_id, 0)
            if count >= threshold:
                result.append((patient, count))

        # Sort by prescription count descending
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def search_patients_by_name(self, search_term: str) -> list[Patient]:
        all_patients = self.patient_repo.find_all()
        search_lower = search_term.lower()
        return [
            p for p in all_patients
            if search_lower in p.first_name.lower() or search_lower in p.last_name.lower()
        ]
