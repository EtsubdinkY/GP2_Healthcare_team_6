# Knowledge Graph Repository for Neo4j

from dataclasses import dataclass
from src.config.neo4j_config import execute_query

@dataclass
class DrugInteraction:
    medication1: str
    medication2: str
    severity: str
    description: str

@dataclass
class AllergyContraindication:
    patient_id: int
    patient_name: str
    allergy: str
    contraindicated_medication: str


class KnowledgeGraphRepository:

    # Find drug interactions between a set of medications
    def find_interactions_for_medications(self, med_ids):
        query = """
        MATCH (m1:Medication)-[i:INTERACTS_WITH]->(m2:Medication)
        WHERE m1.med_id IN $med_ids AND m2.med_id IN $med_ids
        RETURN m1.name AS medication1, m2.name AS medication2,
               i.severity AS severity, i.description AS description
        ORDER BY CASE i.severity WHEN 'contraindicated' THEN 1 WHEN 'major' THEN 2 ELSE 3 END
        """
        results = execute_query(query, {"med_ids": med_ids})
        return [DrugInteraction(**r) for r in results]

    # Check if a new medication interacts with current medications
    def check_new_medication_interactions(self, new_med_id, current_med_ids):
        query = """
        MATCH (new_med:Medication {med_id: $new_med_id})-[i:INTERACTS_WITH]-(current:Medication)
        WHERE current.med_id IN $current_med_ids
        RETURN new_med.name AS medication1, current.name AS medication2,
               i.severity AS severity, i.description AS description
        ORDER BY CASE i.severity WHEN 'contraindicated' THEN 1 WHEN 'major' THEN 2 ELSE 3 END
        """
        results = execute_query(query, {"new_med_id": new_med_id, "current_med_ids": current_med_ids})
        return [DrugInteraction(**r) for r in results]

    # Find medications contraindicated for patient based on allergies
    def find_contraindicated_medications_for_patient(self, patient_id):
        query = """
        MATCH (p:Patient {patient_id: $patient_id})-[:ALLERGIC_TO]->(a:Allergen)
              <-[:CONTRAINDICATED_FOR]-(m:Medication)
        RETURN p.patient_id AS patient_id,
               p.first_name + ' ' + p.last_name AS patient_name,
               a.name AS allergy,
               m.name AS contraindicated_medication
        """
        results = execute_query(query, {"patient_id": patient_id})
        return [AllergyContraindication(**r) for r in results]

    # Check if a medication is safe for a patient
    def is_medication_safe_for_patient(self, patient_id, med_id):
        query = """
        MATCH (p:Patient {patient_id: $patient_id})
        OPTIONAL MATCH (p)-[:ALLERGIC_TO]->(a:Allergen)<-[contra:CONTRAINDICATED_FOR]-(m:Medication {med_id: $med_id})
        OPTIONAL MATCH (med:Medication {med_id: $med_id})
        RETURN p.first_name + ' ' + p.last_name AS patient_name,
               med.name AS medication_name,
               CASE WHEN contra IS NOT NULL THEN false ELSE true END AS is_safe,
               a.name AS conflicting_allergy
        """
        results = execute_query(query, {"patient_id": patient_id, "med_id": med_id})
        return results[0] if results else {}

    # Find top referral destinations by specialty
    def find_top_referral_destinations(self, specialty, limit=10):
        query = """
        MATCH (source:Provider {specialty: $specialty})-[r:REFERS_TO]->(target:Provider)
        RETURN source.first_name + ' ' + source.last_name AS from_provider,
               target.specialty AS to_specialty,
               target.first_name + ' ' + target.last_name AS to_provider,
               r.referral_count AS referral_count
        ORDER BY r.referral_count DESC
        LIMIT $limit
        """
        return execute_query(query, {"specialty": specialty, "limit": limit})

    # Find interactions between two drug classes
    def find_drug_class_interactions(self, class1, class2):
        query = """
        MATCH (m1:Medication)-[:BELONGS_TO]->(dc1:DrugClass {name: $class1})
        MATCH (m2:Medication)-[:BELONGS_TO]->(dc2:DrugClass {name: $class2})
        MATCH (m1)-[i:INTERACTS_WITH]-(m2)
        RETURN m1.name AS medication1, m2.name AS medication2,
               i.severity AS severity, i.description AS description
        """
        results = execute_query(query, {"class1": class1, "class2": class2})
        return [DrugInteraction(**r) for r in results]

    # Get hospital -> department -> provider hierarchy
    def get_organization_hierarchy(self):
        query = """
        MATCH (pr:Provider)-[:WORKS_IN]->(d:Department)-[:PART_OF]->(h:Hospital)
        RETURN h.name AS hospital, d.name AS department,
               pr.first_name + ' ' + pr.last_name AS provider, pr.specialty
        ORDER BY h.name, d.name
        """
        return execute_query(query, {})

    # Find patients with drug allergies
    def find_patients_with_drug_allergies(self):
        query = """
        MATCH (p:Patient)-[allergy:ALLERGIC_TO]->(a:Allergen {category: 'Drug'})
        OPTIONAL MATCH (m:Medication)-[:CONTRAINDICATED_FOR]->(a)
        RETURN p.patient_id AS patient_id,
               p.first_name + ' ' + p.last_name AS patient_name,
               a.name AS drug_allergy,
               allergy.severity AS severity,
               COLLECT(m.name) AS medications_to_avoid
        """
        return execute_query(query, {})

    # Get all interactions by severity level
    def get_all_interactions_by_severity(self, severity):
        query = """
        MATCH (m1:Medication)-[i:INTERACTS_WITH]->(m2:Medication)
        WHERE i.severity = $severity
        RETURN m1.name AS medication1, m2.name AS medication2,
               i.severity AS severity, i.description AS description
        """
        results = execute_query(query, {"severity": severity})
        return [DrugInteraction(**r) for r in results]
