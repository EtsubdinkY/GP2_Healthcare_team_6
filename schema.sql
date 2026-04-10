-- Group Project: Healthcare Patient Management Platform
-- This SQL script defines Group 6 database schema for our healthcare patient management platform project and it a continuation from GP1.
-- Group Members: Louis Tafah, Pushkar Vishwas, Adyasha Mishra, and Etsubdink Workalemahu Yergashewa.

-- This section enables the required extensions for pgcrypto, remove existing tables, and defines ENUM types for contraints.

BEGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP TABLE IF EXISTS lab_result CASCADE;
DROP TABLE IF EXISTS lab_order_item CASCADE;
DROP TABLE IF EXISTS lab_order CASCADE;
DROP TABLE IF EXISTS lab_test CASCADE;
DROP TABLE IF EXISTS claim CASCADE;
DROP TABLE IF EXISTS billing_record CASCADE;
DROP TABLE IF EXISTS patient_insurance CASCADE;
DROP TABLE IF EXISTS insurance_plan CASCADE;
DROP TABLE IF EXISTS admission CASCADE;
DROP TABLE IF EXISTS prescription CASCADE;
DROP TABLE IF EXISTS medication CASCADE;
DROP TABLE IF EXISTS appointment CASCADE;
DROP TABLE IF EXISTS allergy CASCADE;
DROP TABLE IF EXISTS emergency_contact CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
DROP TABLE IF EXISTS provider CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS hospital CASCADE;
DROP TYPE IF EXISTS facility_type_enum CASCADE;
DROP TYPE IF EXISTS gender_enum CASCADE;
DROP TYPE IF EXISTS comm_pref_enum CASCADE;
DROP TYPE IF EXISTS appointment_status_enum CASCADE;
DROP TYPE IF EXISTS rx_status_enum CASCADE;
DROP TYPE IF EXISTS claim_status_enum CASCADE;
DROP TYPE IF EXISTS billing_status_enum CASCADE;
DROP TYPE IF EXISTS admission_status_enum CASCADE;
DROP TYPE IF EXISTS lab_status_enum CASCADE;
DROP TYPE IF EXISTS priority_enum CASCADE;
DROP TYPE IF EXISTS coverage_enum CASCADE;
DROP TYPE IF EXISTS severity_enum CASCADE;
DROP TYPE IF EXISTS relationship_enum CASCADE;
CREATE TYPE facility_type_enum AS ENUM ('Hospital', 'Clinic');
CREATE TYPE gender_enum AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE comm_pref_enum AS ENUM ('Email', 'Phone', 'Mail', 'Portal');
CREATE TYPE appointment_status_enum AS ENUM ('scheduled', 'checked_in', 'completed', 'cancelled', 'no_show');
CREATE TYPE rx_status_enum AS ENUM ('active', 'completed', 'cancelled');
CREATE TYPE claim_status_enum AS ENUM ('submitted', 'paid', 'denied', 'pending');
CREATE TYPE billing_status_enum AS ENUM ('open', 'paid', 'partial', 'void');
CREATE TYPE admission_status_enum AS ENUM ('admitted', 'discharged', 'cancelled');
CREATE TYPE lab_status_enum AS ENUM ('ordered', 'collected', 'resulted', 'cancelled');
CREATE TYPE priority_enum AS ENUM ('Routine', 'Urgent', 'STAT');
CREATE TYPE coverage_enum AS ENUM ('Primary', 'Secondary');
CREATE TYPE severity_enum AS ENUM ('Low', 'Moderate', 'High', 'Critical');
CREATE TYPE relationship_enum AS ENUM ('Spouse', 'Parent', 'Child', 'Sibling', 'Friend', 'Guardian', 'Other');


-- Trigger funtions  to automatically set created_at and updated_at timestamps

CREATE OR REPLACE FUNCTION set_timestamp_fields()
    RETURNS TRIGGER AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.created_at := COALESCE(NEW.created_at, CURRENT_TIMESTAMP);
        NEW.updated_at := COALESCE(NEW.updated_at, CURRENT_TIMESTAMP);
    ELSE
        NEW.updated_at := CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- HOSPITAL TABLE with constraints to ensure data integrity, including checks for state and zip code formats, bed count based on facility type, and unique hospital names.

CREATE TABLE hospital
(
    hospital_id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    facility_type facility_type_enum NOT NULL,
    name          VARCHAR(120)       NOT NULL UNIQUE,
    address       TEXT               NOT NULL,
    city          VARCHAR(80)        NOT NULL,
    state         CHAR(2)            NOT NULL CHECK (state ~ '^[A-Z]{2}$'),
    zip_code      VARCHAR(10)        NOT NULL CHECK (zip_code ~ '^\d{5}(-\d{4})?$'),
    phone         VARCHAR(20)        NOT NULL,
    bed_count     INT                NOT NULL DEFAULT 0 CHECK (bed_count >= 0),
    created_at    TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_beds_for_facility_type CHECK (
        (facility_type = 'Hospital' AND bed_count >= 1)
            OR (facility_type = 'Clinic' AND bed_count = 0)
        )
);


-- DEPARTMENT TABLE 

CREATE TABLE department
(
    dept_id     INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hospital_id INT          NOT NULL REFERENCES hospital (hospital_id) ON DELETE CASCADE ON UPDATE CASCADE,
    name        VARCHAR(100) NOT NULL,
    phone       VARCHAR(20)  NOT NULL,
    floor       INT          NOT NULL CHECK (floor >= 0),
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_department_per_facility UNIQUE (hospital_id, name)
);


-- PROVIDER TABLE 

CREATE TABLE provider
(
    provider_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dept_id     INT          NOT NULL REFERENCES department (dept_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    npi         VARCHAR(10)  NOT NULL UNIQUE,
    dea_number  VARCHAR(20),
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    speciality  VARCHAR(100) NOT NULL,
    license_no  VARCHAR(50)  NOT NULL UNIQUE,
    licence_exp DATE         NOT NULL,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_npi_format CHECK (npi ~ '^\d{10}$'),
    CONSTRAINT chk_dea_format CHECK (dea_number IS NULL OR dea_number ~ '^[A-Z]{2}\d{7}$')
);


-- PATIENT TABLE 

CREATE TABLE patient
(
    patient_id    INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    mrn           VARCHAR(10)    NOT NULL UNIQUE,
    ssn           VARCHAR(11) UNIQUE,
    first_name    VARCHAR(50)    NOT NULL,
    last_name     VARCHAR(50)    NOT NULL,
    dob           DATE           NOT NULL CHECK (dob <= CURRENT_DATE),
    gender        gender_enum    NOT NULL,
    phone         VARCHAR(20),
    email         VARCHAR(100),
    address       TEXT           NOT NULL,
    city          VARCHAR(80)    NOT NULL,
    state         CHAR(2)        NOT NULL CHECK (state ~ '^[A-Z]{2}$'),
    zip_code      VARCHAR(10)    NOT NULL CHECK (zip_code ~ '^\d{5}(-\d{4})?$'),
    comm_pref     comm_pref_enum NOT NULL,
    pref_pharmacy VARCHAR(100)   NOT NULL,
    created_at    TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_mrn_format CHECK (mrn ~ '^\d{10}$'),
    CONSTRAINT chk_ssn_format CHECK (ssn IS NULL OR ssn ~ '^\d{3}-\d{2}-\d{4}$'),
    CONSTRAINT chk_patient_contact CHECK (phone IS NOT NULL OR email IS NOT NULL)
);


-- EMERGENCY CONTACT TABLE

CREATE TABLE emergency_contact
(
    contact_id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id   INT               NOT NULL REFERENCES patient (patient_id) ON DELETE CASCADE ON UPDATE CASCADE,
    name         VARCHAR(100)      NOT NULL,
    relationship relationship_enum NOT NULL,
    phone        VARCHAR(20)       NOT NULL,
    email        VARCHAR(100),
    created_at   TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ALLERGY TABLE

CREATE TABLE allergy
(
    allergy_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id INT           NOT NULL REFERENCES patient (patient_id) ON DELETE CASCADE ON UPDATE CASCADE,
    allergen   VARCHAR(100)  NOT NULL,
    severity   severity_enum NOT NULL,
    reaction   TEXT          NOT NULL,
    onset_date DATE,
    created_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);


--- APPOINTMENT TABLE

CREATE TABLE appointment
(
    appt_id     INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id  INT                     NOT NULL REFERENCES patient (patient_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    provider_id INT                     NOT NULL REFERENCES provider (provider_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    appt_date   DATE                    NOT NULL,
    appt_time   TIME                    NOT NULL,
    duration    INT                     NOT NULL CHECK (duration BETWEEN 10 AND 240),
    status      appointment_status_enum NOT NULL,
    appt_type   VARCHAR(50)             NOT NULL,
    reason      TEXT                    NOT NULL,
    notes       TEXT,
    created_at  TIMESTAMP               NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP               NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_provider_datetime UNIQUE (provider_id, appt_date, appt_time)
);


-- MEDICATION TABLE

CREATE TABLE medication
(
    med_id                        INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name                          VARCHAR(100) NOT NULL UNIQUE,
    generic_name                  VARCHAR(100) NOT NULL,
    drug_class                    VARCHAR(100) NOT NULL,
    controlled_substance_schedule VARCHAR(20),
    form                          VARCHAR(50)  NOT NULL,
    created_at                    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_controlled_schedule CHECK (
        controlled_substance_schedule IS NULL
            OR
        controlled_substance_schedule IN ('Schedule I', 'Schedule II', 'Schedule III', 'Schedule IV', 'Schedule V')
        )
);


--- PRESCRIPTION TABLE

CREATE TABLE prescription
(
    rx_id                         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id                    INT            NOT NULL REFERENCES patient (patient_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    provider_id                   INT            NOT NULL REFERENCES provider (provider_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    med_id                        INT            NOT NULL REFERENCES medication (med_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    date_written                  DATE           NOT NULL,
    dosage                        VARCHAR(50)    NOT NULL,
    frequency                     VARCHAR(50)    NOT NULL,
    quantity                      INT            NOT NULL CHECK (quantity > 0),
    refills                       INT            NOT NULL DEFAULT 0 CHECK (refills >= 0),
    is_controlled                 BOOLEAN        NOT NULL DEFAULT FALSE,
    controlled_substance_schedule VARCHAR(20),
    prescriber_dea_number         VARCHAR(20),
    status                        rx_status_enum NOT NULL,
    created_at                    TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                    TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_rx_controlled_schedule CHECK (
        controlled_substance_schedule IS NULL
            OR
        controlled_substance_schedule IN ('Schedule I', 'Schedule II', 'Schedule III', 'Schedule IV', 'Schedule V')
        ),
    CONSTRAINT chk_dea_for_controlled CHECK (
        controlled_substance_schedule IS NULL OR prescriber_dea_number IS NOT NULL
        ),
    CONSTRAINT chk_controlled_consistency CHECK (
        (is_controlled = FALSE AND controlled_substance_schedule IS NULL)
            OR (is_controlled = TRUE AND controlled_substance_schedule IS NOT NULL)
        ),
    CONSTRAINT chk_prescriber_dea_format CHECK (
        prescriber_dea_number IS NULL OR prescriber_dea_number ~ '^[A-Z]{2}\d{7}$'
        )
);


-- ADMISSION TABLE 

CREATE TABLE admission
(
    admission_id        INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id          INT                   NOT NULL REFERENCES patient (patient_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    hospital_id         INT                   NOT NULL REFERENCES hospital (hospital_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    provider_id         INT                   NOT NULL REFERENCES provider (provider_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    admit_date          DATE                  NOT NULL,
    discharge_date      DATE,
    admit_reason        TEXT                  NOT NULL,
    discharge_diagnosis TEXT,
    room_number         VARCHAR(20),
    status              admission_status_enum NOT NULL,
    created_at          TIMESTAMP             NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP             NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_admission_dates CHECK (discharge_date IS NULL OR discharge_date >= admit_date)
);


--- INSURANCE PLAN TABLE

CREATE TABLE insurance_plan
(
    plan_id    INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payer_name VARCHAR(100) NOT NULL,
    plan_type  VARCHAR(50)  NOT NULL,
    phone      VARCHAR(20)  NOT NULL,
    address    TEXT         NOT NULL,
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_payer_plan UNIQUE (payer_name, plan_type)
);


-- PATIENT INSURANCE TABLE

CREATE TABLE patient_insurance
(
    pat_ins_id    INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id    INT            NOT NULL REFERENCES patient (patient_id) ON DELETE CASCADE ON UPDATE CASCADE,
    plan_id       INT            NOT NULL REFERENCES insurance_plan (plan_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    policy_number VARCHAR(50)    NOT NULL UNIQUE,
    group_number  VARCHAR(50),
    copay         NUMERIC(10, 2) NOT NULL CHECK (copay >= 0),
    coverage_type coverage_enum  NOT NULL,
    start_date    DATE           NOT NULL,
    end_date      DATE,
    created_at    TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_coverage_dates CHECK (end_date IS NULL OR end_date >= start_date)
);


-- BILLING RECORD TABLE

CREATE TABLE billing_record
(
    bill_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    appt_id      INT                 NOT NULL UNIQUE REFERENCES appointment (appt_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    pat_ins_id   INT                 NOT NULL REFERENCES patient_insurance (pat_ins_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    service_date DATE                NOT NULL,
    total_amount NUMERIC(10, 2)      NOT NULL CHECK (total_amount >= 0),
    paid_amount  NUMERIC(10, 2)      NOT NULL DEFAULT 0 CHECK (paid_amount >= 0),
    balance      NUMERIC(10, 2)      NOT NULL CHECK (balance >= 0),
    status       billing_status_enum NOT NULL,
    billing_code VARCHAR(50)         NOT NULL,
    created_at   TIMESTAMP           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_balance_math CHECK (ROUND(total_amount - paid_amount, 2) = balance)
);


-- CLAIM TABLE

CREATE TABLE claim
(
    claim_id               INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bill_id                INT               NOT NULL REFERENCES billing_record (bill_id) ON DELETE CASCADE ON UPDATE CASCADE,
    pat_ins_id             INT               NOT NULL REFERENCES patient_insurance (pat_ins_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    cpt_code               VARCHAR(50)       NOT NULL,
    icd10_code             VARCHAR(50)       NOT NULL,
    charge_amount          NUMERIC(10, 2)    NOT NULL CHECK (charge_amount >= 0),
    payment_amount         NUMERIC(10, 2)    NOT NULL DEFAULT 0 CHECK (payment_amount >= 0),
    patient_responsibility NUMERIC(10, 2)    NOT NULL DEFAULT 0 CHECK (patient_responsibility >= 0),
    status                 claim_status_enum NOT NULL,
    denial_reason          TEXT,
    claim_date             DATE              NOT NULL,
    created_at             TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- LAB_TEST TABLE

CREATE TABLE lab_test
(
    test_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    test_name    VARCHAR(100) NOT NULL UNIQUE,
    test_code    VARCHAR(50)  NOT NULL UNIQUE,
    category     VARCHAR(50)  NOT NULL,
    normal_range VARCHAR(50)  NOT NULL,
    unit         VARCHAR(20)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- LAB_ORDER TABLE

CREATE TABLE lab_order
(
    order_id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    appt_id    INT             NOT NULL REFERENCES appointment (appt_id) ON DELETE CASCADE ON UPDATE CASCADE,
    order_date DATE            NOT NULL,
    priority   priority_enum   NOT NULL,
    status     lab_status_enum NOT NULL,
    notes      TEXT,
    created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- LAB_ORDER_ITEM TABLE

CREATE TABLE lab_order_item
(
    order_item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id      INT       NOT NULL REFERENCES lab_order (order_id) ON DELETE CASCADE ON UPDATE CASCADE,
    test_id       INT       NOT NULL REFERENCES lab_test (test_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_order_test UNIQUE (order_id, test_id)
);


-- LAB_RESULT TABLE

CREATE TABLE lab_result
(
    result_id     INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_item_id INT         NOT NULL UNIQUE REFERENCES lab_order_item (order_item_id) ON DELETE CASCADE ON UPDATE CASCADE,
    value         VARCHAR(50) NOT NULL,
    unit          VARCHAR(20) NOT NULL,
    abnormal_flag BOOLEAN     NOT NULL DEFAULT FALSE,
    result_date   DATE        NOT NULL,
    created_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Create triggers to automatically update timestamps on insert and update for all tables

CREATE TRIGGER trg_hospital_timestamps
    BEFORE INSERT OR UPDATE
    ON hospital
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_department_timestamps
    BEFORE INSERT OR UPDATE
    ON department
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_provider_timestamps
    BEFORE INSERT OR UPDATE
    ON provider
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_patient_timestamps
    BEFORE INSERT OR UPDATE
    ON patient
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_emergency_contact_timestamps
    BEFORE INSERT OR UPDATE
    ON emergency_contact
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_allergy_timestamps
    BEFORE INSERT OR UPDATE
    ON allergy
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_appointment_timestamps
    BEFORE INSERT OR UPDATE
    ON appointment
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_medication_timestamps
    BEFORE INSERT OR UPDATE
    ON medication
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_prescription_timestamps
    BEFORE INSERT OR UPDATE
    ON prescription
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_admission_timestamps
    BEFORE INSERT OR UPDATE
    ON admission
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_insurance_plan_timestamps
    BEFORE INSERT OR UPDATE
    ON insurance_plan
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_patient_insurance_timestamps
    BEFORE INSERT OR UPDATE
    ON patient_insurance
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_billing_record_timestamps
    BEFORE INSERT OR UPDATE
    ON billing_record
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_claim_timestamps
    BEFORE INSERT OR UPDATE
    ON claim
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_lab_test_timestamps
    BEFORE INSERT OR UPDATE
    ON lab_test
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_lab_order_timestamps
    BEFORE INSERT OR UPDATE
    ON lab_order
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_lab_order_item_timestamps
    BEFORE INSERT OR UPDATE
    ON lab_order_item
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();
CREATE TRIGGER trg_lab_result_timestamps
    BEFORE INSERT OR UPDATE
    ON lab_result
    FOR EACH ROW
EXECUTE FUNCTION set_timestamp_fields();


-- Create indexes to optimize common query patterns

CREATE INDEX idx_department_hospital ON department (hospital_id);
CREATE INDEX idx_provider_dept ON provider (dept_id);
CREATE INDEX idx_provider_last_name ON provider (last_name);
CREATE INDEX idx_patient_last_name ON patient (last_name);
CREATE INDEX idx_patient_mrn ON patient (mrn);
CREATE INDEX idx_appointment_patient_date ON appointment (patient_id, appt_date);
CREATE INDEX idx_appointment_provider_date ON appointment (provider_id, appt_date);
CREATE INDEX idx_prescription_patient_date ON prescription (patient_id, date_written);
CREATE INDEX idx_patient_insurance_patient ON patient_insurance (patient_id);
CREATE INDEX idx_billing_status_date ON billing_record (status, service_date);
CREATE INDEX idx_claim_status_date ON claim (status, claim_date);
CREATE INDEX idx_lab_order_appt ON lab_order (appt_id);
CREATE INDEX idx_admission_patient_date ON admission (patient_id, admit_date);

COMMIT;