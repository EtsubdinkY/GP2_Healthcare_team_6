// Cypher Queries for Healthcare Knowledge Graph

// 1. Find drug interactions for a patient's medications
MATCH (m1:Medication)-[i:INTERACTS_WITH]->(m2:Medication)
WHERE m1.med_id IN [5, 13, 24] AND m2.med_id IN [5, 13, 24]
RETURN m1.name AS drug1, m2.name AS drug2, i.severity, i.description
ORDER BY CASE i.severity WHEN 'contraindicated' THEN 1 WHEN 'major' THEN 2 ELSE 3 END;


// 2. Check if new med interacts with current meds (adding Tramadol)
MATCH (new_med:Medication {med_id: 12})-[i:INTERACTS_WITH]-(current:Medication)
WHERE current.med_id IN [8, 31]
RETURN new_med.name AS new_drug, current.name AS current_drug, i.severity, i.description;


// 3. Get contraindicated meds for patient with allergies
MATCH (p:Patient {patient_id: 1})-[:ALLERGIC_TO]->(a:Allergen)<-[:CONTRAINDICATED_FOR]-(m:Medication)
RETURN p.first_name + ' ' + p.last_name AS patient,
       a.name AS allergy,
       m.name AS avoid_medication,
       m.generic_name AS generic;


// 4. Check if Naproxen is safe for patient 6 (has Ibuprofen allergy)
MATCH (p:Patient {patient_id: 6})-[allergy:ALLERGIC_TO]->(a:Allergen)
OPTIONAL MATCH (m:Medication {med_id: 33})-[contra:CONTRAINDICATED_FOR]->(a)
RETURN p.first_name + ' ' + p.last_name AS patient,
       a.name AS allergy,
       CASE WHEN contra IS NOT NULL THEN 'DO NOT PRESCRIBE' ELSE 'Safe' END AS status;


// 5. Provider referral patterns - who does Family Medicine refer to?
MATCH (source:Provider {specialty: 'Family Physician'})-[r:REFERS_TO]->(target:Provider)
RETURN source.first_name + ' ' + source.last_name AS from_provider,
       target.specialty AS to_specialty,
       target.first_name + ' ' + target.last_name AS to_provider,
       r.referral_count AS referrals
ORDER BY r.referral_count DESC;


// 6. Opioid + Benzodiazepine interactions (dangerous combo)
MATCH (m1:Medication)-[:BELONGS_TO]->(dc1:DrugClass {name: 'Opioid Analgesic'})
MATCH (m2:Medication)-[:BELONGS_TO]->(dc2:DrugClass {name: 'Benzodiazepine'})
MATCH (m1)-[i:INTERACTS_WITH]-(m2)
RETURN m1.name AS opioid, m2.name AS benzodiazepine, i.severity;


// 7. Hospital -> Department -> Provider hierarchy
MATCH (pr:Provider)-[:WORKS_IN]->(d:Department)-[:PART_OF]->(h:Hospital)
RETURN h.name AS hospital, d.name AS department,
       pr.first_name + ' ' + pr.last_name AS provider, pr.specialty
ORDER BY h.name, d.name;


// 8. Patients with drug allergies and meds to avoid
MATCH (p:Patient)-[allergy:ALLERGIC_TO]->(a:Allergen {category: 'Drug'})
OPTIONAL MATCH (m:Medication)-[:CONTRAINDICATED_FOR]->(a)
RETURN p.patient_id, p.first_name + ' ' + p.last_name AS patient,
       a.name AS drug_allergy, allergy.severity,
       COLLECT(m.name) AS medications_to_avoid;


// 9. Disease pathway - find treatment options for a disease
MATCH (d:Disease {name: 'Hypertension'})-[:TREATED_BY]->(m:Medication)
OPTIONAL MATCH (m)-[:BELONGS_TO]->(dc:DrugClass)
RETURN d.name AS disease, d.icd10 AS icd10_code,
       m.name AS treatment, dc.name AS drug_class
ORDER BY m.name;


// 10. Disease symptoms and treatments (full pathway)
MATCH (d:Disease)-[p:PRESENTS_WITH]->(s:Symptom)
MATCH (d)-[t:TREATED_BY]->(m:Medication)
WHERE d.name = 'Type 2 Diabetes'
RETURN d.name AS disease,
       COLLECT(DISTINCT s.name) AS symptoms,
       COLLECT(DISTINCT m.name) AS treatments;


// 11. Check medication contraindication for disease
MATCH (m:Medication)-[c:CONTRAINDICATED_IN]->(d:Disease)
RETURN m.name AS medication, d.name AS disease,
       c.reason AS contraindication_reason
ORDER BY d.name;


// 12. Find safe medications for patient with specific disease
MATCH (d:Disease {name: 'Kidney Disease'})<-[c:CONTRAINDICATED_IN]-(unsafe:Medication)
MATCH (d)-[:TREATED_BY]->(safe:Medication)
WHERE NOT (safe)-[:CONTRAINDICATED_IN]->(d)
RETURN d.name AS disease,
       COLLECT(DISTINCT safe.name) AS safe_treatments,
       COLLECT(DISTINCT unsafe.name) AS avoid_medications;
