from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.models import Prescription, Patient, Provider, Medication
from src.repositories import (
    PrescriptionRepository,
    PatientRepository,
    ProviderRepository,
    MedicationRepository,
)


@dataclass
class PrescriptionDetail:
    prescription: Prescription
    patient: Optional[Patient]
    provider: Optional[Provider]
    medication: Optional[Medication]


class PrescriptionService:

    def __init__(self):
        self.prescription_repo = PrescriptionRepository()
        self.patient_repo = PatientRepository()
        self.provider_repo = ProviderRepository()
        self.medication_repo = MedicationRepository()

    def get_all_prescriptions(self):
        return self.prescription_repo.find_all()

    def get_prescription_by_id(self, rx_id: int):
        return self.prescription_repo.find_by_id(rx_id)

    def create_prescription(self, prescription: Prescription):
        return self.prescription_repo.create(prescription)

    def update_prescription(self, rx_id: int, prescription: Prescription):
        return self.prescription_repo.update(rx_id, prescription)

    def delete_prescription(self, rx_id: int):
        return self.prescription_repo.delete(rx_id)

    def get_prescription_detail(self, rx_id: int):
        rx = self.prescription_repo.find_by_id(rx_id)
        if rx is None:
            return None

        patient = self.patient_repo.find_by_id(rx.patient_id)
        provider = self.provider_repo.find_by_id(rx.provider_id)
        med = self.medication_repo.find_by_id(rx.med_id)

        return PrescriptionDetail(prescription=rx, patient=patient, provider=provider, medication=med)

    def get_patient_prescriptions(self, patient_id: int):
        all_rxs = self.prescription_repo.find_all()
        patient = self.patient_repo.find_by_id(patient_id)

        result = []
        for rx in all_rxs:
            if rx.patient_id != patient_id:
                continue
            provider = self.provider_repo.find_by_id(rx.provider_id)
            med = self.medication_repo.find_by_id(rx.med_id)
            result.append(PrescriptionDetail(
                prescription=rx,
                patient=patient,
                provider=provider,
                medication=med
            ))

        return result

    def get_active_prescriptions(self):
        all_rxs = self.prescription_repo.find_all()

        result = []
        for rx in all_rxs:
            if rx.status != 'active':
                continue
            patient = self.patient_repo.find_by_id(rx.patient_id)
            provider = self.provider_repo.find_by_id(rx.provider_id)
            med = self.medication_repo.find_by_id(rx.med_id)
            result.append(PrescriptionDetail(
                prescription=rx,
                patient=patient,
                provider=provider,
                medication=med
            ))

        return result

    def get_controlled_substances(self):
        # returns all prescriptions flagged as controlled substances
        all_rxs = self.prescription_repo.find_all()

        result = []
        for rx in all_rxs:
            if not rx.is_controlled:
                continue
            patient = self.patient_repo.find_by_id(rx.patient_id)
            provider = self.provider_repo.find_by_id(rx.provider_id)
            med = self.medication_repo.find_by_id(rx.med_id)
            result.append(PrescriptionDetail(
                prescription=rx,
                patient=patient,
                provider=provider,
                medication=med
            ))

        return result

    def discontinue_prescription(self, rx_id: int):
        rx = self.prescription_repo.find_by_id(rx_id)
        if rx is None:
            return None

        # copy the prescription over but change the status
        updated = Prescription(
            rx_id=rx.rx_id,
            patient_id=rx.patient_id,
            provider_id=rx.provider_id,
            med_id=rx.med_id,
            date_written=rx.date_written,
            dosage=rx.dosage,
            frequency=rx.frequency,
            quantity=rx.quantity,
            refills=rx.refills,
            is_controlled=rx.is_controlled,
            controlled_substance_schedule=rx.controlled_substance_schedule,
            prescriber_dea_number=rx.prescriber_dea_number,
            status='cancelled',
        )
        return self.prescription_repo.update(rx_id, updated)
