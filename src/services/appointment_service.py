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
    """Appointment with related patient and provider information."""
    appointment: Appointment
    patient: Optional[Patient]
    provider: Optional[Provider]


class AppointmentService:
    """Business logic for appointment operations."""

    def __init__(self) -> None:
        self.appointment_repo = AppointmentRepository()
        self.patient_repo = PatientRepository()
        self.provider_repo = ProviderRepository()

    def get_all_appointments(self) -> list[Appointment]:
        """Retrieve all appointments."""
        return self.appointment_repo.find_all()

    def get_appointment_by_id(self, appt_id: int) -> Optional[Appointment]:
        """Retrieve an appointment by ID."""
        return self.appointment_repo.find_by_id(appt_id)

    def create_appointment(self, appointment: Appointment) -> Appointment:
        """Create a new appointment."""
        return self.appointment_repo.create(appointment)

    def update_appointment(self, appt_id: int, appointment: Appointment) -> Optional[Appointment]:
        """Update an existing appointment."""
        return self.appointment_repo.update(appt_id, appointment)

    def delete_appointment(self, appt_id: int) -> bool:
        """Delete an appointment."""
        return self.appointment_repo.delete(appt_id)

    def get_appointment_detail(self, appt_id: int) -> Optional[AppointmentDetail]:
        """Get appointment with patient and provider details."""
        appointment = self.appointment_repo.find_by_id(appt_id)
        if appointment is None:
            return None

        patient = self.patient_repo.find_by_id(appointment.patient_id)
        provider = self.provider_repo.find_by_id(appointment.provider_id)

        return AppointmentDetail(
            appointment=appointment,
            patient=patient,
            provider=provider,
        )

    def get_upcoming_appointments(self) -> list[AppointmentDetail]:
        """Get all upcoming scheduled appointments with details."""
        today = date.today()
        all_appointments = self.appointment_repo.find_all()

        upcoming = [
            appt for appt in all_appointments
            if appt.appt_date >= today and appt.status == 'scheduled'
        ]

        result = []
        for appt in upcoming:
            patient = self.patient_repo.find_by_id(appt.patient_id)
            provider = self.provider_repo.find_by_id(appt.provider_id)
            result.append(AppointmentDetail(
                appointment=appt,
                patient=patient,
                provider=provider,
            ))

        return result

    def get_provider_schedule(self, provider_id: int) -> list[AppointmentDetail]:
        """Get upcoming appointments for a specific provider."""
        today = date.today()
        all_appointments = self.appointment_repo.find_all()

        provider = self.provider_repo.find_by_id(provider_id)
        provider_appointments = [
            appt for appt in all_appointments
            if appt.provider_id == provider_id
            and appt.appt_date >= today
            and appt.status == 'scheduled'
        ]

        result = []
        for appt in provider_appointments:
            patient = self.patient_repo.find_by_id(appt.patient_id)
            result.append(AppointmentDetail(
                appointment=appt,
                patient=patient,
                provider=provider,
            ))

        return result

    def get_appointments_by_date(self, target_date: date) -> list[AppointmentDetail]:
        """Get all appointments for a specific date."""
        all_appointments = self.appointment_repo.find_all()

        date_appointments = [
            appt for appt in all_appointments
            if appt.appt_date == target_date
        ]

        result = []
        for appt in date_appointments:
            patient = self.patient_repo.find_by_id(appt.patient_id)
            provider = self.provider_repo.find_by_id(appt.provider_id)
            result.append(AppointmentDetail(
                appointment=appt,
                patient=patient,
                provider=provider,
            ))

        return result

    def cancel_appointment(self, appt_id: int) -> Optional[Appointment]:
        """Cancel an appointment by updating its status."""
        appointment = self.appointment_repo.find_by_id(appt_id)
        if appointment is None:
            return None

        # Create updated appointment with cancelled status
        cancelled = Appointment(
            appt_id=appointment.appt_id,
            patient_id=appointment.patient_id,
            provider_id=appointment.provider_id,
            appt_date=appointment.appt_date,
            appt_time=appointment.appt_time,
            duration=appointment.duration,
            status='cancelled',
            appt_type=appointment.appt_type,
            reason=appointment.reason,
            notes=appointment.notes,
        )
        return self.appointment_repo.update(appt_id, cancelled)
