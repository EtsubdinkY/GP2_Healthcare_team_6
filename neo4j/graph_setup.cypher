// Neo4j Graph Setup for Healthcare System
// Creates constraints and indexes for the knowledge graph

// Constraints for unique IDs
CREATE CONSTRAINT medication_id_unique IF NOT EXISTS
FOR (m:Medication) REQUIRE m.med_id IS UNIQUE;

CREATE CONSTRAINT drugclass_name_unique IF NOT EXISTS
FOR (dc:DrugClass) REQUIRE dc.name IS UNIQUE;

CREATE CONSTRAINT allergen_name_unique IF NOT EXISTS
FOR (a:Allergen) REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT patient_id_unique IF NOT EXISTS
FOR (p:Patient) REQUIRE p.patient_id IS UNIQUE;

CREATE CONSTRAINT provider_id_unique IF NOT EXISTS
FOR (pr:Provider) REQUIRE pr.provider_id IS UNIQUE;

CREATE CONSTRAINT department_id_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.dept_id IS UNIQUE;

CREATE CONSTRAINT hospital_id_unique IF NOT EXISTS
FOR (h:Hospital) REQUIRE h.hospital_id IS UNIQUE;

CREATE CONSTRAINT disease_icd10_unique IF NOT EXISTS
FOR (d:Disease) REQUIRE d.icd10 IS UNIQUE;

CREATE CONSTRAINT symptom_name_unique IF NOT EXISTS
FOR (s:Symptom) REQUIRE s.name IS UNIQUE;

// Indexes for faster lookups
CREATE INDEX medication_name_index IF NOT EXISTS
FOR (m:Medication) ON (m.name);

CREATE INDEX medication_generic_index IF NOT EXISTS
FOR (m:Medication) ON (m.generic_name);

CREATE INDEX patient_mrn_index IF NOT EXISTS
FOR (p:Patient) ON (p.mrn);

CREATE INDEX provider_specialty_index IF NOT EXISTS
FOR (pr:Provider) ON (pr.specialty);

CREATE INDEX provider_npi_index IF NOT EXISTS
FOR (pr:Provider) ON (pr.npi);

CREATE INDEX hospital_name_index IF NOT EXISTS
FOR (h:Hospital) ON (h.name);

CREATE INDEX disease_name_index IF NOT EXISTS
FOR (d:Disease) ON (d.name);

CREATE INDEX disease_category_index IF NOT EXISTS
FOR (d:Disease) ON (d.category);

CREATE INDEX symptom_body_system_index IF NOT EXISTS
FOR (s:Symptom) ON (s.body_system);
