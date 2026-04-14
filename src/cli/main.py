#!/usr/bin/env python3
import sys
from datetime import date, time

from src.config.database import close_pool
from src.models import Patient, Appointment, Prescription
from src.services import PatientService, AppointmentService, PrescriptionService


def get_input(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required!")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Enter a valid number")


def get_date(prompt):
    while True:
        val = input(f"{prompt} (YYYY-MM-DD): ").strip()
        try:
            return date.fromisoformat(val)
        except:
            print("Wrong format, use YYYY-MM-DD")


def get_time(prompt):
    while True:
        val = input(f"{prompt} (HH:MM): ").strip()
        try:
            h, m = val.split(':')
            return time(int(h), int(m))
        except:
            print("Wrong format")


# patient stuff

def list_patients(svc):
    print("\n" + "="*50)
    print("  ALL PATIENTS")
    print("="*50 + "\n")

    patients = svc.get_all_patients()
    if not patients:
        print("No patients found.")
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
        print(f"Patient {pid} not found")
    else:
        print(f"\nID: {p.patient_id}")
        print(f"MRN: {p.mrn}")
        print(f"Name: {p.first_name} {p.last_name}")
        print(f"DOB: {p.dob}")
        print(f"Gender: {p.gender}")
        print(f"Phone: {p.phone or 'N/A'}")
        print(f"Email: {p.email or 'N/A'}")
        print(f"Address: {p.address}, {p.city}, {p.state} {p.zip_code}")
    input("\nPress Enter to continue...")


def patient_dashboard(svc):
    print("\n========== PATIENT DASHBOARD ==========\n")
    pid = get_int("Patient ID: ")
    dash = svc.get_patient_dashboard(pid)

    if not dash:
        print(f"Patient {pid} not found")
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
    gender = get_input("Gender: ")
    phone = get_input("Phone (optional): ", required=False) or None
    email = get_input("Email (optional): ", required=False) or None
    addr = get_input("Address: ")
    city = get_input("City: ")
    state = get_input("State: ")
    zipcode = get_input("ZIP: ")
    comm = get_input("Communication Preference (email/phone/mail): ")
    pharmacy = get_input("Preferred Pharmacy: ")

    patient = Patient(
        patient_id=None, mrn=mrn, ssn=ssn, first_name=first, last_name=last,
        dob=dob, gender=gender, phone=phone, email=email, address=addr,
        city=city, state=state, zip_code=zipcode, comm_pref=comm, pref_pharmacy=pharmacy
    )

    try:
        created = svc.create_patient(patient)
        print(f"\nPatient created with ID: {created.patient_id}")
    except Exception as e:
        print(f"Error creating patient: {e}")
    input("\nPress Enter...")


def update_patient(svc):
    print("\n--- Update Patient ---\n")
    pid = get_int("Patient ID: ")
    p = svc.get_patient_by_id(pid)

    if not p:
        print("Patient not found!")
        input("\nPress Enter...")
        return

    print(f"Updating {p.first_name} {p.last_name}")
    print("(press Enter to keep current value)\n")

    mrn = get_input(f"MRN [{p.mrn}]: ", False) or p.mrn
    ssn = get_input(f"SSN [{p.ssn}]: ", False) or p.ssn
    first = get_input(f"First Name [{p.first_name}]: ", False) or p.first_name
    last = get_input(f"Last Name [{p.last_name}]: ", False) or p.last_name
    dob_s = get_input(f"DOB [{p.dob}]: ", False)
    dob = date.fromisoformat(dob_s) if dob_s else p.dob
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
        print("Patient updated!")
    except Exception as e:
        print(f"Error: {e}")
    input("\nPress Enter...")


def delete_patient(svc):
    print("\n--- Delete Patient ---")
    pid = get_int("Patient ID: ")
    p = svc.get_patient_by_id(pid)

    if not p:
        print("Not found")
        input("\nPress Enter...")
        return

    confirm = input(f"Are you sure you want to delete {p.first_name} {p.last_name}? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.delete_patient(pid)
            print("Deleted successfully")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Cancelled")
    input("\nPress Enter...")


def search_patients(svc):
    print("\n--- Search Patients ---")
    term = get_input("Enter name to search: ")
    results = svc.search_patients_by_name(term)

    if not results:
        print("No patients found")
    else:
        print(f"\nFound {len(results)} patient(s):")
        for p in results:
            print(f"  {p.patient_id}: {p.first_name} {p.last_name} ({p.mrn})")
    input("\nPress Enter...")


def polypharmacy_report(svc):
    print("\n===== Polypharmacy Report =====\n")
    results = svc.get_polypharmacy_patients(5)

    if not results:
        print("No patients with 5+ active prescriptions")
    else:
        print("Patients with 5+ active prescriptions:\n")
        for p, count in results:
            print(f"  {p.first_name} {p.last_name}: {count} prescriptions")
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
        else: print("Invalid choice")


# appointment functions

def list_appointments(svc):
    print("\n------ All Appointments ------\n")
    appts = svc.get_all_appointments()

    if not appts:
        print("No appointments")
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
        print("Appointment not found")
        input("\nPress Enter...")
        return

    a = detail.appointment
    print(f"\nAppointment #{a.appt_id}")
    print(f"Date: {a.appt_date} at {a.appt_time}")
    print(f"Duration: {a.duration} minutes")
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
        print("No upcoming appointments")
    else:
        for d in appts:
            a = d.appointment
            pname = f"{d.patient.first_name} {d.patient.last_name}" if d.patient else "N/A"
            print(f"  {a.appt_date} {a.appt_time} - {pname} - {a.reason}")
    input("\nPress Enter...")


def schedule_appointment(svc):
    print("\n=== Schedule New Appointment ===\n")

    patient_id = get_int("Patient ID: ")
    provider_id = get_int("Provider ID: ")
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
        print(f"\nAppointment scheduled! ID: {created.appt_id}")
    except Exception as e:
        print(f"Failed to schedule: {e}")
    input("\nPress Enter...")


def cancel_appointment(svc):
    print("\n--- Cancel Appointment ---")
    aid = get_int("Appointment ID to cancel: ")

    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.cancel_appointment(aid)
            print("Appointment cancelled")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Not cancelled")
    input("\nPress Enter...")


def delete_appointment(svc):
    print("\n--- Delete Appointment ---")
    aid = get_int("Appointment ID: ")

    confirm = input("Confirm delete? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.delete_appointment(aid)
            print("Deleted")
        except Exception as e:
            print(f"Error: {e}")
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
        else: print("Invalid option")


# prescription stuff

def list_prescriptions(svc):
    print("\n------ All Prescriptions ------\n")
    rxs = svc.get_all_prescriptions()

    if not rxs:
        print("No prescriptions in system")
        input("\nPress Enter...")
        return

    print(f"{'ID':<5} {'Date':<12} {'Patient':<10} {'Dosage':<15} {'Status':<10}")
    print("-" * 55)
    for rx in rxs:
        print(f"{rx.rx_id:<5} {str(rx.date_written):<12} {rx.patient_id:<10} {rx.dosage:<15} {rx.status:<10}")
    print(f"\n{len(rxs)} prescription(s) total")
    input("\nPress Enter...")


def view_prescription(svc):
    print("\n--- Prescription Details ---")
    rid = get_int("Prescription ID: ")
    detail = svc.get_prescription_detail(rid)

    if not detail:
        print("Not found")
        input("\nPress Enter...")
        return

    rx = detail.prescription
    print(f"\nPrescription #{rx.rx_id}")
    print(f"Date Written: {rx.date_written}")
    print(f"Dosage: {rx.dosage}")
    print(f"Frequency: {rx.frequency}")
    print(f"Quantity: {rx.quantity}")
    print(f"Refills Remaining: {rx.refills}")
    print(f"Status: {rx.status}")
    print(f"Controlled Substance: {'Yes' if rx.is_controlled else 'No'}")

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
        print("No active prescriptions")
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
    refills = get_int("Number of Refills: ")

    is_controlled = input("Is this a controlled substance? (yes/no): ").lower() == 'yes'
    schedule = None
    dea = None
    if is_controlled:
        schedule = get_input("DEA Schedule (II/III/IV/V): ")
        dea = get_input("Prescriber DEA Number: ")

    rx = Prescription(
        rx_id=None, patient_id=patient_id, provider_id=provider_id, med_id=med_id,
        date_written=date_written, dosage=dosage, frequency=frequency,
        quantity=quantity, refills=refills, is_controlled=is_controlled,
        controlled_substance_schedule=schedule, prescriber_dea_number=dea, status='active'
    )

    try:
        created = svc.create_prescription(rx)
        print(f"\nPrescription created - ID: {created.rx_id}")
    except Exception as e:
        print(f"Error: {e}")
    input("\nPress Enter...")


def discontinue_prescription(svc):
    print("\n--- Discontinue Prescription ---")
    rid = get_int("Rx ID: ")

    confirm = input("Discontinue this prescription? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            svc.discontinue_prescription(rid)
            print("Prescription discontinued")
        except Exception as e:
            print(f"Error: {e}")
    input("\nPress Enter...")


def controlled_report(svc):
    print("\n===== CONTROLLED SUBSTANCES REPORT =====\n")
    rxs = svc.get_controlled_substances()

    if not rxs:
        print("No controlled substance prescriptions found")
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
        else: print("Invalid selection")


# main menu

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
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1': patient_menu(patient_svc)
        elif choice == '2': appointment_menu(appt_svc)
        elif choice == '3': prescription_menu(rx_svc)
        elif choice == '4': upcoming_appointments(appt_svc)
        elif choice == '5': active_prescriptions(rx_svc)
        elif choice == '6': polypharmacy_report(patient_svc)
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    finally:
        close_pool()
