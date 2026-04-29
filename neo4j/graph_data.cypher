// Neo4j Graph Data for Healthcare System
// Sample data for drug interactions, allergies, and provider networks

// Drug Classes
CREATE (dc1:DrugClass {name: 'Statin', description: 'Cholesterol medications'})
CREATE (dc2:DrugClass {name: 'ACE Inhibitor', description: 'Blood pressure medications'})
CREATE (dc3:DrugClass {name: 'Biguanide', description: 'Diabetes medications'})
CREATE (dc4:DrugClass {name: 'Antibiotic', description: 'Antimicrobial agents'})
CREATE (dc5:DrugClass {name: 'Opioid Analgesic', description: 'Pain relievers'})
CREATE (dc6:DrugClass {name: 'Bronchodilator', description: 'Respiratory medications'})
CREATE (dc7:DrugClass {name: 'Corticosteroid', description: 'Anti-inflammatory steroids'})
CREATE (dc8:DrugClass {name: 'SSRI', description: 'Antidepressants'})
CREATE (dc9:DrugClass {name: 'Hormone', description: 'Hormone therapies'})
CREATE (dc10:DrugClass {name: 'Calcium Channel Blocker', description: 'Heart medications'})
CREATE (dc11:DrugClass {name: 'Neuropathic Pain', description: 'Nerve pain medications'})
CREATE (dc12:DrugClass {name: 'Benzodiazepine', description: 'Anti-anxiety medications'})
CREATE (dc13:DrugClass {name: 'Stimulant', description: 'ADHD medications'})
CREATE (dc14:DrugClass {name: 'Antidiabetic', description: 'Insulin medications'})
CREATE (dc15:DrugClass {name: 'PPI', description: 'Acid reflux medications'})
CREATE (dc16:DrugClass {name: 'ARB', description: 'Blood pressure medications'})
CREATE (dc17:DrugClass {name: 'Diuretic', description: 'Water pills'})
CREATE (dc18:DrugClass {name: 'Muscle Relaxant', description: 'Muscle relaxers'})
CREATE (dc19:DrugClass {name: 'Sedative', description: 'Sleep aids'})
CREATE (dc20:DrugClass {name: 'Antidepressant', description: 'Mood medications'})
CREATE (dc21:DrugClass {name: 'Alpha Blocker', description: 'Prostate medications'})
CREATE (dc22:DrugClass {name: 'Anticoagulant', description: 'Blood thinners'})
CREATE (dc23:DrugClass {name: 'Analgesic', description: 'Pain relievers'})
CREATE (dc24:DrugClass {name: 'NSAID', description: 'Anti-inflammatory drugs'})
CREATE (dc25:DrugClass {name: 'Leukotriene Modifier', description: 'Asthma medications'});

// Medications (matching PostgreSQL med_id 1-35)
CREATE (m1:Medication {med_id: 1, name: 'Lipitor', generic_name: 'Atorvastatin', form: 'Tablet', is_controlled: false})
CREATE (m2:Medication {med_id: 2, name: 'Lisinopril', generic_name: 'Lisinopril', form: 'Tablet', is_controlled: false})
CREATE (m3:Medication {med_id: 3, name: 'Metformin', generic_name: 'Metformin', form: 'Tablet', is_controlled: false})
CREATE (m4:Medication {med_id: 4, name: 'Amoxicillin', generic_name: 'Amoxicillin', form: 'Capsule', is_controlled: false})
CREATE (m5:Medication {med_id: 5, name: 'Oxycodone', generic_name: 'Oxycodone', form: 'Tablet', is_controlled: true, schedule: 'Schedule II'})
CREATE (m6:Medication {med_id: 6, name: 'Albuterol Inhaler', generic_name: 'Albuterol', form: 'Inhaler', is_controlled: false})
CREATE (m7:Medication {med_id: 7, name: 'Hydrocortisone Cream', generic_name: 'Hydrocortisone', form: 'Cream', is_controlled: false})
CREATE (m8:Medication {med_id: 8, name: 'Sertraline', generic_name: 'Sertraline', form: 'Tablet', is_controlled: false})
CREATE (m9:Medication {med_id: 9, name: 'Levothyroxine', generic_name: 'Levothyroxine', form: 'Tablet', is_controlled: false})
CREATE (m10:Medication {med_id: 10, name: 'Amlodipine', generic_name: 'Amlodipine', form: 'Tablet', is_controlled: false})
CREATE (m11:Medication {med_id: 11, name: 'Gabapentin', generic_name: 'Gabapentin', form: 'Capsule', is_controlled: false})
CREATE (m12:Medication {med_id: 12, name: 'Tramadol', generic_name: 'Tramadol', form: 'Tablet', is_controlled: true, schedule: 'Schedule IV'})
CREATE (m13:Medication {med_id: 13, name: 'Clonazepam', generic_name: 'Clonazepam', form: 'Tablet', is_controlled: true, schedule: 'Schedule IV'})
CREATE (m14:Medication {med_id: 14, name: 'Adderall XR', generic_name: 'Amphetamine/Dextroamphetamine', form: 'Capsule', is_controlled: true, schedule: 'Schedule II'})
CREATE (m15:Medication {med_id: 15, name: 'Insulin Glargine', generic_name: 'Insulin Glargine', form: 'Injection', is_controlled: false})
CREATE (m16:Medication {med_id: 16, name: 'Omeprazole', generic_name: 'Omeprazole', form: 'Capsule', is_controlled: false})
CREATE (m17:Medication {med_id: 17, name: 'Losartan', generic_name: 'Losartan', form: 'Tablet', is_controlled: false})
CREATE (m18:Medication {med_id: 18, name: 'Prednisone', generic_name: 'Prednisone', form: 'Tablet', is_controlled: false})
CREATE (m19:Medication {med_id: 19, name: 'Azithromycin', generic_name: 'Azithromycin', form: 'Tablet', is_controlled: false})
CREATE (m20:Medication {med_id: 20, name: 'Furosemide', generic_name: 'Furosemide', form: 'Tablet', is_controlled: false})
CREATE (m21:Medication {med_id: 21, name: 'Cyclobenzaprine', generic_name: 'Cyclobenzaprine', form: 'Tablet', is_controlled: false})
CREATE (m22:Medication {med_id: 22, name: 'Hydrocodone-Acetaminophen', generic_name: 'Hydrocodone/APAP', form: 'Tablet', is_controlled: true, schedule: 'Schedule II'})
CREATE (m23:Medication {med_id: 23, name: 'Zolpidem', generic_name: 'Zolpidem', form: 'Tablet', is_controlled: true, schedule: 'Schedule IV'})
CREATE (m24:Medication {med_id: 24, name: 'Lorazepam', generic_name: 'Lorazepam', form: 'Tablet', is_controlled: true, schedule: 'Schedule IV'})
CREATE (m25:Medication {med_id: 25, name: 'Codeine Syrup', generic_name: 'Codeine/Guaifenesin', form: 'Syrup', is_controlled: true, schedule: 'Schedule V'})
CREATE (m26:Medication {med_id: 26, name: 'Methylphenidate', generic_name: 'Methylphenidate', form: 'Tablet', is_controlled: true, schedule: 'Schedule II'})
CREATE (m27:Medication {med_id: 27, name: 'Bupropion', generic_name: 'Bupropion', form: 'Tablet', is_controlled: false})
CREATE (m28:Medication {med_id: 28, name: 'Tamsulosin', generic_name: 'Tamsulosin', form: 'Capsule', is_controlled: false})
CREATE (m29:Medication {med_id: 29, name: 'Doxycycline', generic_name: 'Doxycycline', form: 'Capsule', is_controlled: false})
CREATE (m30:Medication {med_id: 30, name: 'Warfarin', generic_name: 'Warfarin', form: 'Tablet', is_controlled: false})
CREATE (m31:Medication {med_id: 31, name: 'Escitalopram', generic_name: 'Escitalopram', form: 'Tablet', is_controlled: false})
CREATE (m32:Medication {med_id: 32, name: 'Acetaminophen', generic_name: 'Acetaminophen', form: 'Tablet', is_controlled: false})
CREATE (m33:Medication {med_id: 33, name: 'Naproxen', generic_name: 'Naproxen', form: 'Tablet', is_controlled: false})
CREATE (m34:Medication {med_id: 34, name: 'Montelukast', generic_name: 'Montelukast', form: 'Tablet', is_controlled: false})
CREATE (m35:Medication {med_id: 35, name: 'Insulin Lispro', generic_name: 'Insulin Lispro', form: 'Injection', is_controlled: false});

// Allergens
CREATE (a1:Allergen {name: 'Penicillin', category: 'Drug'})
CREATE (a2:Allergen {name: 'Peanuts', category: 'Food'})
CREATE (a3:Allergen {name: 'Latex', category: 'Environmental'})
CREATE (a4:Allergen {name: 'Shellfish', category: 'Food'})
CREATE (a5:Allergen {name: 'Pollen', category: 'Environmental'})
CREATE (a6:Allergen {name: 'Ibuprofen', category: 'Drug'})
CREATE (a7:Allergen {name: 'Dust', category: 'Environmental'})
CREATE (a8:Allergen {name: 'Soy', category: 'Food'})
CREATE (a9:Allergen {name: 'Eggs', category: 'Food'})
CREATE (a10:Allergen {name: 'Bee stings', category: 'Insect'})
CREATE (a11:Allergen {name: 'Sulfa', category: 'Drug'})
CREATE (a12:Allergen {name: 'Codeine', category: 'Drug'});

// Link medications to drug classes
MATCH (m:Medication {med_id: 1}), (dc:DrugClass {name: 'Statin'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 2}), (dc:DrugClass {name: 'ACE Inhibitor'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 3}), (dc:DrugClass {name: 'Biguanide'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 4}), (dc:DrugClass {name: 'Antibiotic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 5}), (dc:DrugClass {name: 'Opioid Analgesic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 6}), (dc:DrugClass {name: 'Bronchodilator'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 7}), (dc:DrugClass {name: 'Corticosteroid'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 8}), (dc:DrugClass {name: 'SSRI'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 9}), (dc:DrugClass {name: 'Hormone'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 10}), (dc:DrugClass {name: 'Calcium Channel Blocker'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 11}), (dc:DrugClass {name: 'Neuropathic Pain'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 12}), (dc:DrugClass {name: 'Opioid Analgesic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 13}), (dc:DrugClass {name: 'Benzodiazepine'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 14}), (dc:DrugClass {name: 'Stimulant'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 15}), (dc:DrugClass {name: 'Antidiabetic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 16}), (dc:DrugClass {name: 'PPI'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 17}), (dc:DrugClass {name: 'ARB'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 18}), (dc:DrugClass {name: 'Corticosteroid'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 19}), (dc:DrugClass {name: 'Antibiotic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 20}), (dc:DrugClass {name: 'Diuretic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 21}), (dc:DrugClass {name: 'Muscle Relaxant'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 22}), (dc:DrugClass {name: 'Opioid Analgesic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 23}), (dc:DrugClass {name: 'Sedative'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 24}), (dc:DrugClass {name: 'Benzodiazepine'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 25}), (dc:DrugClass {name: 'Opioid Analgesic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 26}), (dc:DrugClass {name: 'Stimulant'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 27}), (dc:DrugClass {name: 'Antidepressant'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 28}), (dc:DrugClass {name: 'Alpha Blocker'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 29}), (dc:DrugClass {name: 'Antibiotic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 30}), (dc:DrugClass {name: 'Anticoagulant'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 31}), (dc:DrugClass {name: 'SSRI'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 32}), (dc:DrugClass {name: 'Analgesic'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 33}), (dc:DrugClass {name: 'NSAID'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 34}), (dc:DrugClass {name: 'Leukotriene Modifier'}) CREATE (m)-[:BELONGS_TO]->(dc);
MATCH (m:Medication {med_id: 35}), (dc:DrugClass {name: 'Antidiabetic'}) CREATE (m)-[:BELONGS_TO]->(dc);

// Drug-drug interactions
// Opioid + Benzodiazepine (dangerous combination)
MATCH (m1:Medication {name: 'Oxycodone'}), (m2:Medication {name: 'Lorazepam'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'contraindicated', description: 'Risk of respiratory depression'}]->(m2);

MATCH (m1:Medication {name: 'Oxycodone'}), (m2:Medication {name: 'Clonazepam'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'contraindicated', description: 'Risk of respiratory depression'}]->(m2);

MATCH (m1:Medication {name: 'Hydrocodone-Acetaminophen'}), (m2:Medication {name: 'Lorazepam'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'contraindicated', description: 'Risk of respiratory depression'}]->(m2);

MATCH (m1:Medication {name: 'Tramadol'}), (m2:Medication {name: 'Clonazepam'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Increased sedation risk'}]->(m2);

// Warfarin interactions
MATCH (m1:Medication {name: 'Warfarin'}), (m2:Medication {name: 'Naproxen'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Increased bleeding risk'}]->(m2);

// SSRI + Tramadol (serotonin syndrome)
MATCH (m1:Medication {name: 'Sertraline'}), (m2:Medication {name: 'Tramadol'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Serotonin syndrome risk'}]->(m2);

MATCH (m1:Medication {name: 'Escitalopram'}), (m2:Medication {name: 'Tramadol'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Serotonin syndrome risk'}]->(m2);

// ACE + ARB
MATCH (m1:Medication {name: 'Lisinopril'}), (m2:Medication {name: 'Losartan'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Hyperkalemia risk'}]->(m2);

// Gabapentin + Opioids
MATCH (m1:Medication {name: 'Gabapentin'}), (m2:Medication {name: 'Oxycodone'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Respiratory depression risk'}]->(m2);

// Bupropion + Tramadol
MATCH (m1:Medication {name: 'Bupropion'}), (m2:Medication {name: 'Tramadol'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'major', description: 'Seizure risk'}]->(m2);

// Moderate interactions
MATCH (m1:Medication {name: 'Amlodipine'}), (m2:Medication {name: 'Lipitor'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'moderate', description: 'Increased statin levels'}]->(m2);

MATCH (m1:Medication {name: 'Levothyroxine'}), (m2:Medication {name: 'Omeprazole'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'moderate', description: 'Reduced absorption'}]->(m2);

MATCH (m1:Medication {name: 'Prednisone'}), (m2:Medication {name: 'Naproxen'})
CREATE (m1)-[:INTERACTS_WITH {severity: 'moderate', description: 'GI bleeding risk'}]->(m2);

// Allergy contraindications
MATCH (a:Allergen {name: 'Penicillin'}), (m:Medication {name: 'Amoxicillin'})
CREATE (m)-[:CONTRAINDICATED_FOR {reason: 'Penicillin-class antibiotic'}]->(a);

MATCH (a:Allergen {name: 'Ibuprofen'}), (m:Medication {name: 'Naproxen'})
CREATE (m)-[:CONTRAINDICATED_FOR {reason: 'NSAID cross-reactivity'}]->(a);

MATCH (a:Allergen {name: 'Codeine'}), (m:Medication {name: 'Codeine Syrup'})
CREATE (m)-[:CONTRAINDICATED_FOR {reason: 'Contains codeine'}]->(a);

MATCH (a:Allergen {name: 'Codeine'}), (m:Medication {name: 'Hydrocodone-Acetaminophen'})
CREATE (m)-[:CONTRAINDICATED_FOR {reason: 'Opioid cross-reactivity'}]->(a);

MATCH (a:Allergen {name: 'Sulfa'}), (m:Medication {name: 'Furosemide'})
CREATE (m)-[:CONTRAINDICATED_FOR {reason: 'Sulfonamide structure'}]->(a);

// Hospitals
CREATE (h1:Hospital {hospital_id: 1, name: 'New York General Hospital', facility_type: 'Hospital', city: 'New York', state: 'NY'})
CREATE (h2:Hospital {hospital_id: 2, name: 'Los Angeles Medical Center', facility_type: 'Hospital', city: 'Los Angeles', state: 'CA'})
CREATE (h3:Hospital {hospital_id: 3, name: 'Chicago Central Hospital', facility_type: 'Hospital', city: 'Chicago', state: 'IL'})
CREATE (h4:Hospital {hospital_id: 4, name: 'Houston Care Hospital', facility_type: 'Hospital', city: 'Houston', state: 'TX'})
CREATE (h5:Hospital {hospital_id: 5, name: 'Miami Wellness Hospital', facility_type: 'Hospital', city: 'Miami', state: 'FL'});

// Departments
CREATE (d1:Department {dept_id: 1, name: 'Cardiology', hospital_id: 1})
CREATE (d2:Department {dept_id: 2, name: 'Emergency Medicine', hospital_id: 1})
CREATE (d3:Department {dept_id: 3, name: 'Neurology', hospital_id: 2})
CREATE (d4:Department {dept_id: 4, name: 'Family Medicine', hospital_id: 2})
CREATE (d5:Department {dept_id: 5, name: 'Orthopedics', hospital_id: 3})
CREATE (d6:Department {dept_id: 6, name: 'Internal Medicine', hospital_id: 3})
CREATE (d7:Department {dept_id: 7, name: 'Pediatrics', hospital_id: 4})
CREATE (d8:Department {dept_id: 8, name: 'Radiology', hospital_id: 4})
CREATE (d9:Department {dept_id: 9, name: 'Oncology', hospital_id: 5});

// Department -> Hospital links
MATCH (d:Department {dept_id: 1}), (h:Hospital {hospital_id: 1}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 2}), (h:Hospital {hospital_id: 1}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 3}), (h:Hospital {hospital_id: 2}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 4}), (h:Hospital {hospital_id: 2}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 5}), (h:Hospital {hospital_id: 3}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 6}), (h:Hospital {hospital_id: 3}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 7}), (h:Hospital {hospital_id: 4}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 8}), (h:Hospital {hospital_id: 4}) CREATE (d)-[:PART_OF]->(h);
MATCH (d:Department {dept_id: 9}), (h:Hospital {hospital_id: 5}) CREATE (d)-[:PART_OF]->(h);

// Providers
CREATE (pr1:Provider {provider_id: 1, npi: '1000000001', first_name: 'Kelly', last_name: 'Mbenga', specialty: 'Cardiologist'})
CREATE (pr2:Provider {provider_id: 2, npi: '1000000002', first_name: 'John', last_name: 'Johnson', specialty: 'Emergency Physician'})
CREATE (pr3:Provider {provider_id: 3, npi: '1000000003', first_name: 'Robert', last_name: 'Williams', specialty: 'Neurologist'})
CREATE (pr4:Provider {provider_id: 4, npi: '1000000004', first_name: 'Michael', last_name: 'Brown', specialty: 'Family Physician'})
CREATE (pr5:Provider {provider_id: 5, npi: '1000000005', first_name: 'William', last_name: 'Jones', specialty: 'Orthopedic Surgeon'})
CREATE (pr6:Provider {provider_id: 6, npi: '1000000006', first_name: 'David', last_name: 'Garcia', specialty: 'Internist'})
CREATE (pr7:Provider {provider_id: 7, npi: '1000000007', first_name: 'Richard', last_name: 'Miller', specialty: 'Pediatrician'})
CREATE (pr8:Provider {provider_id: 8, npi: '1000000008', first_name: 'Joseph', last_name: 'Davis', specialty: 'Registered Nurse'})
CREATE (pr9:Provider {provider_id: 9, npi: '1000000009', first_name: 'Thomas', last_name: 'Rodriguez', specialty: 'Oncologist'});

// Provider -> Department links
MATCH (pr:Provider {provider_id: 1}), (d:Department {dept_id: 1}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 2}), (d:Department {dept_id: 2}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 3}), (d:Department {dept_id: 3}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 4}), (d:Department {dept_id: 4}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 5}), (d:Department {dept_id: 5}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 6}), (d:Department {dept_id: 6}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 7}), (d:Department {dept_id: 7}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 8}), (d:Department {dept_id: 8}) CREATE (pr)-[:WORKS_IN]->(d);
MATCH (pr:Provider {provider_id: 9}), (d:Department {dept_id: 9}) CREATE (pr)-[:WORKS_IN]->(d);

// Provider referral network
MATCH (pr1:Provider {specialty: 'Family Physician'}), (pr2:Provider {specialty: 'Cardiologist'})
CREATE (pr1)-[:REFERS_TO {referral_count: 45, common_reasons: ['chest pain', 'hypertension']}]->(pr2);

MATCH (pr1:Provider {specialty: 'Family Physician'}), (pr2:Provider {specialty: 'Neurologist'})
CREATE (pr1)-[:REFERS_TO {referral_count: 28, common_reasons: ['headaches', 'numbness']}]->(pr2);

MATCH (pr1:Provider {specialty: 'Family Physician'}), (pr2:Provider {specialty: 'Orthopedic Surgeon'})
CREATE (pr1)-[:REFERS_TO {referral_count: 35, common_reasons: ['joint pain', 'back pain']}]->(pr2);

MATCH (pr1:Provider {specialty: 'Emergency Physician'}), (pr2:Provider {specialty: 'Cardiologist'})
CREATE (pr1)-[:REFERS_TO {referral_count: 67, common_reasons: ['chest pain', 'heart attack']}]->(pr2);

MATCH (pr1:Provider {specialty: 'Internist'}), (pr2:Provider {specialty: 'Oncologist'})
CREATE (pr1)-[:REFERS_TO {referral_count: 18, common_reasons: ['abnormal labs', 'mass found']}]->(pr2);

// Patients (subset matching PostgreSQL)
CREATE (p1:Patient {patient_id: 1, mrn: '0000000001', first_name: 'James', last_name: 'Smith'})
CREATE (p2:Patient {patient_id: 2, mrn: '0000000002', first_name: 'Patricia', last_name: 'Brown'})
CREATE (p3:Patient {patient_id: 3, mrn: '0000000003', first_name: 'Robert', last_name: 'Miller'})
CREATE (p4:Patient {patient_id: 4, mrn: '0000000004', first_name: 'Linda', last_name: 'Martinez'})
CREATE (p5:Patient {patient_id: 5, mrn: '0000000005', first_name: 'William', last_name: 'Gonzalez'})
CREATE (p6:Patient {patient_id: 6, mrn: '0000000006', first_name: 'Barbara', last_name: 'Thomas'})
CREATE (p7:Patient {patient_id: 7, mrn: '0000000007', first_name: 'Richard', last_name: 'Jackson'})
CREATE (p8:Patient {patient_id: 8, mrn: '0000000008', first_name: 'Jessica', last_name: 'Perez'})
CREATE (p9:Patient {patient_id: 9, mrn: '0000000009', first_name: 'Thomas', last_name: 'Harris'})
CREATE (p10:Patient {patient_id: 10, mrn: '0000000010', first_name: 'Karen', last_name: 'Ramirez'});

// Patient allergies
MATCH (p:Patient {patient_id: 1}), (a:Allergen {name: 'Penicillin'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Low', reaction: 'Rash'}]->(a);

MATCH (p:Patient {patient_id: 2}), (a:Allergen {name: 'Peanuts'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Moderate', reaction: 'Swelling'}]->(a);

MATCH (p:Patient {patient_id: 3}), (a:Allergen {name: 'Latex'})
CREATE (p)-[:ALLERGIC_TO {severity: 'High', reaction: 'Hives'}]->(a);

MATCH (p:Patient {patient_id: 4}), (a:Allergen {name: 'Shellfish'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Critical', reaction: 'Sneezing'}]->(a);

MATCH (p:Patient {patient_id: 5}), (a:Allergen {name: 'Pollen'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Low', reaction: 'Stomach pain'}]->(a);

MATCH (p:Patient {patient_id: 6}), (a:Allergen {name: 'Ibuprofen'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Moderate', reaction: 'Anaphylaxis'}]->(a);

MATCH (p:Patient {patient_id: 7}), (a:Allergen {name: 'Dust'})
CREATE (p)-[:ALLERGIC_TO {severity: 'High', reaction: 'Skin irritation'}]->(a);

MATCH (p:Patient {patient_id: 8}), (a:Allergen {name: 'Soy'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Critical', reaction: 'Rash'}]->(a);

MATCH (p:Patient {patient_id: 9}), (a:Allergen {name: 'Eggs'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Low', reaction: 'Swelling'}]->(a);

MATCH (p:Patient {patient_id: 10}), (a:Allergen {name: 'Bee stings'})
CREATE (p)-[:ALLERGIC_TO {severity: 'Moderate', reaction: 'Hives'}]->(a);

// Patient-provider relationships
MATCH (p:Patient {patient_id: 1}), (pr:Provider {provider_id: 1})
CREATE (p)-[:TREATED_BY]->(pr);

MATCH (p:Patient {patient_id: 2}), (pr:Provider {provider_id: 4})
CREATE (p)-[:TREATED_BY]->(pr);

MATCH (p:Patient {patient_id: 3}), (pr:Provider {provider_id: 3})
CREATE (p)-[:TREATED_BY]->(pr);

MATCH (p:Patient {patient_id: 4}), (pr:Provider {provider_id: 4})
CREATE (p)-[:TREATED_BY]->(pr);

MATCH (p:Patient {patient_id: 5}), (pr:Provider {provider_id: 5})
CREATE (p)-[:TREATED_BY]->(pr);
