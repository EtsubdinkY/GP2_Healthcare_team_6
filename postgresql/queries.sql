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