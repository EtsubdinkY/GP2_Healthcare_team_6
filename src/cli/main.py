#!/usr/bin/env python3
import sys
import re
from datetime import date, time

from src.config.database import close_pool
from src.models import Patient, Appointment, Prescription
from src.services import PatientService, AppointmentService, PrescriptionService
from src.services.clinical_record_service import ClinicalRecordService
from src.services.prescription_safety_service import PrescriptionSafetyService
from src.repositories.mongodb.clinical_notes_repo import ClinicalNotesRepository
from src.repositories.neo4j.knowledge_graph_repo import KnowledgeGraphRepository
from src.repositories.mongodb.care_plan_repo import CarePlanRepository
from src.services.lab_service import LabService

# helper functions for input

def get_input(prompt, required=True):
    while True:
        val = input(prompt).strip()
        if val or not required:
            return val
        print("this field is required")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("please enter a number")


def get_date(prompt):
    while True:
        val = input(f"{prompt} (YYYY-MM-DD): ").strip()
        try:
            return date.fromisoformat(val)
        except:
            print("wrong format, use YYYY-MM-DD")


def get_time(prompt):
    while True:
        val = input(f"{prompt} (HH:MM): ").strip()
        try:
            h, m = val.split(':')
            return time(int(h), int(m))
        except:
            print("wrong format, use HH:MM")


# ---- patient functions ----

def list_patients(svc):
    patients = svc.get_all_patients()

    print("\n" + "="*50)
    print("  ALL PATIENTS")
    print("="*50 + "\n")

    if not patients:
        print("no patients in the system")
        input("\nPress Enter...")
        return

    print(f"{'ID':<5} {'MRN':<12} {'Name':<25} {'DOB':<12} {'Phone':<15}")
    print("-" * 70)
    for p in patients:
        name = f"{p.first_name} {p.last_name}"
        print(f"{p.patient_id:<5} {p.mrn:<12} {name:<25} {str(p.dob):<12} {p.phone or 'N/A':<15}")
    print(f"\nTotal: {len(patients)}")
    input("\nPress Enter...")


def view_patient(svc):
    print("\n--- View Patient ---")
    pid = get_int("Enter Patient ID: ")
    p = svc.get_patient_by_id(pid)

    if not p:
        print(f"no patient found with ID {pid}")
        input("\nPress Enter...")
        return

    print(f"\nID: {p.patient_id}")
    print(f"MRN: {p.mrn}")
    print(f"Name: {p.first_name} {p.last_name}")
    print(f"DOB: {p.dob}")
    print(f"Gender: {p.gender}")
    print(f"Phone: {p.phone or 'N/A'}")
    print(f"Email: {p.email or 'N/A'}")
    print(f"Address: {p.address}, {p.city}, {p.state} {p.zip_code}")
    input("\nPress Enter...")


def patient_dashboard(svc):
    print("\n========== PATIENT DASHBOARD ==========\n")
    pid = get_int("Patient ID: ")
    dash = svc.get_patient_dashboard(pid)

    if not dash:
        print(f"patient {pid} not found")
        input("\nPress Enter...")
        return

    p = dash.patient
    print(f"\n--- {p.first_name} {p.last_name} (MRN: {p.mrn}) ---")
    print(f"DOB: {p.dob} | Phone: {p.phone or 'N/A'}")

    print("\nInsurance:")
    if dash.insurance_coverage:
        for ins in dash.insurance_coverage:
            print(f"  - {ins.policy_number} | {ins.coverage_type} | Copay: ${ins.copay}")
    else:
        print("  None")

    print("\nActive Prescriptions:")
    if dash.active_prescriptions:
        for rx in dash.active_prescriptions:
            print(f"  - Rx#{rx.rx_id}: {rx.dosage}, {rx.frequency}")
    else:
        print("  None")

    print("\nUpcoming Appointments:")
    if dash.upcoming_appointments:
        for apt in dash.upcoming_appointments:
            print(f"  - {apt.appt_date} {apt.appt_time} - {apt.reason}")
    else:
        print("  None")

    input("\nPress Enter...")


def add_patient(svc):
    print("\n*** Add New Patient ***\n")

    mrn = get_input("MRN (10 digits): ")
    ssn = get_input("SSN (optional): ", required=False) or None
    first = get_input("First Name: ")
    last = get_input("Last Name: ")
    dob = get_date("DOB")
    gender = get_input("Gender (Male/Female/Other): ")
    while gender not in ['Male', 'Female', 'Other']:
        print("please enter: Male, Female, or Other")
        gender = get_input("Try again: ")
    phone = get_input("Phone (optional): ", required=False) or None
    email = get_input("Email (optional): ", required=False) or None
    # db requires at least one of phone or email
    while phone is None and email is None:
        print("need at least a phone number or email")
        phone = get_input("Phone: ", required=False) or None
        email = get_input("Email: ", required=False) or None
    addr = get_input("Address: ")
    city = get_input("City: ")
    state = get_input("State (2-letter code e.g. MD): ").upper()
    while len(state) != 2 or not state.isalpha():
        print("state must be a 2-letter code like MD, VA, CA")
        state = get_input("State: ").upper()
    zipcode = get_input("ZIP: ")

    # the db enum only accepts these exact values (case sensitive)
    comm = get_input("Communication Preference (Email/Phone/Mail/Portal): ")
    while comm not in ['Email', 'Phone', 'Mail', 'Portal']:
        print("please enter exactly: Email, Phone, Mail, or Portal")
        comm = get_input("Try again: ")

    pharmacy = get_input("Preferred Pharmacy: ")

    p = Patient(
        patient_id=None, mrn=mrn, ssn=ssn, first_name=first, last_name=last,
        dob=dob, gender=gender, phone=phone, email=email, address=addr,
        city=city, state=state, zip_code=zipcode, comm_pref=comm, pref_pharmacy=pharmacy
    )

    try:
        created = svc.create_patient(p)
        print(f"\npatient added, ID is: {created.patient_id}")
    except Exception as e:
        print(f"something went wrong: {e}")
    input("\nPress Enter...")


def update_patient(svc):
    print("\n--- Update Patient ---\n")
    pid = get_int("Patient ID: ")
    p = svc.get_patient_by_id(pid)

    if not p:
        print("patient not found")
        input("\nPress Enter...")
        return

    print(f"updating {p.first_name} {p.last_name}")
    print("press Enter to keep existing value\n")

    mrn = get_input(f"MRN [{p.mrn}]: ", False) or p.mrn
    if len(mrn) > 10:
        print("MRN can't be more than 10 characters, keeping the old one")
        mrn = p.mrn

    ssn = get_input(f"SSN [{p.ssn}]: ", False) or p.ssn
    first = get_input(f"First Name [{p.first_name}]: ", False) or p.first_name
    last = get_input(f"Last Name [{p.last_name}]: ", False) or p.last_name
    dob_str = get_input(f"DOB [{p.dob}]: ", False)
    dob = date.fromisoformat(dob_str) if dob_str else p.dob
    gender = get_input(f"Gender [{p.gender}]: ", False) or p.gender
    phone = get_input(f"Phone [{p.phone}]: ", False) or p.phone
    email = get_input(f"Email [{p.email}]: ", False) or p.email
    addr = get_input(f"Address [{p.address}]: ", False) or p.address
    city = get_input(f"City [{p.city}]: ", False) or p.city
    state = get_input(f"State [{p.state}]: ", False) or p.state
    zipcode = get_input(f"ZIP [{p.zip_code}]: ", False) or p.zip_code
    comm = get_input(f"Comm Pref [{p.comm_pref}]: ", False) or p.comm_pref
    pharmacy = get_input(f"Pharmacy [{p.pref_pharmacy}]: ", False) or p.pref_pharmacy

    updated = Patient(
        patient_id=pid, mrn=mrn, ssn=ssn, first_name=first, last_name=last,
        dob=dob, gender=gender, phone=phone, email=email, address=addr,
        city=city, state=state, zip_code=zipcode, comm_pref=comm, pref_pharmacy=pharmacy
    )

    try:
        svc.update_patient(pid, updated)
        print("updated!")
    except Exception as e:
        print(f"error: {e}")
    input("\nPress Enter...")


def delete_patient(svc):
    print("\n--- Delete Patient ---")
    pid = get_int("Patient ID: ")
    p = svc.get_patient_by_id(pid)

    if not p:
        print("not found")
        input("\nPress Enter...")
        return

    confirm = input(f"delete {p.first_name} {p.last_name}? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.delete_patient(pid)
            print("deleted")
        except Exception as e:
            print(f"error: {e}")
    else:
        print("cancelled")
    input("\nPress Enter...")


def search_patients(svc):
    print("\n--- Search Patients ---")
    term = get_input("name to search: ")
    results = svc.search_patients_by_name(term)

    if not results:
        print("no matches found")
    else:
        print(f"\n{len(results)} result(s):")
        for p in results:
            print(f"  {p.patient_id}: {p.first_name} {p.last_name} ({p.mrn})")
    input("\nPress Enter...")


def polypharmacy_report(svc):
    print("\n===== Polypharmacy Report =====\n")
    results = svc.get_polypharmacy_patients(5)

    if not results:
        print("no patients with 5+ active prescriptions")
    else:
        for p, count in results:
            print(f"  {p.first_name} {p.last_name}: {count} active prescriptions")
    input("\nPress Enter...")


def patient_menu(svc):
    while True:
        print("\n" + "="*40)
        print("       PATIENT MANAGEMENT")
        print("="*40)
        print("1. List All Patients")
        print("2. View Patient")
        print("3. Patient Dashboard")
        print("4. Add Patient")
        print("5. Update Patient")
        print("6. Delete Patient")
        print("7. Search Patients")
        print("8. Polypharmacy Report")
        print("0. Back to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == '1': list_patients(svc)
        elif choice == '2': view_patient(svc)
        elif choice == '3': patient_dashboard(svc)
        elif choice == '4': add_patient(svc)
        elif choice == '5': update_patient(svc)
        elif choice == '6': delete_patient(svc)
        elif choice == '7': search_patients(svc)
        elif choice == '8': polypharmacy_report(svc)
        elif choice == '0': break
        else: print("invalid option")


# ---- appointment functions ----

def list_appointments(svc):
    print("\n------ All Appointments ------\n")
    appts = svc.get_all_appointments()

    if not appts:
        print("no appointments found")
        input("\nPress Enter...")
        return

    print(f"{'ID':<5} {'Date':<12} {'Time':<8} {'Patient':<10} {'Status':<12}")
    print("-" * 50)
    for a in appts:
        print(f"{a.appt_id:<5} {str(a.appt_date):<12} {str(a.appt_time)[:5]:<8} {a.patient_id:<10} {a.status:<12}")
    print(f"\nTotal: {len(appts)} appointments")
    input("\nPress Enter...")


def view_appointment(svc):
    print("\n--- View Appointment ---")
    aid = get_int("Appointment ID: ")
    detail = svc.get_appointment_detail(aid)

    if not detail:
        print("appointment not found")
        input("\nPress Enter...")
        return

    a = detail.appointment
    print(f"\nAppointment #{a.appt_id}")
    print(f"Date: {a.appt_date} at {a.appt_time}")
    print(f"Duration: {a.duration} mins")
    print(f"Status: {a.status}")
    print(f"Type: {a.appt_type}")
    print(f"Reason: {a.reason}")
    if detail.patient:
        print(f"Patient: {detail.patient.first_name} {detail.patient.last_name}")
    if detail.provider:
        print(f"Provider: Dr. {detail.provider.last_name}")
    input("\nPress Enter...")


def upcoming_appointments(svc):
    print("\n*** Upcoming Appointments ***\n")
    appts = svc.get_upcoming_appointments()

    if not appts:
        print("no upcoming appointments")
    else:
        for d in appts:
            a = d.appointment
            pname = f"{d.patient.first_name} {d.patient.last_name}" if d.patient else "N/A"
            print(f"  {a.appt_date} {str(a.appt_time)[:5]} - {pname} - {a.reason}")
    input("\nPress Enter...")


def schedule_appointment(svc):
    print("\n=== Schedule New Appointment ===\n")

    patient_id = get_int("Patient ID: ")
    provider_id = get_int("Provider ID: ")

    appt_date = get_date("Appointment Date")
    # don't allow past dates
    while appt_date <= date.today():
        print("that date is in the past, pick a future date")
        appt_date = get_date("Appointment Date")

    appt_time = get_time("Appointment Time")
    duration = get_int("Duration in minutes: ")
    appt_type = get_input("Appointment Type: ")
    reason = get_input("Reason for visit: ")
    notes = get_input("Notes (optional): ", False) or None

    appt = Appointment(
        appt_id=None, patient_id=patient_id, provider_id=provider_id,
        appt_date=appt_date, appt_time=appt_time, duration=duration,
        status='scheduled', appt_type=appt_type, reason=reason, notes=notes
    )

    try:
        created = svc.create_appointment(appt)
        print(f"\nscheduled! appointment ID: {created.appt_id}")
    except Exception as e:
        err = str(e)
        if "appointment_provider_id_fkey" in err:
            print("provider ID doesn't exist, double check it")
        elif "appointment_patient_id_fkey" in err:
            print("patient ID doesn't exist, double check it")
        else:
            print(f"failed: {e}")
    input("\nPress Enter...")


def cancel_appointment(svc):
    print("\n--- Cancel Appointment ---")
    aid = get_int("Appointment ID to cancel: ")

    confirm = input("sure? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.cancel_appointment(aid)
            print("cancelled")
        except Exception as e:
            print(f"error: {e}")
    else:
        print("ok, not cancelled")
    input("\nPress Enter...")


def delete_appointment(svc):
    print("\n--- Delete Appointment ---")
    aid = get_int("Appointment ID: ")

    confirm = input("confirm delete? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.delete_appointment(aid)
            print("deleted")
        except Exception as e:
            err = str(e)
            # this happens when there's a billing record tied to the appointment
            if "billing_record_appt_id_fkey" in err:
                print("can't delete this, it has billing records attached - cancel it instead")
            else:
                print(f"error: {e}")
    input("\nPress Enter...")


def appointment_menu(svc):
    while True:
        print("\n****************************************")
        print("*       APPOINTMENT MANAGEMENT         *")
        print("****************************************")
        print("1. List All Appointments")
        print("2. View Appointment Details")
        print("3. View Upcoming")
        print("4. Schedule New Appointment")
        print("5. Cancel Appointment")
        print("6. Delete Appointment")
        print("0. Back")

        choice = input("\nChoice: ").strip()

        if choice == '1': list_appointments(svc)
        elif choice == '2': view_appointment(svc)
        elif choice == '3': upcoming_appointments(svc)
        elif choice == '4': schedule_appointment(svc)
        elif choice == '5': cancel_appointment(svc)
        elif choice == '6': delete_appointment(svc)
        elif choice == '0': break
        else: print("invalid")


# ---- prescription functions ----

def list_prescriptions(svc):
    print("\n------ All Prescriptions ------\n")
    rxs = svc.get_all_prescriptions()

    if not rxs:
        print("none found")
        input("\nPress Enter...")
        return

    print(f"{'ID':<5} {'Date':<12} {'Patient':<10} {'Dosage':<15} {'Status':<10}")
    print("-" * 55)
    for rx in rxs:
        print(f"{rx.rx_id:<5} {str(rx.date_written):<12} {rx.patient_id:<10} {rx.dosage:<15} {rx.status:<10}")
    print(f"\n{len(rxs)} total")
    input("\nPress Enter...")


def view_prescription(svc):
    print("\n--- Prescription Details ---")
    rid = get_int("Prescription ID: ")
    detail = svc.get_prescription_detail(rid)

    if not detail:
        print("not found")
        input("\nPress Enter...")
        return

    rx = detail.prescription
    print(f"\nPrescription #{rx.rx_id}")
    print(f"Date Written: {rx.date_written}")
    print(f"Dosage: {rx.dosage}")
    print(f"Frequency: {rx.frequency}")
    print(f"Quantity: {rx.quantity}")
    print(f"Refills: {rx.refills}")
    print(f"Status: {rx.status}")
    print(f"Controlled: {'Yes' if rx.is_controlled else 'No'}")
    if detail.medication:
        print(f"Medication: {detail.medication.name}")
    if detail.patient:
        print(f"Patient: {detail.patient.first_name} {detail.patient.last_name}")
    if detail.provider:
        print(f"Prescriber: Dr. {detail.provider.last_name}")
    input("\nPress Enter...")


def active_prescriptions(svc):
    print("\n=== Active Prescriptions ===\n")
    rxs = svc.get_active_prescriptions()

    if not rxs:
        print("none")
    else:
        for d in rxs:
            rx = d.prescription
            med = d.medication.name if d.medication else "Unknown"
            pt = d.patient.last_name if d.patient else "Unknown"
            print(f"  Rx#{rx.rx_id}: {med} for {pt} - {rx.dosage}")
    input("\nPress Enter...")


def create_prescription(svc):
    print("\n*** New Prescription ***\n")

    patient_id = get_int("Patient ID: ")
    provider_id = get_int("Provider ID: ")
    med_id = get_int("Medication ID: ")
    date_written = get_date("Date Written")
    dosage = get_input("Dosage: ")
    frequency = get_input("Frequency: ")
    quantity = get_int("Quantity: ")
    refills = get_int("Refills: ")

    is_controlled = input("controlled substance? (yes/no): ").lower() == 'yes'
    schedule = None
    dea = None
    if is_controlled:
        valid_schedules = ['Schedule I', 'Schedule II', 'Schedule III', 'Schedule IV', 'Schedule V']
        schedule = get_input("DEA Schedule (e.g. Schedule II): ")
        while schedule not in valid_schedules:
            print("must be one of: Schedule I, Schedule II, Schedule III, Schedule IV, Schedule V")
            schedule = get_input("Try again: ")
        dea = get_input("Prescriber DEA Number: ")
        # format is 2 letters + 7 digits, e.g. AB1234563 - db rejects it otherwise
        while not re.match(r'^[A-Za-z]{2}\d{7}$', dea):
            print("wrong format, needs to be 2 letters then 7 digits like AB1234563")
            dea = get_input("DEA Number: ")

    rx = Prescription(
        rx_id=None, patient_id=patient_id, provider_id=provider_id, med_id=med_id,
        date_written=date_written, dosage=dosage, frequency=frequency,
        quantity=quantity, refills=refills, is_controlled=is_controlled,
        controlled_substance_schedule=schedule, prescriber_dea_number=dea, status='active'
    )

    try:
        created = svc.create_prescription(rx)
        print(f"\ncreated, ID: {created.rx_id}")
    except Exception as e:
        err = str(e)
        if "prescription_patient_id_fkey" in err:
            print("patient ID not found")
        elif "prescription_provider_id_fkey" in err:
            print("provider ID not found")
        elif "prescription_med_id_fkey" in err:
            print("medication ID not found")
        else:
            print(f"error: {e}")
    input("\nPress Enter...")


def discontinue_prescription(svc):
    print("\n--- Discontinue Prescription ---")
    rid = get_int("Rx ID: ")

    confirm = input("discontinue? (yes/no): ")
    if confirm.lower() == 'yes':
        result = svc.discontinue_prescription(rid)
        if result:
            print("done, prescription discontinued")
        else:
            print("rx not found")
    input("\nPress Enter...")


def controlled_report(svc):
    print("\n===== CONTROLLED SUBSTANCES REPORT =====\n")
    rxs = svc.get_controlled_substances()

    if not rxs:
        print("none found")
    else:
        print(f"{'Rx ID':<6} {'Schedule':<12} {'Patient':<15} {'DEA#':<15}")
        print("-" * 50)
        for d in rxs:
            rx = d.prescription
            pt = d.patient.last_name if d.patient else "N/A"
            sch = rx.controlled_substance_schedule or "N/A"
            dea = rx.prescriber_dea_number or "N/A"
            print(f"{rx.rx_id:<6} {sch:<12} {pt:<15} {dea:<15}")
    input("\nPress Enter...")


def prescription_menu(svc):
    while True:
        print("\n+-----------------------------------------+")
        print("|       PRESCRIPTION MANAGEMENT           |")
        print("+-----------------------------------------+")
        print("1. List All Prescriptions")
        print("2. View Prescription Details")
        print("3. View Active Prescriptions")
        print("4. Create New Prescription")
        print("5. Discontinue Prescription")
        print("6. Controlled Substances Report")
        print("0. Back to Main")

        choice = input("\nSelect option: ").strip()

        if choice == '1': list_prescriptions(svc)
        elif choice == '2': view_prescription(svc)
        elif choice == '3': active_prescriptions(svc)
        elif choice == '4': create_prescription(svc)
        elif choice == '5': discontinue_prescription(svc)
        elif choice == '6': controlled_report(svc)
        elif choice == '0': break
        else: print("invalid")


# main

def main_menu():
    patient_svc = PatientService()
    appt_svc = AppointmentService()
    rx_svc = PrescriptionService()

    while True:
        print("\n")
        print("##################################################")
        print("#                                                #")
        print("#       HEALTHCARE MANAGEMENT SYSTEM             #")
        print("#                                                #")
        print("##################################################")
        print("\n1. Patient Management")
        print("2. Appointment Management")
        print("3. Prescription Management")
        print("4. Quick View - Upcoming Appointments")
        print("5. Quick View - Active Prescriptions")
        print("6. Quick View - Polypharmacy Report")
        print("7. GP3 Cross-Database Operations")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1': patient_menu(patient_svc)
        elif choice == '2': appointment_menu(appt_svc)
        elif choice == '3': prescription_menu(rx_svc)
        elif choice == '4': upcoming_appointments(appt_svc)
        elif choice == '5': active_prescriptions(rx_svc)
        elif choice == '6': polypharmacy_report(patient_svc)
        elif choice == '7': gp3_integration_menu(patient_svc, appt_svc, rx_svc)
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("invalid, try again")

def gp3_integration_menu(patient_svc, appt_svc, rx_svc):
    mongo_notes_repo = ClinicalNotesRepository()
    mongo_care_plan_repo = CarePlanRepository()
    neo4j_repo = KnowledgeGraphRepository()
    lab_svc = LabService()

    clinical_service = ClinicalRecordService(
        patient_service=patient_svc,
        prescription_service=rx_svc,
        appointment_service=appt_svc,
        lab_service=lab_svc,
        mongo_notes_repo=mongo_notes_repo,
        mongo_care_plan_repo=mongo_care_plan_repo,
        neo4j_repo=neo4j_repo
    )

    safety_service = PrescriptionSafetyService(
        patient_service=patient_svc,
        prescription_service=rx_svc,
        neo4j_repo=neo4j_repo
    )

    while True:
        print("\n========================================")
        print("      GP3 CROSS-DATABASE OPERATIONS")
        print("========================================")
        print("1. Complete Patient Record")
        print("2. Prescription Safety Check")
        print("0. Back to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == '1':
            patient_id = get_int("Enter Patient ID: ")
            user_id = get_input("Enter User ID: ", required=False) or "demo_user"
            user_role = get_input("Enter User Role: ", required=False) or "clinician"

            record = clinical_service.get_complete_record(
                patient_id=patient_id,
                user_id=user_id,
                user_role=user_role
            )

            patient = record["demographics"]

            print("\n========== COMPLETE PATIENT RECORD ==========")

            print("\nPatient Demographics (PostgreSQL)")
            if patient:
                print(f"ID: {patient.patient_id}")
                print(f"Name: {patient.first_name} {patient.last_name}")
                print(f"MRN: {patient.mrn}")
                print(f"DOB: {patient.dob}")
            else:
                print("Patient not found.")

            print("\nActive Medications (PostgreSQL)")
            if record["active_medications"]:
                for item in record["active_medications"]:
                    med_name = item.medication.name if getattr(item, "medication", None) else "Unknown"
                    rx = item.prescription
                    print(f"- {med_name}: {rx.dosage}, {rx.frequency}")
            else:
                print("- None found")

            print("\nAppointments (PostgreSQL)")
            if record["appointments"]:
                for appt in record["appointments"][:5]:
                    print(f"- {appt.appt_date} {appt.appt_time}: {appt.reason} ({appt.status})")
            else:
                print("- None found")

            print("\nLaboratory Results (PostgreSQL)")
            if record["labs"]:
                for lab in record["labs"]:
                    value = lab["value"] if lab["value"] is not None else "Pending"
                    unit = lab["unit"] or ""
                    flag = lab["abnormal_flag"] or "N/A"
                    print(
                        f"- {lab['test_name']} ({lab['test_code']}): "
                        f"{value} {unit} | Status: {lab['status']} | Flag: {flag}"
                    )
            else:
                print("- No lab records available yet")

            print("\nRecent Clinical Notes (MongoDB)")
            if record["clinical_notes"]:
                for note in record["clinical_notes"]:
                    date_str = str(note.get('encounter_date', 'N/A')).split("T")[0]
                    print(f"- Date: {date_str}")
                    print(f"  Type: {note.get('note_type', 'N/A')}")
                    print(f"  Chief Complaint: {note.get('chief_complaint', 'N/A')}")
                    print(f"  Assessment: {note.get('assessment', note.get('discharge_diagnosis', 'N/A'))}")
                    print(f"  Plan: {note.get('plan', note.get('recommendations', note.get('follow_up', 'N/A')))}")
                    print()
            else:
                print("- No MongoDB notes available yet")

            print("\nCare Plans (MongoDB)")
            if record["care_plans"]:
                for plan in record["care_plans"]:
                    diagnosis = plan.get("primary_diagnosis", {})
                    print(f"- Diagnosis: {diagnosis.get('name', 'N/A')}")
                    print(f"  Status: {plan.get('status', 'N/A')}")
                    print(f"  Last Reviewed: {str(plan.get('last_reviewed', 'N/A')).split('T')[0]}")
                    print(f"  Review Frequency: {plan.get('review_frequency_days', 'N/A')} days")

                    goals = plan.get("goals", [])
                    if goals:
                        print("  Goals:")
                        for goal in goals[:2]:
                            print(f"    - {goal.get('description', 'N/A')} ({goal.get('status', 'N/A')})")
                    print()
            else:
                print("- No active care plans found")

            if record["safety_alerts"]:
                print("\nMedication Safety Alerts (Neo4j)")
                for alert in record["safety_alerts"]:
                    print(f"- {alert.medication1} + {alert.medication2}: {alert.severity} - {alert.description}")

            input("\nPress Enter...")

        elif choice == '2':
            patient_id = get_int("Enter Patient ID: ")
            new_medication = get_input("Enter New Medication Name: ")

            result = safety_service.check_prescription_safety(
                patient_id=patient_id,
                new_medication_name=new_medication
            )

            print("\n========== PRESCRIPTION SAFETY CHECK ==========")
            print(result["message"])

            if result["interaction_alerts"]:
                print("\nInteraction Warnings:")
                for alert in result["interaction_alerts"]:
                    print(f"- {alert.medication1} + {alert.medication2}: {alert.severity} - {alert.description}")
                print("\nPrescription should NOT be inserted.")
            else:
                print("\nNo warnings found.")

                insert_choice = get_input(
                    "Do you want to insert this prescription into PostgreSQL? (yes/no): "
                )

                if insert_choice.lower() == "yes":
                    provider_id = get_int("Enter Provider ID: ")
                    med_id = get_int("Enter Medication ID: ")
                    date_written = get_date("Date Written")
                    dosage = get_input("Dosage: ")
                    frequency = get_input("Frequency: ")
                    quantity = get_int("Quantity: ")
                    refills = get_int("Refills: ")

                    rx = Prescription(
                        rx_id=None,
                        patient_id=patient_id,
                        provider_id=provider_id,
                        med_id=med_id,
                        date_written=date_written,
                        dosage=dosage,
                        frequency=frequency,
                        quantity=quantity,
                        refills=refills,
                        is_controlled=False,
                        controlled_substance_schedule=None,
                        prescriber_dea_number=None,
                        status="active"
                    )

                    try:
                        created = rx_svc.create_prescription(rx)
                        print(f"\nPrescription inserted successfully into PostgreSQL. New Rx ID: {created.rx_id}")
                    except Exception as e:
                        print(f"\nPrescription was not inserted. Error: {e}")
                else:
                    print("\nPrescription was not inserted.")

            input("\nPress Enter...")

        elif choice == '0':
            break

        else:
            print("invalid option")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nexiting...")
    finally:
        close_pool()