#  🩺 GP3 Polyglot Healthcare Database Management System

This project is Team 6’s submission for GP3; a complete polyglot healthcare management platform using PostgreSQL, MongoDB, and Neo4j within a Dockerized environment.
The system combines transactional healthcare operations, flexible clinical document storage, and graph-based clinical decision support into a unified healthcare platform.

---

## 🎯 Learning Objectives

By completing this group project, we were able to achived the following:
* Recognize when document databases are appropriate for clinical data
* Design flexible document schemas for clinical documentation
* Choose embedding vs. referencing for healthcare data
* Write MongoDB aggregation pipelines and text search on clinical narratives
* Design medical knowledge graphs with clinically meaningful relationships
* Write Cypher queries for drug interaction checking
* Implement clinical decision support using graph traversals
* Build a complete three-database healthcare architecture
* Deploy polyglot systems using Docker Compose
* Document complex clinical systems professionally

---

## 🧩 Polyglot Database Architecture

This project uses a polyglot persistence architecture where each database is responsible for a specialized workload.

| Database   | Purpose                                                       |
| ---------- | ------------------------------------------------------------- |
| PostgreSQL | Transactional healthcare records                              |
| MongoDB    | Flexible clinical/document data                               |
| Neo4j      | Clinical decision support and drug interaction graph analysis |

🐳Docker Compose orchestrates all services together.

---

# ✨ System Features

## 🐘 PostgreSQL Features

* Patient management
* Appointment scheduling
* Prescription management
* Insurance tracking
* Billing support
* Polypharmacy reporting
* Provider workload analytics

## 🍃 MongoDB Features

* Flexible patient clinical notes
* Symptom logs
* Medical history records
* Semi-structured healthcare documents

## 🧠 Neo4j Features

* Drug interaction analysis
* Clinical knowledge graph
* Prescription safety checks
* Relationship-based healthcare analytics

---

## 💻 Technologies Used

* Python 3.11
* PostgreSQL 14
* MongoDB 6
* Neo4j 5
* Docker
* Docker Compose
* psycopg3
* MongoDB Compass
* Neo4j Browser

---

## 📁 Project Structure

GP3_Healthcare_Team{X}/
├── postgresql/                 # From GP2
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
├── config/
│   ├── database.py             # Existing from GP2
│   ├── mongodb.py              # New
│   └── neo4j_config.py         # New
├── models/                       # Existing from GP2
│   └── [entity].py
├── repositories/
│   ├── postgres/               # Existing from GP2
│   ├── mongodb/
│   └── neo4j/
├── services/
│   ├── clinical_service.py     # Existing, now cross-database
│   └── prescription_safety.py  # New: uses Neo4j
├── cli/
│   └── main.py                 # Updated with 2+ unified operations
├── docs/
│   ├── polyglot_design.pdf      # Partitioning, MongoDB schemas,
│   │                           # Neo4j node/rel catalog, indexes
│   └── technical_report.pdf
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example              # template with placeholder values
├── .env                      # actual values (committed for
│                             # grading -- see policy below)
├── README.md
└── team_contributions.md

---

# 📋 Prerequisites

Before starting, install:

* Docker Desktop
* Docker Compose
* Git

---

## 🐳 Setup Instructions

## Step 1 — Clone the Repository

```bash
git clone https://github.com/EtsubdinkY/GP2_Healthcare_team_6.git
cd GP2_Healthcare_team_6
```

---

## Step 2 — Start the Full System

```bash
docker compose up --build
```

This automatically starts:

* PostgreSQL
* MongoDB
* Neo4j
* Python Healthcare CLI Application

It also automatically:

* creates databases
* loads schemas
* seeds test data
* initializes MongoDB collections
* starts Neo4j services

---

## 🌐 Service Access Information

| Service       | Port  |
| ------------- | ----- |
| PostgreSQL    | 5433  |
| MongoDB       | 27017 |
| Neo4j Browser | 7474  |
| Neo4j Bolt    | 7687  |

---

## 🐘 PostgreSQL Connection Information

Use these credentials for DataGrip, pgAdmin, or VS Code Database Explorer:

```text
Host: localhost
Port: 5433
Database: healthcare_management
User: healthcare_admin
Password: enpm818t
```

---

## 🍃 MongoDB Connection

For MongoDB Compass:

```text
mongodb://localhost:27017
```

---

## 🧠 Neo4j Browser

Open in browser:

```text
http://localhost:7474
```

Credentials:

```text
Username: neo4j
Password: enpm818t-neo4j
```

---

# ▶️Running the Application

The Python CLI application automatically starts when Docker Compose launches.

You should see:

```text
##################################################
#                                                #
#       HEALTHCARE MANAGEMENT SYSTEM             #
#                                                #
##################################################
```

---

# 📋 CLI Features

## 1. 👨‍⚕️Patient Management

* View patient records
* Add/update/delete patients
* Search patients
* View patient dashboards
* Polypharmacy risk reports

## 2. 📅Appointment Management

* Schedule appointments
* View upcoming appointments
* Cancel/update appointments
* Provider scheduling analytics

## 3. 💊Prescription Management

* Create prescriptions
* Update/discontinue medications
* Controlled substance reporting
* Prescription history tracking

## 4. 📊Quick Views

* Upcoming appointments
* Active prescriptions
* Polypharmacy analytics

## 🔄 GP3 Cross-Database Operations

* PostgreSQL transactional queries
* MongoDB clinical document retrieval
* Neo4j drug interaction analysis
* Cross-database healthcare analytics

---

# 🧪 SQL Analytics Queries

The `postgresql/queries.sql` file contains advanced healthcare analytics queries including:

1. Patient care coordination
2. Polypharmacy risk analysis
3. Provider workload analysis
4. Insurance coverage breakdown
5. Prescription cost analysis
6. Provider productivity metrics
7. Controlled substances reporting
8. Appointment status analytics

---

# 🏗️ Architecture Design

The system uses a layered architecture:

| Layer        | Purpose                                  |
| ------------ | ---------------------------------------- |
| Config       | Database connection management           |
| Models       | Python dataclasses representing entities |
| Repositories | Database interaction layer               |
| Services     | Business logic layer                     |
| CLI          | User interface layer                     |

---

# 🔒Security Considerations

* Credentials are isolated within Docker containers
* Parameterized SQL queries are used throughout
* Synthetic healthcare data only
* No real patient data is stored
* Database access separated by service boundaries

---

# 🛑 Stopping the System

```bash
docker compose down
```

---

# 🔁 Restarting the System

```bash
docker compose up
```

---

# ⚠️ Notes

* Neo4j is used for graph-based clinical decision support.
* MongoDB stores semi-structured clinical information.
* PostgreSQL maintains transactional consistency for healthcare operations.
* Docker volumes preserve database data between restarts.

---

# 👩‍💻 Contributers

* Louis Tafah
* Pushkar Vishwas
* Adyasha Mishra
* Etsubdink Workalemahu Yergashewa
