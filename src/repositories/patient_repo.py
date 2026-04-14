from __future__ import annotations

from typing import Optional

from src.models.patient import Patient
from src.repositories.base_repository import BaseRepository


class PatientRepository(BaseRepository):
    table_name = "patient"
    id_column = "patient_id"

    def create(self, patient: Patient) -> Patient:
        query = """
            INSERT INTO patient (
                mrn, ssn, first_name, last_name, dob, gender, phone, email,
                address, city, state, zip_code, comm_pref, pref_pharmacy
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        row = self.fetch_one(
            query,
            (
                patient.mrn,
                patient.ssn,
                patient.first_name,
                patient.last_name,
                patient.dob,
                patient.gender,
                patient.phone,
                patient.email,
                patient.address,
                patient.city,
                patient.state,
                patient.zip_code,
                patient.comm_pref,
                patient.pref_pharmacy,
            ),
        )
        return Patient.from_row(row)

    def find_by_id(self, patient_id: int) -> Optional[Patient]:
        row = self.fetch_one("SELECT * FROM patient WHERE patient_id = %s", (patient_id,))
        return Patient.from_row(row)

    def find_all(self) -> list[Patient]:
        rows = self.fetch_all("SELECT * FROM patient ORDER BY patient_id")
        return [Patient.from_row(row) for row in rows]

    def update(self, patient_id: int, patient: Patient) -> Optional[Patient]:
        query = """
            UPDATE patient
            SET mrn = %s,
                ssn = %s,
                first_name = %s,
                last_name = %s,
                dob = %s,
                gender = %s,
                phone = %s,
                email = %s,
                address = %s,
                city = %s,
                state = %s,
                zip_code = %s,
                comm_pref = %s,
                pref_pharmacy = %s
            WHERE patient_id = %s
            RETURNING *
        """
        row = self.fetch_one(
            query,
            (
                patient.mrn,
                patient.ssn,
                patient.first_name,
                patient.last_name,
                patient.dob,
                patient.gender,
                patient.phone,
                patient.email,
                patient.address,
                patient.city,
                patient.state,
                patient.zip_code,
                patient.comm_pref,
                patient.pref_pharmacy,
                patient_id,
            ),
        )
        return Patient.from_row(row)

    def delete(self, patient_id: int) -> bool:
        return self.delete_by_id(patient_id)
