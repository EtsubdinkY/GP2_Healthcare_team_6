// GP3 MongoDB clinical query set
// Run with: mongosh mongodb/mongo_queries.js

const databaseName = "healthcare_management";
db = db.getSiblingDB(databaseName);

// -----------------------------------------------------------------------------
// Query #1: Clinical documentation volume by provider and note type
// Clinical Context: Helps operations leaders identify provider documentation load
// and whether specific note types are creating review bottlenecks.
// Collections Used: clinical_notes
// Pipeline Stages: $group, $sort, $project
// -----------------------------------------------------------------------------
print("\nQuery #1: Clinical documentation volume by provider and note type");
printjson(
  db.clinical_notes.aggregate([
    {
      $group: {
        _id: { provider_id: "$provider_id", note_type: "$note_type" },
        note_count: { $sum: 1 },
        unsigned_count: { $sum: { $cond: [{ $eq: ["$signed", false] }, 1, 0] } },
        most_recent_note: { $max: "$encounter_date" }
      }
    },
    { $sort: { "_id.provider_id": 1, "_id.note_type": 1 } },
    {
      $project: {
        _id: 0,
        provider_id: "$_id.provider_id",
        note_type: "$_id.note_type",
        note_count: 1,
        unsigned_count: 1,
        most_recent_note: 1
      }
    }
  ]).limit(10).toArray()
);

// Expected Output: provider_id, note_type, note_count, unsigned_count, most_recent_note.

// -----------------------------------------------------------------------------
// Query #2: Imaging volume and critical finding rate by modality
// Clinical Context: Shows which modalities produce the most studies and where
// critical findings are concentrated.
// Collections Used: medical_images_metadata
// Pipeline Stages: $group, $project, $sort
// -----------------------------------------------------------------------------
print("\nQuery #2: Imaging volume and critical finding rate by modality");
printjson(
  db.medical_images_metadata.aggregate([
    {
      $group: {
        _id: "$modality",
        study_count: { $sum: 1 },
        critical_findings: {
          $sum: { $cond: [{ $eq: ["$radiologist_report.critical_finding", true] }, 1, 0] }
        },
        avg_image_count: { $avg: "$dicom_metadata.image_count" }
      }
    },
    {
      $project: {
        _id: 0,
        modality: "$_id",
        study_count: 1,
        critical_findings: 1,
        critical_rate: { $round: [{ $divide: ["$critical_findings", "$study_count"] }, 3] },
        avg_image_count: { $round: ["$avg_image_count", 1] }
      }
    },
    { $sort: { critical_rate: -1, study_count: -1 } }
  ]).toArray()
);

// Expected Output: modality-level summary with count, critical rate, and average images.

// -----------------------------------------------------------------------------
// Query #3: Patient survey scoring and monthly trend analysis
// Clinical Context: Tracks patient-reported outcomes such as PHQ-9, GAD-7, pain,
// and satisfaction over time.
// Collections Used: patient_surveys
// Pipeline Stages: $group, $project, $sort
// -----------------------------------------------------------------------------
print("\nQuery #3: Patient survey scoring and monthly trend analysis");
printjson(
  db.patient_surveys.aggregate([
    {
      $group: {
        _id: {
          patient_id: "$patient_id",
          survey_type: "$survey_type",
          month: { $dateToString: { format: "%Y-%m", date: "$completed_at" } }
        },
        avg_score: { $avg: "$score.total" },
        latest_completed_at: { $max: "$completed_at" },
        surveys_completed: { $sum: 1 },
        latest_severity: { $last: "$score.severity" }
      }
    },
    {
      $project: {
        _id: 0,
        patient_id: "$_id.patient_id",
        survey_type: "$_id.survey_type",
        month: "$_id.month",
        avg_score: { $round: ["$avg_score", 1] },
        surveys_completed: 1,
        latest_severity: 1,
        latest_completed_at: 1
      }
    },
    { $sort: { patient_id: 1, survey_type: 1, month: 1 } }
  ]).limit(12).toArray()
);

// Expected Output: patient/month survey score summaries for trending.

// -----------------------------------------------------------------------------
// Query #4: Full-text search across clinical narratives
// Clinical Context: Allows clinicians to search all note types for symptoms,
// diagnoses, or plan language without forcing a fixed SQL schema.
// Collections Used: clinical_notes
// Pipeline Stages: $match with $text, $project, $sort, $limit
// -----------------------------------------------------------------------------
print("\nQuery #4: Text search for hypertension and chest pain");
printjson(
  db.clinical_notes.find(
    { $text: { $search: "hypertension chest pain" } },
    {
      score: { $meta: "textScore" },
      patient_id: 1,
      provider_id: 1,
      encounter_date: 1,
      note_type: 1,
      chief_complaint: 1,
      assessment: 1,
      plan: 1,
      findings: 1
    }
  )
  .sort({ score: { $meta: "textScore" }, encounter_date: -1 })
  .limit(5)
  .toArray()
);

// Expected Output: highest relevance notes matching the searched clinical terms.

// -----------------------------------------------------------------------------
// Query #5: Care plan progress tracking using goals array unwind
// Clinical Context: Identifies care-plan goals that are on track, in progress, or
// at risk, supporting care management workflows.
// Collections Used: care_plans
// Pipeline Stages: $match, $unwind, $group, $project, $sort
// -----------------------------------------------------------------------------
print("\nQuery #5: Care plan progress tracking using $unwind on goals");
printjson(
  db.care_plans.aggregate([
    { $match: { status: "active" } },
    { $unwind: "$goals" },
    {
      $group: {
        _id: { goal_status: "$goals.status", diagnosis: "$primary_diagnosis.name" },
        goal_count: { $sum: 1 },
        avg_progress_percent: { $avg: "$goals.progress_percent" },
        patients: { $addToSet: "$patient_id" }
      }
    },
    {
      $project: {
        _id: 0,
        diagnosis: "$_id.diagnosis",
        goal_status: "$_id.goal_status",
        goal_count: 1,
        avg_progress_percent: { $round: ["$avg_progress_percent", 1] },
        patient_count: { $size: "$patients" }
      }
    },
    { $sort: { goal_status: 1, diagnosis: 1 } }
  ]).limit(12).toArray()
);

// Expected Output: goal counts and average progress by diagnosis and goal status.

// -----------------------------------------------------------------------------
// Query #6: Find clinical notes containing a specific ICD-10 code using $elemMatch
// Clinical Context: Helps clinicians and analysts find documentation tied to a
// diagnosis code such as hypertension (I10) or diabetes (E11.9).
// Collections Used: clinical_notes
// Pipeline Stages: find with $elemMatch, projection, sort, limit
// -----------------------------------------------------------------------------
print("\nQuery #6: Notes with ICD-10 code I10 using $elemMatch");
printjson(
  db.clinical_notes.find(
    { icd10_codes: { $elemMatch: { $eq: "I10" } } },
    {
      patient_id: 1,
      provider_id: 1,
      encounter_date: 1,
      note_type: 1,
      icd10_codes: 1,
      assessment: 1,
      discharge_diagnosis: 1,
      reason_for_consultation: 1
    }
  )
  .sort({ encounter_date: -1 })
  .limit(8)
  .toArray()
);


