"""
Test suite for service classes.

Services contain business logic that combines multiple repositories.
These tests verify that your services return correct, well-structured
results for the operations exposed through your CLI.

SETUP:
    Same as test_repositories.py -- make sure your test database
    has schema and data loaded before running.

    Run from project root:
        PYTHONPATH=. pytest tests/test_services.py -v

NOTE: These are starter-style tests adapted to match the actual
      methods implemented in PatientService.
"""

from datetime import date
import pytest

from src.config.database import get_pool, close_pool
from src.models.patient import Patient
from src.services.patient_service import PatientService, PatientDashboard


# ----------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    """Initialize the connection pool once for the entire test session."""
    get_pool()
    yield
    close_pool()


@pytest.fixture
def patient_service():
    """Provide a fresh PatientService instance for each test."""
    return PatientService()


# ----------------------------------------------------------------
# Basic Patient Service Operations
# ----------------------------------------------------------------

class TestPatientServiceBasicOperations:
    """Tests for basic patient service methods."""

    def test_get_all_patients_returns_list(self, patient_service):
        """Should return a list of patients."""
        results = patient_service.get_all_patients()

        assert isinstance(results, list)
        assert len(results) > 0
        assert isinstance(results[0], Patient)

    def test_get_patient_by_id_returns_patient(self, patient_service):
        """Should return a patient for a known ID."""
        result = patient_service.get_patient_by_id(1)

        assert result is not None
        assert isinstance(result, Patient)
        assert result.patient_id == 1

    def test_get_patient_by_id_returns_none_for_missing(self, patient_service):
        """Should return None for a non-existent patient ID."""
        result = patient_service.get_patient_by_id(99999)
        assert result is None


# ----------------------------------------------------------------
# Patient CRUD Through Service Layer
# ----------------------------------------------------------------

class TestPatientServiceCRUD:
    """Tests for create, update, and delete through the service layer."""

    def test_create_patient_and_retrieve(self, patient_service):
        """Service should create a patient and allow retrieval."""
        new_patient = Patient(
            patient_id=None,
            mrn="5555555555",
            ssn=None,
            first_name="Service",
            last_name="Create",
            dob=date(1990, 1, 1),
            gender="Female",
            phone="555-111-9999",
            email="service.create@example.com",
            address="100 Service St",
            city="Ottawa",
            state="ON",
            zip_code="12345",
            comm_pref="Email",
            pref_pharmacy="Service Pharmacy",
        )

        created = patient_service.create_patient(new_patient)

        assert created is not None
        assert created.patient_id is not None
        assert created.mrn == "5555555555"

        retrieved = patient_service.get_patient_by_id(created.patient_id)
        assert retrieved is not None
        assert retrieved.first_name == "Service"
        assert retrieved.last_name == "Create"

        assert patient_service.delete_patient(created.patient_id) is True

    def test_update_patient_persists_changes(self, patient_service):
        """Service should update a patient and persist the changes."""
        temp_patient = Patient(
            patient_id=None,
            mrn="4444444444",
            ssn=None,
            first_name="Before",
            last_name="Update",
            dob=date(1991, 2, 2),
            gender="Male",
            phone="555-222-9999",
            email="before.update@example.com",
            address="200 Update Ave",
            city="Toronto",
            state="ON",
            zip_code="23456",
            comm_pref="Phone",
            pref_pharmacy="Original Pharmacy",
        )

        created = patient_service.create_patient(temp_patient)
        assert created is not None
        assert created.patient_id is not None

        updated_patient = Patient(
            patient_id=created.patient_id,
            mrn=created.mrn,
            ssn=created.ssn,
            first_name="After",
            last_name="Update",
            dob=created.dob,
            gender=created.gender,
            phone="555-000-1234",
            email="after.update@example.com",
            address=created.address,
            city=created.city,
            state=created.state,
            zip_code=created.zip_code,
            comm_pref="Email",
            pref_pharmacy="Updated Pharmacy",
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

        result = patient_service.update_patient(created.patient_id, updated_patient)

        assert result is not None
        assert result.first_name == "After"
        assert result.phone == "555-000-1234"
        assert result.email == "after.update@example.com"
        assert result.pref_pharmacy == "Updated Pharmacy"

        retrieved = patient_service.get_patient_by_id(created.patient_id)
        assert retrieved is not None
        assert retrieved.first_name == "After"

        assert patient_service.delete_patient(created.patient_id) is True

    def test_delete_patient_removes_record(self, patient_service):
        """Service should delete a patient so it can no longer be found."""
        temp_patient = Patient(
            patient_id=None,
            mrn="3333333333",
            ssn=None,
            first_name="Delete",
            last_name="Service",
            dob=date(1992, 3, 3),
            gender="Female",
            phone="555-333-9999",
            email="delete.service@example.com",
            address="300 Delete Rd",
            city="Montreal",
            state="QC",
            zip_code="34567",
            comm_pref="Email",
            pref_pharmacy="Delete Pharmacy",
        )

        created = patient_service.create_patient(temp_patient)
        assert created is not None
        assert created.patient_id is not None

        deleted = patient_service.delete_patient(created.patient_id)

        assert deleted is True
        assert patient_service.get_patient_by_id(created.patient_id) is None


# ----------------------------------------------------------------
# Patient Dashboard
# ----------------------------------------------------------------

class TestPatientDashboard:
    """Tests for dashboard aggregation logic."""

    def test_dashboard_returns_object_for_valid_patient(self, patient_service):
        """Should return a PatientDashboard for a valid patient ID."""
        result = patient_service.get_patient_dashboard(1)

        assert result is not None
        assert isinstance(result, PatientDashboard)
        assert result.patient is not None
        assert result.patient.patient_id == 1

    def test_dashboard_returns_none_for_missing_patient(self, patient_service):
        """Should return None for a non-existent patient ID."""
        result = patient_service.get_patient_dashboard(99999)
        assert result is None

    def test_dashboard_contains_expected_sections(self, patient_service):
        """Dashboard should include patient, insurance, prescriptions, appointments."""
        result = patient_service.get_patient_dashboard(1)

        assert result is not None
        assert hasattr(result, "patient")
        assert hasattr(result, "insurance_coverage")
        assert hasattr(result, "active_prescriptions")
        assert hasattr(result, "upcoming_appointments")

        assert isinstance(result.insurance_coverage, list)
        assert isinstance(result.active_prescriptions, list)
        assert isinstance(result.upcoming_appointments, list)

    def test_dashboard_active_prescriptions_are_active(self, patient_service):
        """All prescriptions in dashboard should have active status."""
        result = patient_service.get_patient_dashboard(1)

        assert result is not None
        for rx in result.active_prescriptions:
            assert rx.patient_id == 1
            assert rx.status == "active"

    def test_dashboard_upcoming_appointments_are_scheduled_for_patient(self, patient_service):
        """Appointments in dashboard should belong to patient and be scheduled."""
        result = patient_service.get_patient_dashboard(1)

        assert result is not None
        today = date.today()

        for appt in result.upcoming_appointments:
            assert appt.patient_id == 1
            assert appt.status == "scheduled"
            assert appt.appt_date >= today


# ----------------------------------------------------------------
# Polypharmacy Risk
# ----------------------------------------------------------------

class TestPolypharmacyPatients:
    """Tests for polypharmacy detection."""

    def test_returns_list(self, patient_service):
        """Should return a list of (patient, count) tuples."""
        results = patient_service.get_polypharmacy_patients()

        assert isinstance(results, list)
        if len(results) > 0:
            patient, count = results[0]
            assert isinstance(patient, Patient)
            assert isinstance(count, int)

    def test_results_meet_threshold(self, patient_service):
        """Each returned patient should meet or exceed the threshold."""
        threshold = 5
        results = patient_service.get_polypharmacy_patients(threshold=threshold)

        for patient, count in results:
            assert count >= threshold
            assert isinstance(patient, Patient)

    def test_results_sorted_by_count_descending(self, patient_service):
        """Results should be sorted by prescription count descending."""
        results = patient_service.get_polypharmacy_patients(threshold=1)

        if len(results) >= 2:
            counts = [count for _, count in results]
            assert counts == sorted(counts, reverse=True)

    def test_high_threshold_returns_empty(self, patient_service):
        """Very high threshold should usually return no results."""
        results = patient_service.get_polypharmacy_patients(threshold=100)
        assert results == []


# ----------------------------------------------------------------
# Search Patients by Name
# ----------------------------------------------------------------

class TestSearchPatientsByName:
    """Tests for patient name search."""

    def test_search_returns_list(self, patient_service):
        """Search should return a list."""
        results = patient_service.search_patients_by_name("a")
        assert isinstance(results, list)

    def test_search_finds_matches_case_insensitive(self, patient_service):
        """Search should be case-insensitive."""
        lower_results = patient_service.search_patients_by_name("john")
        upper_results = patient_service.search_patients_by_name("JOHN")

        lower_ids = sorted([p.patient_id for p in lower_results])
        upper_ids = sorted([p.patient_id for p in upper_results])

        assert lower_ids == upper_ids

    def test_search_returns_empty_for_no_match(self, patient_service):
        """Search should return an empty list when there is no match."""
        results = patient_service.search_patients_by_name("zzzzzz_nonexistent_name")
        assert results == []


# ----------------------------------------------------------------
# Edge Cases
# ----------------------------------------------------------------

class TestServiceEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_delete_missing_patient_returns_false(self, patient_service):
        """Deleting a missing patient should return False."""
        result = patient_service.delete_patient(99999)
        assert result is False