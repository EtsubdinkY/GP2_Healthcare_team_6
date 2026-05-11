// GP3 MongoDB setup script
// Database: healthcare_management
// Purpose: create clinical document collections with validation and indexes.

const databaseName = "healthcare_management";
db = db.getSiblingDB(databaseName);

print(`Using database: ${databaseName}`);

[
  "clinical_notes",
  "medical_images_metadata",  
  "care_plans",
  "patient_surveys"
].forEach((collectionName) => {
  if (db.getCollectionNames().includes(collectionName)) {
    db[collectionName].drop();
    print(`Dropped existing collection: ${collectionName}`);
  }
});

// -----------------------------------------------------------------------------
// Collection 1: clinical_notes
// Stores variable clinical documentation: progress notes, consultations,
// discharge summaries, and procedure notes. Patient/provider IDs reference GP2
// PostgreSQL tables.
// -----------------------------------------------------------------------------
db.createCollection("clinical_notes", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "provider_id", "encounter_date", "note_type", "signed"],
      properties: {
        patient_id: { bsonType: "int", description: "PostgreSQL patient.patient_id" },
        provider_id: { bsonType: "int", description: "PostgreSQL provider.provider_id" },
        encounter_date: { bsonType: "date" },
        note_type: {
          enum: ["progress_note", "consultation", "discharge_summary", "procedure_note"]
        },
        chief_complaint: { bsonType: ["string", "null"] },
        review_of_systems: { bsonType: ["object", "null"] },
        physical_exam: { bsonType: ["object", "null"] },
        assessment: { bsonType: ["string", "null"] },
        plan: { bsonType: ["string", "null"] },
        icd10_codes: {
          bsonType: ["array", "null"],
          items: { bsonType: "string" }
        },
        signed: { bsonType: "bool" },
        signed_date: { bsonType: ["date", "null"] },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

db.clinical_notes.createIndex({ patient_id: 1, encounter_date: -1 }, { name: "idx_notes_patient_timeline" });
db.clinical_notes.createIndex({ provider_id: 1, note_type: 1, encounter_date: -1 }, { name: "idx_notes_provider_type_date" });
db.clinical_notes.createIndex({ icd10_codes: 1 }, { name: "idx_notes_icd10_codes" });
db.clinical_notes.createIndex(
  { chief_complaint: "text", assessment: "text", plan: "text", findings: "text", recommendations: "text", discharge_diagnosis: "text" },
  { name: "idx_notes_text_search" }
);
db.clinical_notes.createIndex(
  { provider_id: 1, encounter_date: -1 },
  { name: "idx_notes_unsigned_review", partialFilterExpression: { signed: false } }
);

// -----------------------------------------------------------------------------
// Collection 2: medical_images_metadata
// Stores imaging study metadata and radiology reports. DICOM metadata is embedded
// because fields vary by modality and are queried with the parent imaging study.
// -----------------------------------------------------------------------------
db.createCollection("medical_images_metadata", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "study_date", "modality", "body_part", "study_description", "dicom_metadata"],
      properties: {
        patient_id: { bsonType: "int" },
        provider_id: { bsonType: ["int", "null"] },
        study_date: { bsonType: "date" },
        modality: { enum: ["CT", "MRI", "XRAY", "US", "MAMMO"] },
        body_part: { bsonType: "string" },
        study_description: { bsonType: "string" },
        dicom_metadata: { bsonType: "object" },
        radiologist_report: { bsonType: ["object", "null"] },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

db.medical_images_metadata.createIndex({ patient_id: 1, study_date: -1 }, { name: "idx_images_patient_timeline" });
db.medical_images_metadata.createIndex({ modality: 1, body_part: 1, study_date: -1 }, { name: "idx_images_modality_bodypart" });
db.medical_images_metadata.createIndex({ "dicom_metadata.study_uid": 1 }, { name: "uidx_images_study_uid", unique: true });
db.medical_images_metadata.createIndex(
  { "radiologist_report.provider_id": 1, study_date: -1 },
  { name: "idx_images_critical_findings", partialFilterExpression: { "radiologist_report.critical_finding": true } }
);
db.medical_images_metadata.createIndex(
  { study_description: "text", "radiologist_report.findings": "text", "radiologist_report.impression": "text" },
  { name: "idx_images_text_report" }
);

// -----------------------------------------------------------------------------
// Collection 3: care_plans
// Stores nested patient goals, interventions, and monitoring schedules. Goals and
// interventions are embedded because they are bounded and viewed with the plan.
// -----------------------------------------------------------------------------
db.createCollection("care_plans", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "provider_id", "primary_diagnosis", "status", "goals", "interventions", "created_at"],
      properties: {
        patient_id: { bsonType: "int" },
        provider_id: { bsonType: "int" },
        primary_diagnosis: { bsonType: "object" },
        status: { enum: ["active", "completed", "paused", "cancelled"] },
        goals: { bsonType: "array" },
        interventions: { bsonType: "array" },
        review_frequency_days: { bsonType: "int" },
        last_reviewed: { bsonType: ["date", "null"] },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

db.care_plans.createIndex({ patient_id: 1, status: 1, last_reviewed: -1 }, { name: "idx_care_plans_patient_status" });
db.care_plans.createIndex({ provider_id: 1, status: 1 }, { name: "idx_care_plans_provider_status" });
db.care_plans.createIndex({ "primary_diagnosis.icd10": 1 }, { name: "idx_care_plans_icd10" });
db.care_plans.createIndex({ "goals.status": 1 }, { name: "idx_care_plans_goal_status" });
db.care_plans.createIndex(
  { "primary_diagnosis.name": "text", "goals.description": "text", "interventions.description": "text" },
  { name: "idx_care_plans_text" }
);

// -----------------------------------------------------------------------------
// Collection 4: patient_surveys
// Stores variable patient reported outcomes like PHQ-9, GAD-7, pain scales, and
// satisfaction surveys. Responses are embedded because each survey response set is
// bounded and always interpreted with the parent survey.
// -----------------------------------------------------------------------------
db.createCollection("patient_surveys", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "survey_type", "completed_at", "responses", "score"],
      properties: {
        patient_id: { bsonType: "int" },
        survey_type: { enum: ["PHQ-9", "GAD-7", "Pain", "Satisfaction"] },
        completed_at: { bsonType: "date" },
        responses: { bsonType: "array" },
        score: { bsonType: "object" },
        source: { enum: ["portal", "tablet", "phone", "paper"] },
        notes: { bsonType: ["string", "null"] },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

db.patient_surveys.createIndex({ patient_id: 1, survey_type: 1, completed_at: -1 }, { name: "idx_surveys_patient_type_timeline" });
db.patient_surveys.createIndex({ survey_type: 1, "score.severity": 1 }, { name: "idx_surveys_type_severity" });
db.patient_surveys.createIndex({ "responses.question_code": 1 }, { name: "idx_surveys_question_code" });
db.patient_surveys.createIndex({ notes: "text" }, { name: "idx_surveys_notes_text" });

print("MongoDB setup completed: collections, validators, and indexes created.");
