# 🩺 GP3 Polyglot Healthcare Database Management System

This project is Team 6’s submission for Group Project 3 (GP3) for ENPM818T. It implements a complete polyglot healthcare management platform using PostgreSQL, MongoDB, and Neo4j deployed through Docker Compose.

The system combines transactional healthcare operations, flexible clinical document storage, and graph-based clinical decision support into a single integrated healthcare platform.

---

# System Architecture Overview

This project uses a polyglot persistence architecture where each database handles a specialized workload.

| Database   | Responsibility |
|-----------|----------------|
| PostgreSQL | Transactional healthcare records including patients, providers, appointments, prescriptions, billing, admissions, and laboratory data |
| MongoDB | Semi-structured clinical documentation including notes, care plans, surveys, and imaging metadata |
| Neo4j | Clinical knowledge graph for medication interaction analysis and prescription safety decision support |

Docker Compose orchestrates all services into a unified deployment environment.

---

# Key Features

## PostgreSQL Features
- Patient management
- Appointment scheduling
- Prescription management
- Insurance tracking
- Billing workflows
- Laboratory orders and results
- Polypharmacy reporting
- Provider analytics

## MongoDB Features
- Flexible clinical note storage
- Care plans
- Patient surveys
- Medical imaging metadata
- Semi-structured healthcare document retrieval

## Neo4j Features
- Drug interaction analysis
- Clinical knowledge graph traversal
- Prescription safety validation
- Medication contraindication analysis

---

# Technology Stack

- Python 3.11
- PostgreSQL 14
- MongoDB 6
- Neo4j 5
- Docker
- Docker Compose
- psycopg3
- pymongo
- neo4j Python driver

---

# Project Structure

```text
GP2_Healthcare_team_6/
├── postgresql/
│   ├── schema.sql
│   ├── data.sql
│   └── queries.sql
├── mongodb/
│   ├── mongo_setup.js
│   ├── mongo_data.js
│   └── mongo_queries.js
├── neo4j/
│   ├── graph_setup.cypher
│   ├── graph_data.cypher
│   └── cypher_queries.cypher
├── src/
│   ├── config/
│   │   ├── database.py
│   │   ├── mongodb.py
│   │   └── neo4j_config.py
│   ├── models/
│   ├── repositories/
│   │   ├── postgres/
│   │   ├── mongodb/
│   │   └── neo4j/
│   ├── services/
│   └── cli/
│       └── main.py
├── docs/
│   ├── polyglot_design.pdf
│   └── technical_report.pdf
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .env
├── README.md
└── team_contributions.md
```

---

# Prerequisites

Install:

- Docker Desktop
- Docker Compose
- Git

No separate MongoDB, PostgreSQL, or Neo4j installation is required when using Docker Compose.

---

# Credentials for Grading

The assignment requires committed runtime credentials so the grader can run the system without manual changes.

## PostgreSQL
```text
Host: localhost
Port: 5433
Database: healthcare_management
User: healthcare_admin
Password: enpm818t
```

## MongoDB
```text
mongodb://localhost:27017
```

## Neo4j
```text
Browser URL: http://localhost:7474
Username: neo4j
Password: enpm818t-neo4j
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/EtsubdinkY/GP2_Healthcare_team_6.git
cd GP2_Healthcare_team_6
```

Note: The repository name remains GP2_Healthcare_team_6 because GP3 builds on the GP2 codebase.

---

## 2. Start the Full Polyglot System

```bash
docker-compose up --build
```

This starts:

- PostgreSQL
- MongoDB
- Neo4j
- Python application container

It also:

- loads PostgreSQL schema
- seeds PostgreSQL test data
- initializes MongoDB collections
- loads MongoDB sample documents
- initializes Neo4j graph
- starts the healthcare CLI application

---

## 3. Launch CLI

If needed:

```bash
docker exec -it healthcare_app python -m src.cli.main
```

---

# Service Access

| Service | Port |
|--------|------|
| PostgreSQL | 5433 |
| MongoDB | 27017 |
| Neo4j Browser | 7474 |
| Neo4j Bolt | 7687 |

---

# Unified Cross-Database Operations

## 1. Complete Patient Record

This workflow demonstrates all three databases working together.

### Databases Used

**PostgreSQL**
- patient demographics
- active prescriptions
- appointments
- laboratory results

**MongoDB**
- recent clinical notes
- care plans

**Neo4j**
- medication interaction safety analysis

This operation builds a unified patient record from all database systems.

---

## 2. Prescription Safety Check

This workflow provides clinical decision support during medication ordering.

### Databases Used

**PostgreSQL**
- patient validation
- active medication retrieval
- prescription insertion

**Neo4j**
- medication interaction lookup
- contraindication analysis

### Workflow

1. Validate patient in PostgreSQL
2. Retrieve active medications
3. Compare proposed medication against Neo4j knowledge graph
4. If unsafe:
   - display warnings
   - block prescription insertion
5. If safe:
   - allow provider confirmation
   - insert prescription into PostgreSQL

---

# Running the Application

Launch:

```bash
docker exec -it healthcare_app python -m src.cli.main
```

Main menu:

```text
##################################################
#                                                #
#       HEALTHCARE MANAGEMENT SYSTEM             #
#                                                #
##################################################
```

---

# Analytics and Query Support

## PostgreSQL
Healthcare reporting and analytics queries:

- patient care coordination
- provider workload analysis
- billing analytics
- prescription analytics
- controlled substances reporting
- appointment analytics
- polypharmacy risk analysis

## MongoDB
Clinical document queries:

- aggregation pipelines
- patient timeline analysis
- text search across clinical narratives
- array operations for care plans

## Neo4j
Clinical graph queries:

- medication interaction checking
- disease treatment pathways
- contraindication analysis
- clinical decision support traversals

---

# Security Notes

- Synthetic healthcare data only
- No real patient information
- Parameterized SQL queries used
- Environment-based configuration
- Database services isolated through Docker networking

---

# Stopping the System

```bash
docker-compose down
```

To remove volumes and fully reset:

```bash
docker-compose down -v
```

---

# Contributors

- Louis Tafah
- Pushkar Vishwas
- Adyasha Mishra
- Etsubdink Workalemahu Yergashewa
