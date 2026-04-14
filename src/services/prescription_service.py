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
    def __init__(self) -> None:
        self.prescription_repo = PrescriptionRepository()
        self.patient_repo = PatientRepository()
        self.provider_repo = ProviderRepository()
        self.medication_repo = MedicationRepository()

    def get_all_prescriptions(self) -> list[Prescription]:
        return self.prescription_repo.find_all()

    def get_prescription_by_id(self, rx_id: int) -> Optional[Prescription]:
        return self.prescription_repo.find_by_id(rx_id)

    def create_prescription(self, prescription: Prescription) -> Prescription:
        return self.prescription_repo.create(prescription)

    def update_prescription(self, rx_id: int, prescription: Prescription) -> Optional[Prescription]:
        return self.prescription_repo.update(rx_id, prescription)

    def delete_prescription(self, rx_id: int) -> bool:
        return self.prescription_repo.delete(rx_id)

    def get_prescription_detail(self, rx_id: int) -> Optional[PrescriptionDetail]:
        prescription = self.prescription_repo.find_by_id(rx_id)
        if prescription is None:
            return None

        patient = self.patient_repo.find_by_id(prescription.patient_id)
        provider = self.provider_repo.find_by_id(prescription.provider_id)
        medication = self.medication_repo.find_by_id(prescription.med_id)

        return PrescriptionDetail(
            prescription=prescription,
            patient=patient,
            provider=provider,
            medication=medication,
        )

    def get_patient_prescriptions(self, patient_id: int) -> list[PrescriptionDetail]:
        all_prescriptions = self.prescription_repo.find_all()

        patient = self.patient_repo.find_by_id(patient_id)
        patient_rxs = [
            rx for rx in all_prescriptions
            if rx.patient_id == patient_id
        ]

        result = []
        for rx in patient_rxs:
            provider = self.provider_repo.find_by_id(rx.provider_id)
            medication = self.medication_repo.find_by_id(rx.med_id)
            result.append(PrescriptionDetail(
                prescription=rx,
                patient=patient,
                provider=provider,
                medication=medication,
            ))

        return result

    def get_active_prescriptions(self) -> list[PrescriptionDetail]:
        all_prescriptions = self.prescription_repo.find_all()

        active = [rx for rx in all_prescriptions if rx.status == 'active']

        result = []
        for rx in active:
            patient = self.patient_repo.find_by_id(rx.patient_id)
            provider = self.provider_repo.find_by_id(rx.provider_id)
            medication = self.medication_repo.find_by_id(rx.med_id)
            result.append(PrescriptionDetail(
                prescription=rx,
                patient=patient,
                provider=provider,
                medication=medication,
            ))

        return result

    def get_controlled_substances(self) -> list[PrescriptionDetail]:
        all_prescriptions = self.prescription_repo.find_all()

        controlled = [rx for rx in all_prescriptions if rx.is_controlled]

        result = []
        for rx in controlled:
            patient = self.patient_repo.find_by_id(rx.patient_id)
            provider = self.provider_repo.find_by_id(rx.provider_id)
            medication = self.medication_repo.find_by_id(rx.med_id)
            result.append(PrescriptionDetail(
                prescription=rx,
                patient=patient,
                provider=provider,
                medication=medication,
            ))

        return result

    def discontinue_prescription(self, rx_id: int) -> Optional[Prescription]:
        prescription = self.prescription_repo.find_by_id(rx_id)
        if prescription is None:
            return None

        discontinued = Prescription(
            rx_id=prescription.rx_id,
            patient_id=prescription.patient_id,
            provider_id=prescription.provider_id,
            med_id=prescription.med_id,
            date_written=prescription.date_written,
            dosage=prescription.dosage,
            frequency=prescription.frequency,
            quantity=prescription.quantity,
            refills=prescription.refills,
            is_controlled=prescription.is_controlled,
            controlled_substance_schedule=prescription.controlled_substance_schedule,
            prescriber_dea_number=prescription.prescriber_dea_number,
            status='discontinued',
        )
        return self.prescription_repo.update(rx_id, discontinued)
