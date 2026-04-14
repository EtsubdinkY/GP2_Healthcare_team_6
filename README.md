# Healthcare Management System

A PostgreSQL-based healthcare management application with a Python CLI interface for managing patients, appointments, and prescriptions.

## Team 6

- Louis Tafah
- Pushkar Vishwas
- Adyasha Mishra
- Etsubdink Workalemahu Yergashewa

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)

## Project Structure

```
GP2_Healthcare_team_6/
├── postgresql/
│   ├── schema.sql          # Database schema with tables, constraints, triggers
│   ├── data.sql            # Synthetic test data
│   └── queries.sql         # 8+ clinical/operational SQL queries
├── src/
│   ├── config/
│   │   └── database.py     # Connection pooling configuration
│   ├── models/
│   │   ├── patient.py      # Patient dataclass
│   │   ├── appointment.py  # Appointment dataclass
│   │   ├── prescription.py # Prescription dataclass
│   │   ├── provider.py     # Provider dataclass
│   │   ├── medication.py   # Medication dataclass
│   │   ├── hospital.py     # Hospital dataclass
│   │   └── patient_insurance.py  # Insurance dataclass
│   ├── repositories/
│   │   ├── base_repository.py    # Base CRUD operations
│   │   ├── patient_repo.py       # Full CRUD for patients
│   │   ├── appointment_repo.py   # Full CRUD for appointments
│   │   ├── prescription_repo.py  # Full CRUD for prescriptions
│   │   ├── provider_repo.py      # Read-only for providers
│   │   ├── patient_insurance_repo.py  # Read-only for insurance
│   │   ├── medication_repo.py    # Read-only for medications
│   │   └── hospital_repo.py      # Read-only for hospitals
│   ├── services/
│   │   ├── patient_service.py    # Patient business logic
│   │   ├── appointment_service.py # Appointment business logic
│   │   └── prescription_service.py # Prescription business logic
│   └── cli/
│       └── main.py         # Menu-driven CLI application
├── tests/                  # Optional test files
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/EtsubdinkY/GP2_Healthcare_team_6.git
cd GP2_Healthcare_team_6
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL connection details:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=healthcare_management
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_POOL_MIN_SIZE=1
DB_POOL_MAX_SIZE=5
```

### 5. Set Up the Database

Create the database and load the schema:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE healthcare_management;

# Exit psql
\q

# Load schema
psql -U postgres -d healthcare_management -f postgresql/schema.sql

# Load sample data
psql -U postgres -d healthcare_management -f postgresql/data.sql
```

## Running the Application

From the project root directory:

```bash
python -m src.cli.main
```

## CLI Features

### Main Menu
1. **Patient Management** - Full CRUD operations for patients
2. **Appointment Management** - Schedule, update, cancel appointments
3. **Prescription Management** - Manage prescriptions and medications
4. **Quick Views** - Upcoming appointments, active prescriptions, polypharmacy risk

### Patient Management
- List all patients
- View patient details
- View patient dashboard (demographics, insurance, prescriptions, appointments)
- Add, update, delete patients
- Search patients by name
- Polypharmacy risk report (5+ active prescriptions)

### Appointment Management
- List all appointments
- View appointment details with patient/provider info
- View upcoming scheduled appointments
- Schedule new appointments
- Update or cancel appointments
- View appointments by date

### Prescription Management
- List all prescriptions
- View prescription details with medication/patient/provider info
- View active prescriptions
- Create, update, discontinue prescriptions
- View patient prescription history
- Controlled substances report (DEA compliance)

## SQL Queries

The `postgresql/queries.sql` file contains 8 documented queries:

1. **Patient Care Coordination** - Demographics, insurance, active prescriptions for arriving patients
2. **Medication Safety** - Polypharmacy risk detection (5+ active prescriptions)
3. **Provider Workload** - Upcoming appointments per provider
4. **Insurance Coverage Summary** - Coverage statistics by plan
5. **Prescription Cost Analysis** - Cost and coverage breakdown
6. **Provider Productivity** - Appointment metrics by provider
7. **Controlled Substances Report** - Schedule II DEA reporting
8. **Appointment Status by Facility** - Status breakdown per facility

## Architecture

### Layered Architecture

- **Config Layer** (`config/database.py`): Connection pooling with psycopg3
- **Model Layer** (`models/`): Python dataclasses mirroring database tables
- **Repository Layer** (`repositories/`): Data access with parameterized queries
- **Service Layer** (`services/`): Business logic combining multiple repositories
- **CLI Layer** (`cli/`): User interface with menu-driven navigation

### Design Patterns

- **Repository Pattern**: Abstracts database operations from business logic
- **Service Layer**: Encapsulates business rules and coordinates repositories
- **Dataclass Models**: Type-safe domain objects with `from_row()` factory methods
- **Connection Pooling**: Efficient database connection management

## Dependencies

- `psycopg[binary]` (3.1.18) - PostgreSQL adapter for Python
- `psycopg-pool` (3.2.2) - Connection pooling
- `python-dotenv` (1.0.1) - Environment variable management

## Security Notes

- Database credentials are stored in `.env` (never committed to git)
- All SQL queries use parameterized statements to prevent SQL injection
- Sensitive data (SSN) is optional and should be handled according to HIPAA guidelines
- This is a demonstration project using synthetic data only

