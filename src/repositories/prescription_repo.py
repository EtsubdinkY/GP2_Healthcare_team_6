from __future__ import annotations

from typing import Optional

from src.models.prescription import Prescription
from src.repositories.base_repository import BaseRepository


class PrescriptionRepository(BaseRepository):
    table_name = "prescription"
    id_column = "rx_id"

    def create(self, prescription: Prescription) -> Prescription:
        query = """
            INSERT INTO prescription (
                patient_id, provider_id, med_id, date_written, dosage,
                frequency, quantity, refills, is_controlled,
                controlled_substance_schedule, prescriber_dea_number, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        row = self.fetch_one(
            query,
            (
                prescription.patient_id,
                prescription.provider_id,
                prescription.med_id,
                prescription.date_written,
                prescription.dosage,
                prescription.frequency,
                prescription.quantity,
                prescription.refills,
                prescription.is_controlled,
                prescription.controlled_substance_schedule,
                prescription.prescriber_dea_number,
                prescription.status,
            ),
        )
        return Prescription.from_row(row)

    def find_by_id(self, rx_id: int) -> Optional[Prescription]:
        row = self.fetch_one("SELECT * FROM prescription WHERE rx_id = %s", (rx_id,))
        return Prescription.from_row(row)

    def find_all(self) -> list[Prescription]:
        rows = self.fetch_all("SELECT * FROM prescription ORDER BY date_written DESC, rx_id")
        return [Prescription.from_row(row) for row in rows]

    def update(self, rx_id: int, prescription: Prescription) -> Optional[Prescription]:
        query = """
            UPDATE prescription
            SET patient_id = %s,
                provider_id = %s,
                med_id = %s,
                date_written = %s,
                dosage = %s,
                frequency = %s,
                quantity = %s,
                refills = %s,
                is_controlled = %s,
                controlled_substance_schedule = %s,
                prescriber_dea_number = %s,
                status = %s
            WHERE rx_id = %s
            RETURNING *
        """
        row = self.fetch_one(
            query,
            (
                prescription.patient_id,
                prescription.provider_id,
                prescription.med_id,
                prescription.date_written,
                prescription.dosage,
                prescription.frequency,
                prescription.quantity,
                prescription.refills,
                prescription.is_controlled,
                prescription.controlled_substance_schedule,
                prescription.prescriber_dea_number,
                prescription.status,
                rx_id,
            ),
        )
        return Prescription.from_row(row)

    def delete(self, rx_id: int) -> bool:
        return self.delete_by_id(rx_id)
