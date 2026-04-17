from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.models import Appointment, Patient, Provider
from src.repositories import (
    AppointmentRepository,
    PatientRepository,
    ProviderRepository,
)


@dataclass
class AppointmentDetail:
    appointment: Appointment
    patient: Optional[Patient]
    provider: Optional[Provider]


class AppointmentService:

    def __init__(self):
        self.appointment_repo = AppointmentRepository()
        self.patient_repo = PatientRepository()
        self.provider_repo = ProviderRepository()

    def get_all_appointments(self):
        return self.appointment_repo.find_all()

    def get_appointment_by_id(self, appt_id: int):
        return self.appointment_repo.find_by_id(appt_id)

    def create_appointment(self, appointment: Appointment):
        return self.appointment_repo.create(appointment)

    def update_appointment(self, appt_id: int, appointment: Appointment):
        return self.appointment_repo.update(appt_id, appointment)

    def delete_appointment(self, appt_id: int):
        return self.appointment_repo.delete(appt_id)

    def get_appointment_detail(self, appt_id: int):
        appt = self.appointment_repo.find_by_id(appt_id)
        if appt is None:
            return None

        patient = self.patient_repo.find_by_id(appt.patient_id)
        provider = self.provider_repo.find_by_id(appt.provider_id)

        return AppointmentDetail(appointment=appt, patient=patient, provider=provider)

    def get_upcoming_appointments(self):
        today = date.today()
        all_appts = self.appointment_repo.find_all()

        result = []
        for appt in all_appts:
            if appt.appt_date >= today and appt.status == 'scheduled':
                patient = self.patient_repo.find_by_id(appt.patient_id)
                provider = self.provider_repo.find_by_id(appt.provider_id)
                result.append(AppointmentDetail(
                    appointment=appt,
                    patient=patient,
                    provider=provider
                ))

        return result

    def get_provider_schedule(self, provider_id: int):
        today = date.today()
        all_appts = self.appointment_repo.find_all()
        provider = self.provider_repo.find_by_id(provider_id)

        result = []
        for appt in all_appts:
            if (appt.provider_id == provider_id
                    and appt.status == 'scheduled'
                    and appt.appt_date >= today):
                patient = self.patient_repo.find_by_id(appt.patient_id)
                result.append(AppointmentDetail(
                    appointment=appt,
                    patient=patient,
                    provider=provider
                ))

        return result

    def get_appointments_by_date(self, target_date: date):
        all_appts = self.appointment_repo.find_all()

        result = []
        for appt in all_appts:
            if appt.appt_date == target_date:
                patient = self.patient_repo.find_by_id(appt.patient_id)
                provider = self.provider_repo.find_by_id(appt.provider_id)
                result.append(AppointmentDetail(
                    appointment=appt,
                    patient=patient,
                    provider=provider
                ))

        return result

    def cancel_appointment(self, appt_id: int):
        appt = self.appointment_repo.find_by_id(appt_id)
        if appt is None:
            return None

        # build a new Appointment object with status flipped to cancelled
        updated = Appointment(
            appt_id=appt.appt_id,
            patient_id=appt.patient_id,
            provider_id=appt.provider_id,
            appt_date=appt.appt_date,
            appt_time=appt.appt_time,
            duration=appt.duration,
            status='cancelled',
            appt_type=appt.appt_type,
            reason=appt.reason,
            notes=appt.notes,
        )
        return self.appointment_repo.update(appt_id, updated)
