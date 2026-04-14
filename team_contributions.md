# Team Contributions - GP2 Healthcare Management System

## Team 6 Members

| Member | Name | Responsibility |
|--------|------|----------------|
| Member 1 | Louis Tafah | schema.sql + constraints + triggers |
| Member 2 | Etsubdink Workalemahu Yergashewa | data.sql + queries.sql |
| Member 3 | Adyasha Mishra | Python repos + models + database config |
| Member 4 | Pushkar Vishwas | Python services + CLI + documentation |

## Detailed Contributions

### Member 1: Louis Tafah - Database Schema
**Tasks Completed:**
- Designed and implemented `schema.sql` with all tables from GP1 design
- Created ENUM types for healthcare values (appointment_status, rx_status, etc.)
- Implemented primary keys, foreign keys with ON DELETE/UPDATE rules
- Added CHECK constraints for business rules
- Created healthcare identifier constraints (MRN format, NPI format, DEA requirements)
- Implemented indexes for clinical query patterns
- Created triggers for automatic `updated_at` timestamps

**Contribution Percentage:** 25%

---

### Member 2: Etsubdink Workalemahu Yergashewa - Data and Queries
**Tasks Completed:**
- Generated synthetic test data in `data.sql` for all tables
- Ensured data meets minimum volume requirements
- Created realistic clinical patterns in test data
- Wrote 8 SQL queries in `queries.sql`:
  1. Patient Care Coordination
  2. Medication Safety (Polypharmacy Risk)
  3. Provider Workload
  4. Insurance Coverage Summary
  5. Prescription Cost Analysis
  6. Provider Productivity
  7. Controlled Substances Report
  8. Appointment Status by Facility
- Documented each query with clinical/business justification

**Contribution Percentage:** 25%

---

### Member 3: Adyasha Mishra - Python Data Layer
**Tasks Completed:**
- Implemented database connection pooling (`config/database.py`)
- Created dataclass models for all entities:
  - Patient, Appointment, Prescription (core tables)
  - Provider, PatientInsurance (read-only tables)
  - Medication, Hospital (supporting tables)
- Implemented `from_row()` factory methods for database mapping
- Created BaseRepository with CRUD operations
- Implemented full CRUD repositories:
  - PatientRepository
  - AppointmentRepository
  - PrescriptionRepository
- Implemented read-only repositories:
  - ProviderRepository
  - PatientInsuranceRepository
  - MedicationRepository
  - HospitalRepository

**Contribution Percentage:** 25%

---

### Member 4: Pushkar Vishwas - Services, CLI, Documentation
**Tasks Completed:**
- Implemented service layer with business logic:
  - `PatientService` with patient dashboard and polypharmacy detection
  - `AppointmentService` with scheduling and provider schedule views
  - `PrescriptionService` with controlled substance reporting
- Built menu-driven CLI application (`cli/main.py`):
  - Patient Management (8 menu options)
  - Appointment Management (8 menu options)
  - Prescription Management (9 menu options)
  - Quick views for common operations
- Created comprehensive documentation:
  - README.md with setup and usage instructions
  - team_contributions.md (this file)
- Input validation and error handling in CLI
- Color-coded terminal output for better UX

**Contribution Percentage:** 25%

---

## Summary

| Member | Name | Tasks | Contribution |
|--------|------|-------|--------------|
| Member 1 | Louis Tafah | Schema, constraints, triggers | 25% |
| Member 2 | Etsubdink Workalemahu Yergashewa | Data generation, SQL queries | 25% |
| Member 3 | Adyasha Mishra | Models, repositories, config | 25% |
| Member 4 | Pushkar Vishwas | Services, CLI, documentation | 25% |
| **Total** | | | **100%** |
