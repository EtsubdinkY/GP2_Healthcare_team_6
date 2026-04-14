"""
Test suite for repository classes.

These tests verify that your repositories correctly interact with the
PostgreSQL database. Each test should use a real database connection
(not mocks) so you are testing actual SQL execution.
"""

from datetime import date
import pytest

from src.config.database import get_pool, close_pool
from src.models.patient import Patient
from src.repositories.patient_repo import PatientRepository


@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    """Initialize the connection pool once for the entire test session."""
    get_pool()
    yield
    close_pool()


@pytest.fixture
def patient_repo():
    """Provide a fresh PatientRepository instance for each test."""
    return PatientRepository()


class TestPatientRepository:
    """Tests for PatientRepository CRUD operations."""

    def test_find_by_id_returns_entity(self, patient_repo):
        """find_by_id() should return a Patient for a known ID."""
        known_id = 1
        result = patient_repo.find_by_id(known_id)

        assert result is not None
        assert result.patient_id == known_id
        assert result.mrn is not None
        assert result.first_name is not None
        assert result.last_name is not None

    def test_find_by_id_returns_none_for_missing(self, patient_repo):
        """find_by_id() should return None for a non-existent ID."""
        result = patient_repo.find_by_id(99999)
        assert result is None

    def test_find_all_returns_list(self, patient_repo):
        """find_all() should return a list of Patient objects."""
        results = patient_repo.find_all()

        assert isinstance(results, list)
        assert len(results) > 0

        first = results[0]
        assert isinstance(first, Patient)
        assert first.patient_id is not None
        assert first.mrn is not None

    def test_find_all_returns_patients_ordered_by_id(self, patient_repo):
        """find_all() should return patients ordered by patient_id."""
        results = patient_repo.find_all()
        ids = [patient.patient_id for patient in results]
        assert ids == sorted(ids)

    def test_create_and_retrieve(self, patient_repo):
        """create() should insert a record that can then be retrieved."""
        new_patient = Patient(
            patient_id=None,
            mrn="9999999999",
            ssn=None,
            first_name="Test",
            last_name="Patient",
            dob=date(1990, 1, 1),
            gender="Female",
            phone="555-111-2222",
            email="test.patient@example.com",
            address="123 Test Street",
            city="Ottawa",
            state="ON",
            zip_code="12345",
            comm_pref="Email",
            pref_pharmacy="Test Pharmacy",
        )

        created = patient_repo.create(new_patient)

        assert created is not None
        assert created.patient_id is not None
        assert created.mrn == "9999999999"

        retrieved = patient_repo.find_by_id(created.patient_id)
        assert retrieved is not None
        assert retrieved.patient_id == created.patient_id
        assert retrieved.mrn == "9999999999"
        assert retrieved.first_name == "Test"
        assert retrieved.last_name == "Patient"

        assert patient_repo.delete(created.patient_id) is True

    def test_update_persists_changes(self, patient_repo):
        """update() should modify a record so changes persist."""
        temp_patient = Patient(
            patient_id=None,
            mrn="8888888888",
            ssn=None,
            first_name="Original",
            last_name="Patient",
            dob=date(1992, 2, 2),
            gender="Male",
            phone="555-222-3333",
            email="original.patient@example.com",
            address="456 Original Ave",
            city="Toronto",
            state="ON",
            zip_code="23456",
            comm_pref="Phone",
            pref_pharmacy="Original Pharmacy",
        )

        created = patient_repo.create(temp_patient)
        assert created is not None
        assert created.patient_id is not None

        updated_patient = Patient(
            patient_id=created.patient_id,
            mrn=created.mrn,
            ssn=created.ssn,
            first_name="Updated",
            last_name="Patient",
            dob=created.dob,
            gender=created.gender,
            phone="555-000-0000",
            email="updated.patient@example.com",
            address=created.address,
            city=created.city,
            state=created.state,
            zip_code=created.zip_code,
            comm_pref="Email",
            pref_pharmacy="Updated Pharmacy",
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

        result = patient_repo.update(created.patient_id, updated_patient)

        assert result is not None
        assert result.first_name == "Updated"
        assert result.phone == "555-000-0000"
        assert result.email == "updated.patient@example.com"
        assert result.comm_pref == "Email"
        assert result.pref_pharmacy == "Updated Pharmacy"

        retrieved = patient_repo.find_by_id(created.patient_id)
        assert retrieved is not None
        assert retrieved.first_name == "Updated"
        assert retrieved.phone == "555-000-0000"

        assert patient_repo.delete(created.patient_id) is True

    def test_delete_removes_record(self, patient_repo):
        """delete() should remove a record so it can no longer be found."""
        temp_patient = Patient(
            patient_id=None,
            mrn="7777777777",
            ssn=None,
            first_name="Delete",
            last_name="Me",
            dob=date(1995, 5, 5),
            gender="Female",
            phone="555-333-4444",
            email="delete.me@example.com",
            address="789 Delete Rd",
            city="Montreal",
            state="QC",
            zip_code="34567",
            comm_pref="Email",
            pref_pharmacy="Delete Pharmacy",
        )

        created = patient_repo.create(temp_patient)
        assert created is not None
        assert created.patient_id is not None

        deleted = patient_repo.delete(created.patient_id)

        assert deleted is True
        assert patient_repo.find_by_id(created.patient_id) is None

    def test_create_duplicate_mrn_raises_error(self, patient_repo):
        """Inserting a duplicate MRN should raise an exception."""
        first_patient = Patient(
            patient_id=None,
            mrn="6666666666",
            ssn=None,
            first_name="First",
            last_name="Duplicate",
            dob=date(1991, 6, 6),
            gender="Male",
            phone="555-444-5555",
            email="first.duplicate@example.com",
            address="111 First St",
            city="Calgary",
            state="AB",
            zip_code="45678",
            comm_pref="Email",
            pref_pharmacy="First Pharmacy",
        )

        created = patient_repo.create(first_patient)
        assert created is not None

        duplicate_patient = Patient(
            patient_id=None,
            mrn="6666666666",
            ssn=None,
            first_name="Second",
            last_name="Duplicate",
            dob=date(1993, 3, 3),
            gender="Female",
            phone="555-555-6666",
            email="second.duplicate@example.com",
            address="222 Second St",
            city="Edmonton",
            state="AB",
            zip_code="56789",
            comm_pref="Phone",
            pref_pharmacy="Second Pharmacy",
        )

        with pytest.raises(Exception):
            patient_repo.create(duplicate_patient)

        assert patient_repo.delete(created.patient_id) is True

    def test_delete_returns_false_for_missing_record(self, patient_repo):
        """Deleting a non-existent patient should return False."""
        result = patient_repo.delete(99999)
        assert result is False