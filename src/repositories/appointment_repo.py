from __future__ import annotations

from typing import Optional

from src.models.appointment import Appointment
from src.repositories.base_repository import BaseRepository


class AppointmentRepository(BaseRepository):
    table_name = "appointment"
    id_column = "appt_id"

    def create(self, appointment: Appointment) -> Appointment:
        query = """
            INSERT INTO appointment (
                patient_id, provider_id, appt_date, appt_time, duration,
                status, appt_type, reason, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        row = self.fetch_one(
            query,
            (
                appointment.patient_id,
                appointment.provider_id,
                appointment.appt_date,
                appointment.appt_time,
                appointment.duration,
                appointment.status,
                appointment.appt_type,
                appointment.reason,
                appointment.notes,
            ),
        )
        return Appointment.from_row(row)

    def find_by_id(self, appt_id: int) -> Optional[Appointment]:
        row = self.fetch_one("SELECT * FROM appointment WHERE appt_id = %s", (appt_id,))
        return Appointment.from_row(row)

    def find_all(self) -> list[Appointment]:
        rows = self.fetch_all("SELECT * FROM appointment ORDER BY appt_date, appt_time, appt_id")
        return [Appointment.from_row(row) for row in rows]

    def update(self, appt_id: int, appointment: Appointment) -> Optional[Appointment]:
        query = """
            UPDATE appointment
            SET patient_id = %s,
                provider_id = %s,
                appt_date = %s,
                appt_time = %s,
                duration = %s,
                status = %s,
                appt_type = %s,
                reason = %s,
                notes = %s
            WHERE appt_id = %s
            RETURNING *
        """
        row = self.fetch_one(
            query,
            (
                appointment.patient_id,
                appointment.provider_id,
                appointment.appt_date,
                appointment.appt_time,
                appointment.duration,
                appointment.status,
                appointment.appt_type,
                appointment.reason,
                appointment.notes,
                appt_id,
            ),
        )
        return Appointment.from_row(row)

    def delete(self, appt_id: int) -> bool:
        return self.delete_by_id(appt_id)
