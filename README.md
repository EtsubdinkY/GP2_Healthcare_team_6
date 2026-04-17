# GP2 Healthcare Management System

This is our team's submission for GP2 — a PostgreSQL-backed healthcare app with a Python CLI for handling patients, appointments, and prescriptions.

## Team 6

- Louis Tafah
- Pushkar Vishwas
- Adyasha Mishra
- Etsubdink Workalemahu Yergashewa

## What You Need Before Starting

- Python 3.10+
- PostgreSQL 14+
- pip

## How the Project Is Organized

```
GP2_Healthcare_team_6/
├── postgresql/
│   ├── schema.sql          # all the tables, constraints, triggers
│   ├── data.sql            # test data we generated
│   └── queries.sql         # the 8 SQL queries
├── src/
│   ├── config/
│   │   └── database.py     # sets up connection pooling
│   ├── models/
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   ├── prescription.py
│   │   ├── provider.py
│   │   ├── medication.py
│   │   ├── hospital.py
│   │   └── patient_insurance.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── patient_repo.py
│   │   ├── appointment_repo.py
│   │   ├── prescription_repo.py
│   │   ├── provider_repo.py
│   │   ├── patient_insurance_repo.py
│   │   ├── medication_repo.py
│   │   └── hospital_repo.py
│   ├── services/
│   │   ├── patient_service.py
│   │   ├── appointment_service.py
│   │   └── prescription_service.py
│   └── cli/
│       └── main.py
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Step 1 — Clone the repo

```bash
git clone https://github.com/EtsubdinkY/GP2_Healthcare_team_6.git
cd GP2_Healthcare_team_6
```

### Step 2 — Set up a virtual environment (recommended)

```bash
python -m venv venv

# on Windows:
venv\Scripts\activate

# on Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install the dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up your environment variables

Copy `.env.example` to `.env` and fill in your own database info:

```bash
cp .env.example .env
```

The `.env` file should look something like this:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=healthcare_management
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_POOL_MIN_SIZE=1
DB_POOL_MAX_SIZE=5
```

### Step 5 — Create and load the database

```bash
psql -U postgres
```

Inside psql:

```sql
CREATE DATABASE healthcare_management;
\q
```

Then from your terminal:

```bash
psql -U postgres -d healthcare_management -f postgresql/schema.sql
psql -U postgres -d healthcare_management -f postgresql/data.sql
```

## Running It

From the project root:

```bash
python -m src.cli.main
```

## What the CLI Can Do

The main menu has four sections:

**1. Patient Management**
- list patients, view details, see full dashboard
- add / update / delete patients
- search by name
- polypharmacy risk report (patients on 5+ active meds)

**2. Appointment Management**
- list and view appointments
- see upcoming scheduled ones
- schedule new, update, or cancel existing
- filter by date

**3. Prescription Management**
- list and view prescriptions
- create, update, discontinue
- patient prescription history
- controlled substances report

**4. Quick Views**
- upcoming appointments
- active prescriptions
- polypharmacy flag

## The SQL Queries

`postgresql/queries.sql` has 8 queries:

1. Patient care coordination — pulls demographics, insurance, and active meds for incoming patients
2. Polypharmacy risk — flags patients on 5 or more active prescriptions
3. Provider workload — counts upcoming appointments per provider
4. Insurance coverage breakdown by plan
5. Prescription cost and coverage analysis
6. Provider productivity metrics
7. Controlled substances report (Schedule II, DEA)
8. Appointment status breakdown by facility

## Architecture Notes

We went with a layered approach:

- **Config** — connection pool setup via psycopg3
- **Models** — Python dataclasses that mirror the DB tables, each with a `from_row()` method
- **Repositories** — one per table, handles all SQL; patients/appointments/prescriptions are full CRUD, the rest are read-only
- **Services** — business logic lives here, calls into multiple repos as needed
- **CLI** — menu-driven interface, calls into the service layer

## Python Dependencies

- `psycopg[binary]` 3.1.18
- `psycopg-pool` 3.2.2
- `python-dotenv` 1.0.1

## A Note on Security

Credentials stay in `.env` which is gitignored. All queries use parameterized statements (no string formatting into SQL). SSN fields are optional. This project only uses synthetic data — nothing real.
