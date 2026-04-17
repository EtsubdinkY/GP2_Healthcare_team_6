# Team Contributions

## GP2 — Healthcare Management System
### Team 6

---

### Louis Tafah — Database Schema

- Designed `schema.sql` from the GP1 ER diagram
- Set up all ENUM types (appointment statuses, rx statuses, etc.)
- Defined foreign key relationships, including cascade vs. restrict rules
- Added CHECK constraints for MRN and NPI format validation
- Created indexes to support the clinical queries
- Wrote triggers for auto-updating `updated_at` timestamps on all relevant tables

**Contribution: 25%**

---

### Etsubdink Workalemahu Yergashewa — Test Data and SQL Queries

- Wrote synthetic data in `data.sql` with enough rows across all tables to properly test the queries
- Made sure the data reflects realistic clinical patterns (not just random values)
- Wrote all 8 SQL queries in `queries.sql`:
  1. Patient care coordination
  2. Polypharmacy risk detection
  3. Provider workload
  4. Insurance coverage summary
  5. Prescription cost analysis
  6. Provider productivity
  7. Controlled substances report (Schedule II)
  8. Appointment status breakdown by facility
- Added comments to each query explaining the clinical/operational use case

**Contribution: 25%**

---

### Adyasha Mishra — Models, Repositories, Database Config

- Set up connection pooling in `config/database.py` using psycopg3
- Built dataclass models for all tables: Patient, Appointment, Prescription, Provider, PatientInsurance, Medication, Hospital
- Added `from_row()` factory methods to each model for mapping DB results
- Wrote `BaseRepository` with shared CRUD logic to avoid repeating code
- Implemented full CRUD repositories for Patient, Appointment, Prescription
- Implemented read-only repositories for Provider, PatientInsurance, Medication, Hospital

**Contribution: 25%**

---

### Pushkar Vishwas — Services, CLI, Documentation

- Built the service layer on top of the repositories:
  - `PatientService` — patient dashboard, name search, polypharmacy detection
  - `AppointmentService` — scheduling, cancellation, provider schedule view, date filtering
  - `PrescriptionService` — active/controlled substance reports, discontinuation
- Built the menu-driven CLI in `cli/main.py` with four main sections and input validation
- Added color-coded terminal output to make results easier to read
- Wrote the README and this contributions file

**Contribution: 25%**

---

## Summary

| Member | Area | % |
|--------|------|---|
| Louis Tafah | Schema, constraints, triggers | 25% |
| Etsubdink Workalemahu Yergashewa | Data generation, SQL queries | 25% |
| Adyasha Mishra | Models, repositories, DB config | 25% |
| Pushkar Vishwas | Services, CLI, documentation | 25% |
