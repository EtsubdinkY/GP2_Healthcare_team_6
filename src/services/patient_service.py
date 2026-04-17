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

    def __init__(self):
        self.patient_repo = PatientRepository()
        self.insurance_repo = PatientInsuranceRepository()
        self.prescription_repo = PrescriptionRepository()
        self.appointment_repo = AppointmentRepository()

    def get_all_patients(self):
        return self.patient_repo.find_all()

    def get_patient_by_id(self, patient_id: int):
        return self.patient_repo.find_by_id(patient_id)

    def create_patient(self, patient: Patient):
        return self.patient_repo.create(patient)

    def update_patient(self, patient_id: int, patient: Patient):
        return self.patient_repo.update(patient_id, patient)

    def delete_patient(self, patient_id: int):
        return self.patient_repo.delete(patient_id)

    def get_patient_dashboard(self, patient_id: int):
        patient = self.patient_repo.find_by_id(patient_id)
        if not patient:
            return None

        today = date.today()

        # grab insurance records and keep only the active ones
        all_insurance = self.insurance_repo.find_by_patient_id(patient_id)
        active_insurance = []
        for ins in all_insurance:
            if ins.end_date is None or ins.end_date >= today:
                active_insurance.append(ins)

        # pull prescriptions for this patient (status must be active)
        rxs = self.prescription_repo.find_all()
        active_prescriptions = []
        for rx in rxs:
            if rx.patient_id == patient_id and rx.status == 'active':
                active_prescriptions.append(rx)

        # same idea for appointments - only upcoming scheduled ones
        appts = self.appointment_repo.find_all()
        upcoming = []
        for appt in appts:
            if appt.patient_id == patient_id and appt.status == 'scheduled':
                if appt.appt_date >= today:
                    upcoming.append(appt)

        return PatientDashboard(
            patient=patient,
            insurance_coverage=active_insurance,
            active_prescriptions=active_prescriptions,
            upcoming_appointments=upcoming,
        )

    def get_polypharmacy_patients(self, threshold=5):
        # polypharmacy = patient on 5+ active meds at once
        rxs = self.prescription_repo.find_all()
        patients = self.patient_repo.find_all()

        counts = {}
        for rx in rxs:
            if rx.status == 'active':
                if rx.patient_id not in counts:
                    counts[rx.patient_id] = 0
                counts[rx.patient_id] += 1

        flagged = []
        for p in patients:
            n = counts.get(p.patient_id, 0)
            if n >= threshold:
                flagged.append((p, n))

        flagged.sort(key=lambda x: x[1], reverse=True)
        return flagged

    def search_patients_by_name(self, search_term: str):
        patients = self.patient_repo.find_all()
        term = search_term.lower()
        matches = []
        for p in patients:
            if term in p.first_name.lower() or term in p.last_name.lower():
                matches.append(p)
        return matches
