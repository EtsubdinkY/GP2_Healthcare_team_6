// GP3 MongoDB seed data
// Creates 200+ clinical notes, 100+ imaging metadata records, plus care plans
// and patient surveys for the healthcare_management database.
const databaseName = "healthcare_management";
db = db.getSiblingDB(databaseName);

print(`Seeding MongoDB database: ${databaseName}`);

const now = new Date();
const patientCount = 80;
const providerCount = 12;

const diagnoses = [
  { name: "Hypertension", icd10: "I10", category: "Cardiovascular" },
  { name: "Type 2 Diabetes Mellitus", icd10: "E11.9", category: "Endocrine" },
  { name: "Asthma", icd10: "J45.909", category: "Respiratory" },
  { name: "Chronic Kidney Disease", icd10: "N18.9", category: "Renal" },
  { name: "Major Depressive Disorder", icd10: "F32.9", category: "Behavioral Health" },
  { name: "Osteoarthritis", icd10: "M19.90", category: "Musculoskeletal" },
  { name: "Migraine", icd10: "G43.909", category: "Neurology" },
  { name: "Pneumonia", icd10: "J18.9", category: "Respiratory" }
];

const noteTypes = ["progress_note", "consultation", "discharge_summary", "procedure_note"];
const modalities = ["CT", "MRI", "XRAY", "US", "MAMMO"];
const bodyParts = ["chest", "head", "abdomen", "knee", "spine", "pelvis", "breast", "shoulder"];
const surveyTypes = ["PHQ-9", "GAD-7", "Pain", "Satisfaction"];

function patientId(i) { return (i % patientCount) + 1; }
function providerId(i) { return (i % providerCount) + 1; }
function makeDate(i, monthOffset = 0) {
  return new Date(Date.UTC(2026, (i + monthOffset) % 12, (i % 28) + 1, 14, 30, 0));
}
function pick(array, i) { return array[i % array.length]; }
function severityFromScore(type, total) {
  if (type === "PHQ-9") {
    if (total >= 20) return "severe";
    if (total >= 15) return "moderately severe";
    if (total >= 10) return "moderate";
    if (total >= 5) return "mild";
    return "minimal";
  }
  if (type === "GAD-7") {
    if (total >= 15) return "severe";
    if (total >= 10) return "moderate";
    if (total >= 5) return "mild";
    return "minimal";
  }
  if (type === "Pain") {
    if (total >= 7) return "severe";
    if (total >= 4) return "moderate";
    return "mild";
  }
  return total >= 80 ? "high" : total >= 60 ? "acceptable" : "needs_follow_up";
}

// -----------------------------------------------------------------------------
// clinical_notes: 240 documents across multiple note types.
// -----------------------------------------------------------------------------
const clinicalNotes = [];

for (let i = 0; i < 240; i++) {
  const diagnosis = pick(diagnoses, i);
  const type = pick(noteTypes, i);
  const base = {
    patient_id: patientId(i),
    provider_id: providerId(i + 3),
    encounter_date: makeDate(i),
    note_type: type,
    icd10_codes: [diagnosis.icd10],
    signed: i % 11 !== 0,
    signed_date: i % 11 !== 0 ? makeDate(i, 1) : null,
    created_at: now,
    updated_at: now
  };

  if (type === "progress_note") {
    clinicalNotes.push({
      ...base,
      chief_complaint: `Follow-up for ${diagnosis.name.toLowerCase()} management`,
      review_of_systems: {
        cardiovascular: i % 3 === 0 ? "Reports intermittent chest discomfort" : "No chest pain or palpitations",
        respiratory: i % 5 === 0 ? "Mild shortness of breath with exertion" : "No shortness of breath",
        constitutional: "No fever or chills"
      },
      physical_exam: {
        vitals: {
          bp_systolic: 118 + (i % 35),
          bp_diastolic: 72 + (i % 18),
          heart_rate: 62 + (i % 35),
          temperature: 98.1 + ((i % 8) / 10)
        },
        findings: `${diagnosis.category} follow-up exam stable without acute distress.`
      },
      assessment: `${diagnosis.name} - ${i % 4 === 0 ? "suboptimal control" : "stable on current regimen"}`,
      plan: i % 4 === 0
        ? "Adjust medication dose, reinforce diet and exercise, recheck in 4 weeks."
        : "Continue current care plan and follow up in 3 months."
    });
  } else if (type === "consultation") {
    clinicalNotes.push({
      ...base,
      requesting_provider_id: providerId(i + 7),
      reason_for_consultation: `Specialty evaluation for ${diagnosis.name.toLowerCase()}`,
      findings: `${diagnosis.name} reviewed with labs, medications, and prior imaging. No immediate emergency findings documented.`,
      recommendations: i % 2 === 0
        ? "Recommend medication optimization and repeat diagnostic testing."
        : "Recommend conservative management and close outpatient follow-up.",
      urgency: i % 10 === 0 ? "urgent" : "routine"
    });
  } else if (type === "discharge_summary") {
    clinicalNotes.push({
      ...base,
      admission_date: makeDate(i, -1),
      discharge_date: makeDate(i),
      discharge_diagnosis: diagnosis.name,
      hospital_course: `Patient admitted for management of ${diagnosis.name.toLowerCase()}. Condition improved with treatment and monitoring.`,
      discharge_medications: ["Lisinopril", "Metformin", "Atorvastatin"].slice(0, (i % 3) + 1),
      follow_up: "Primary care follow-up in 7-14 days; return to ER for worsening symptoms."
    });
  } else {
    clinicalNotes.push({
      ...base,
      procedure_name: pick(["Joint injection", "Skin biopsy", "Wound debridement", "Stress test", "Pulmonary function test"], i),
      indication: `Evaluate or treat symptoms related to ${diagnosis.name.toLowerCase()}`,
      anesthesia: i % 3 === 0 ? "Local anesthesia" : "None",
      findings: "Procedure completed without immediate complications.",
      complications: i % 17 === 0 ? "Minor bleeding controlled with pressure" : "None"
    });
  }
}

db.clinical_notes.insertMany(clinicalNotes, { ordered: false });

// -----------------------------------------------------------------------------
// medical_images_metadata: 120 documents with modality-specific DICOM fields.
// -----------------------------------------------------------------------------
const imagingRecords = [];
for (let i = 0; i < 120; i++) {
  const modality = pick(modalities, i);
  const bodyPart = pick(bodyParts, i + 2);
  const critical = i % 23 === 0;
  const metadata = {
    study_uid: `1.2.840.113619.6.${100000 + i}`,
    accession_number: `IMG-${String(i + 1).padStart(5, "0")}`,
    series_count: 1 + (i % 5),
    image_count: modality === "CT" || modality === "MRI" ? 80 + (i % 220) : 2 + (i % 10)
  };

  if (modality === "CT") metadata.slice_thickness = 1.25;
  if (modality === "MRI") metadata.sequence = pick(["T1", "T2", "FLAIR", "DWI"], i);
  if (modality === "XRAY") metadata.views = pick(["AP", "PA/Lateral", "Oblique"], i);
  if (modality === "US") metadata.transducer_frequency_mhz = 5 + (i % 8);
  if (modality === "MAMMO") metadata.birads = pick([1, 2, 3, 4], i);

  imagingRecords.push({
    patient_id: patientId(i + 5),
    provider_id: providerId(i + 1),
    study_date: makeDate(i, 2),
    modality,
    body_part: bodyPart,
    study_description: `${modality} ${bodyPart} study for clinical evaluation`,
    dicom_metadata: metadata,
    radiologist_report: {
      provider_id: providerId(i + 8),
      findings: critical
        ? `Critical finding identified in ${bodyPart}; ordering provider notified.`
        : `No acute abnormality identified in ${bodyPart}.`,
      impression: critical ? "Critical abnormal finding requiring follow-up" : `No acute ${bodyPart} process`,
      critical_finding: critical,
      signed_date: makeDate(i, 2)
    },
    created_at: now,
    updated_at: now
  });
}

db.medical_images_metadata.insertMany(imagingRecords, { ordered: false });

// -----------------------------------------------------------------------------
// care_plans: 80 active/completed plans with nested goals and interventions.
// -----------------------------------------------------------------------------
const carePlans = [];
for (let i = 0; i < 80; i++) {
  const diagnosis = pick(diagnoses, i + 1);
  carePlans.push({
    patient_id: patientId(i),
    provider_id: providerId(i + 2),
    primary_diagnosis: diagnosis,
    status: i % 9 === 0 ? "completed" : i % 13 === 0 ? "paused" : "active",
    goals: [
      {
        goal_id: `G-${i + 1}-1`,
        description: `Improve control of ${diagnosis.name.toLowerCase()}`,
        target_date: makeDate(i, 4),
        status: i % 3 === 0 ? "in_progress" : "on_track",
        progress_percent: 35 + (i % 60)
      },
      {
        goal_id: `G-${i + 1}-2`,
        description: "Improve medication adherence and follow-up attendance",
        target_date: makeDate(i, 5),
        status: i % 5 === 0 ? "at_risk" : "on_track",
        progress_percent: 45 + (i % 50)
      }
    ],
    interventions: [
      {
        intervention_id: `I-${i + 1}-1`,
        description: "Medication reconciliation and adherence counseling",
        owner_role: "nurse",
        frequency: "monthly"
      },
      {
        intervention_id: `I-${i + 1}-2`,
        description: "Lifestyle education and symptom monitoring",
        owner_role: "provider",
        frequency: "quarterly"
      }
    ],
    review_frequency_days: 30 + (i % 3) * 30,
    last_reviewed: makeDate(i, 1),
    created_at: now,
    updated_at: now
  });
}

db.care_plans.insertMany(carePlans, { ordered: false });

// -----------------------------------------------------------------------------
// patient_surveys: 160 variable survey documents.
// -----------------------------------------------------------------------------
const surveys = [];
for (let i = 0; i < 160; i++) {
  const type = pick(surveyTypes, i);
  const responseCount = type === "PHQ-9" ? 9 : type === "GAD-7" ? 7 : type === "Pain" ? 4 : 5;
  const responses = [];
  let total = 0;

  for (let q = 1; q <= responseCount; q++) {
    const maxScore = type === "Satisfaction" ? 20 : type === "Pain" ? 10 : 3;
    const score = (i + q) % (maxScore + 1);
    total += score;
    responses.push({
      question_code: `${type.replace("-", "")}_Q${q}`,
      prompt: `Question ${q} for ${type}`,
      score,
      answer_text: score > maxScore / 2 ? "Positive / elevated response" : "Low or negative response"
    });
  }

  surveys.push({
    patient_id: patientId(i + 9),
    survey_type: type,
    completed_at: makeDate(i, 3),
    responses,
    score: {
      total,
      max_possible: type === "Satisfaction" ? 100 : type === "Pain" ? 40 : responseCount * 3,
      severity: severityFromScore(type, total)
    },
    source: pick(["portal", "tablet", "phone", "paper"], i),
    notes: total > responseCount * 2 ? "Follow-up recommended based on elevated score." : "No immediate concern reported.",
    created_at: now,
    updated_at: now
  });
}

db.patient_surveys.insertMany(surveys, { ordered: false });

print("MongoDB seed completed.");
print(`clinical_notes: ${db.clinical_notes.countDocuments()}`);
print(`medical_images_metadata: ${db.medical_images_metadata.countDocuments()}`);
print(`care_plans: ${db.care_plans.countDocuments()}`);
print(`patient_surveys: ${db.patient_surveys.countDocuments()}`);
