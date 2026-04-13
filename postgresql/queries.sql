-- Query #1: Patient Care Coordination
-- Clinical/Financial/Operational Context: Supports front-desk and clinical staff by showing a patient’s demographics,
-- insurance coverage, and active prescriptions for an appointment encounter.
-- Tables Used: appointment, patient, patient_insurance, insurance_plan, prescription, medication
-- Complexity Features: JOINs, LEFT JOINs, date-range filtering, aggregation with STRING_AGG

SELECT
    a.appt_id,
    a.appt_date,
    a.appt_time,
    p.patient_id,
    p.mrn,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.dob,
    p.gender,
    p.phone,
    p.email,
    ip.payer_name,
    ip.plan_type,
    pi.policy_number,
    pi.coverage_type,
    pi.copay,
    COALESCE(
        STRING_AGG(
            DISTINCT m.name || ' (' || rx.dosage || ', ' || rx.frequency || ')',
            '; '
        ) FILTER (WHERE rx.status = 'active'),
        'No active prescriptions'
    ) AS active_prescriptions
FROM appointment a
JOIN patient p
    ON a.patient_id = p.patient_id
LEFT JOIN patient_insurance pi
    ON p.patient_id = pi.patient_id
   AND pi.start_date <= a.appt_date
   AND (pi.end_date IS NULL OR pi.end_date >= a.appt_date)
LEFT JOIN insurance_plan ip
    ON pi.plan_id = ip.plan_id
LEFT JOIN prescription rx
    ON p.patient_id = rx.patient_id
   AND rx.status = 'active'
LEFT JOIN medication m
    ON rx.med_id = m.med_id
GROUP BY
    a.appt_id, a.appt_date, a.appt_time,
    p.patient_id, p.mrn, p.first_name, p.last_name, p.dob, p.gender, p.phone, p.email,
    ip.payer_name, ip.plan_type, pi.policy_number, pi.coverage_type, pi.copay
ORDER BY a.appt_date, a.appt_time, patient_name;


-- Query #2: Medication Safety - Polypharmacy Risk
-- Clinical/Financial/Operational Context: Identifies patients with 5 or more active prescriptions,
-- which may indicate medication burden or interaction risk.
-- Tables Used: patient, prescription, provider
-- Complexity Features: JOINs, GROUP BY, HAVING, DISTINCT aggregation

SELECT
    p.patient_id,
    p.mrn,
    p.first_name || ' ' || p.last_name AS patient_name,
    COUNT(rx.rx_id) AS active_prescription_count,
    STRING_AGG(
        DISTINCT pr.first_name || ' ' || pr.last_name,
        ', '
        ORDER BY pr.first_name || ' ' || pr.last_name
    ) AS prescribing_providers
FROM patient p
JOIN prescription rx
    ON p.patient_id = rx.patient_id
JOIN provider pr
    ON rx.provider_id = pr.provider_id
WHERE rx.status = 'active'
GROUP BY p.patient_id, p.mrn, p.first_name, p.last_name
HAVING COUNT(rx.rx_id) >= 5
ORDER BY active_prescription_count DESC, patient_name;

-- Query #3: Provider Workload - Upcoming Appointments
-- Clinical/Financial/Operational Context: Helps providers and schedulers view upcoming patient visits,
-- visit types, and reasons for visit.
-- Tables Used: provider, appointment, patient
-- Complexity Features: JOINs, filtering, ordering

SELECT
    pr.provider_id,
    pr.first_name || ' ' || pr.last_name AS provider_name,
    pr.speciality,
    a.appt_id,
    a.appt_date,
    a.appt_time,
    p.first_name || ' ' || p.last_name AS patient_name,
    a.appt_type,
    a.reason,
    a.status
FROM provider pr
JOIN appointment a
    ON pr.provider_id = a.provider_id
JOIN patient p
    ON a.patient_id = p.patient_id
WHERE a.appt_date >= CURRENT_DATE
  AND a.status IN ('scheduled', 'checked_in')
ORDER BY pr.provider_id, a.appt_date, a.appt_time;

-- Query #4: Insurance Coverage Summary
-- Financial/Operational Context: Summarizes each insurance payer’s covered patients and average copay.
-- Useful for payer-mix and reimbursement planning.
-- Tables Used: insurance_plan, patient_insurance
-- Complexity Features: JOINs, COUNT DISTINCT, AVG, GROUP BY

SELECT
    ip.payer_name,
    ip.plan_type,
    COUNT(DISTINCT pi.patient_id) AS covered_patients,
    ROUND(AVG(pi.copay), 2) AS avg_copay
FROM insurance_plan ip
JOIN patient_insurance pi
    ON ip.plan_id = pi.plan_id
WHERE pi.end_date IS NULL OR pi.end_date >= CURRENT_DATE
GROUP BY ip.payer_name, ip.plan_type
ORDER BY covered_patients DESC, ip.payer_name, ip.plan_type;


-- Query #5: Prescription Costs / Coverage View
-- Clinical/Financial Context: Lists active prescriptions together with the patient’s insurance policy
-- to support medication coverage review and billing coordination.
-- Tables Used: prescription, patient, medication, patient_insurance, insurance_plan
-- Complexity Features: JOINs, active coverage filtering, ordering

SELECT
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    m.name AS medication_name,
    rx.dosage,
    rx.frequency,
    rx.date_written,
    ip.payer_name,
    ip.plan_type,
    pi.policy_number,
    pi.copay,
    rx.status
FROM prescription rx
JOIN patient p
    ON rx.patient_id = p.patient_id
JOIN medication m
    ON rx.med_id = m.med_id
LEFT JOIN patient_insurance pi
    ON rx.patient_id = pi.patient_id
   AND pi.start_date <= rx.date_written
   AND (pi.end_date IS NULL OR pi.end_date >= rx.date_written)
LEFT JOIN insurance_plan ip
    ON pi.plan_id = ip.plan_id
WHERE rx.status = 'active'
ORDER BY patient_name, medication_name;


-- Query #6: Provider Productivity
-- Operational Context: Measures provider activity, no-show rates, and average patients seen per appointment day.
-- Tables Used: provider, appointment
-- Complexity Features: JOINs, conditional aggregates, NULLIF, ROUND

SELECT
    pr.provider_id,
    pr.first_name || ' ' || pr.last_name AS provider_name,
    pr.speciality,
    COUNT(a.appt_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count,
    ROUND(
        100.0 * SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.appt_id), 0),
        2
    ) AS no_show_rate_pct,
    ROUND(
        COUNT(a.appt_id)::NUMERIC / NULLIF(COUNT(DISTINCT a.appt_date), 0),
        2
    ) AS avg_patients_per_day
FROM provider pr
LEFT JOIN appointment a
    ON pr.provider_id = a.provider_id
GROUP BY pr.provider_id, pr.first_name, pr.last_name, pr.speciality
ORDER BY total_appointments DESC, provider_name;



-- Query #7: Controlled Substances - Schedule II DEA Reporting
-- Clinical/Regulatory Context: Reports all Schedule II prescriptions by provider for controlled-substance review
-- and DEA-related compliance reporting.
-- Tables Used: prescription, provider, patient, medication
-- Complexity Features: JOINs, filtering, ordering

SELECT
    rx.rx_id,
    rx.date_written,
    pr.provider_id,
    pr.first_name || ' ' || pr.last_name AS provider_name,
    pr.dea_number AS provider_dea_on_file,
    rx.prescriber_dea_number,
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    m.name AS medication_name,
    rx.dosage,
    rx.quantity,
    rx.status
FROM prescription rx
JOIN provider pr
    ON rx.provider_id = pr.provider_id
JOIN patient p
    ON rx.patient_id = p.patient_id
JOIN medication m
    ON rx.med_id = m.med_id
WHERE rx.is_controlled = TRUE
  AND rx.controlled_substance_schedule = 'Schedule II'
ORDER BY provider_name, rx.date_written, patient_name;


-- Query #8: Appointment Status Breakdown by Facility
-- Operational Context: Shows appointment outcomes by facility for capacity, scheduling,
-- and front-desk performance monitoring.
-- Tables Used: appointment, provider, department, hospital
-- Complexity Features: JOINs, conditional aggregation, GROUP BY
-- Note: appointment does not store hospital_id directly in the current schema,
-- so facility is inferred through provider -> department -> hospital.

SELECT
    h.hospital_id,
    h.name AS facility_name,
    h.facility_type,
    COUNT(a.appt_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count,
    SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
    SUM(CASE WHEN a.status = 'scheduled' THEN 1 ELSE 0 END) AS scheduled_count,
    SUM(CASE WHEN a.status = 'checked_in' THEN 1 ELSE 0 END) AS checked_in_count
FROM appointment a
JOIN provider pr
    ON a.provider_id = pr.provider_id
JOIN department d
    ON pr.dept_id = d.dept_id
JOIN hospital h
    ON d.hospital_id = h.hospital_id
GROUP BY h.hospital_id, h.name, h.facility_type
ORDER BY h.name;

