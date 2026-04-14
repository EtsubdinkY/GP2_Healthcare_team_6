#!/usr/bin/env python3
"""
Healthcare Management System - Command Line Interface

A menu-driven CLI application for managing patients, appointments, and prescriptions.
"""

from __future__ import annotations

import sys
from datetime import date, time
from typing import Optional

from src.config.database import close_pool
from src.models import Patient, Appointment, Prescription
from src.services import (
    PatientService,
    AppointmentService,
    PrescriptionService,
)


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def clear_screen() -> None:
    """Clear terminal screen."""
    print('\033[2J\033[H', end='')


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 60}{Colors.ENDC}\n")


def print_success(message: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}[SUCCESS] {message}{Colors.ENDC}")


def print_error(message: str) -> None:
    """Print error message."""
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")


def print_warning(message: str) -> None:
    """Print warning message."""
    print(f"{Colors.WARNING}[WARNING] {message}{Colors.ENDC}")


def get_input(prompt: str, required: bool = True) -> str:
    """Get user input with optional validation."""
    while True:
        value = input(f"{Colors.CYAN}{prompt}{Colors.ENDC}").strip()
        if value or not required:
            return value
        print_error("This field is required. Please enter a value.")


def get_int_input(prompt: str, allow_empty: bool = False) -> Optional[int]:
    """Get integer input from user."""
    while True:
        value = input(f"{Colors.CYAN}{prompt}{Colors.ENDC}").strip()
        if not value and allow_empty:
            return None
        try:
            return int(value)
        except ValueError:
            print_error("Please enter a valid number.")


def get_date_input(prompt: str) -> date:
    """Get date input from user (YYYY-MM-DD format)."""
    while True:
        value = input(f"{Colors.CYAN}{prompt} (YYYY-MM-DD): {Colors.ENDC}").strip()
        try:
            return date.fromisoformat(value)
        except ValueError:
            print_error("Please enter a valid date in YYYY-MM-DD format.")


def get_time_input(prompt: str) -> time:
    """Get time input from user (HH:MM format)."""
    while True:
        value = input(f"{Colors.CYAN}{prompt} (HH:MM): {Colors.ENDC}").strip()
        try:
            parts = value.split(':')
            return time(int(parts[0]), int(parts[1]))
        except (ValueError, IndexError):
            print_error("Please enter a valid time in HH:MM format.")


def pause() -> None:
    """Pause and wait for user to press Enter."""
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")


# =============================================================================
# PATIENT MANAGEMENT
# =============================================================================

def patient_menu(service: PatientService) -> None:
    """Patient management submenu."""
    while True:
        print_header("PATIENT MANAGEMENT")
        print("1. List All Patients")
        print("2. View Patient Details")
        print("3. View Patient Dashboard")
        print("4. Add New Patient")
        print("5. Update Patient")
        print("6. Delete Patient")
        print("7. Search Patients")
        print("8. Polypharmacy Report")
        print("0. Back to Main Menu")

        choice = get_input("\nEnter your choice: ")

        if choice == '1':
            list_patients(service)
        elif choice == '2':
            view_patient(service)
        elif choice == '3':
            view_patient_dashboard(service)
        elif choice == '4':
            add_patient(service)
        elif choice == '5':
            update_patient(service)
        elif choice == '6':
            delete_patient(service)
        elif choice == '7':
            search_patients(service)
        elif choice == '8':
            polypharmacy_report(service)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice. Please try again.")


def list_patients(service: PatientService) -> None:
    """List all patients."""
    print_header("ALL PATIENTS")
    patients = service.get_all_patients()

    if not patients:
        print_warning("No patients found.")
    else:
        print(f"{'ID':<6} {'MRN':<12} {'Name':<25} {'DOB':<12} {'Phone':<15}")
        print("-" * 70)
        for p in patients:
            print(f"{p.patient_id:<6} {p.mrn:<12} {p.first_name + ' ' + p.last_name:<25} {str(p.dob):<12} {p.phone or 'N/A':<15}")

    print(f"\nTotal: {len(patients)} patient(s)")
    pause()


def view_patient(service: PatientService) -> None:
    """View patient details."""
    print_header("VIEW PATIENT")
    patient_id = get_int_input("Enter Patient ID: ")
    patient = service.get_patient_by_id(patient_id)

    if patient is None:
        print_error(f"Patient with ID {patient_id} not found.")
    else:
        print(f"\n{Colors.BOLD}Patient Information:{Colors.ENDC}")
        print(f"  ID:            {patient.patient_id}")
        print(f"  MRN:           {patient.mrn}")
        print(f"  Name:          {patient.first_name} {patient.last_name}")
        print(f"  DOB:           {patient.dob}")
        print(f"  Gender:        {patient.gender}")
        print(f"  Phone:         {patient.phone or 'N/A'}")
        print(f"  Email:         {patient.email or 'N/A'}")
        print(f"  Address:       {patient.address}")
        print(f"  City/State:    {patient.city}, {patient.state} {patient.zip_code}")
        print(f"  Comm Pref:     {patient.comm_pref}")
        print(f"  Pharmacy:      {patient.pref_pharmacy}")

    pause()


def view_patient_dashboard(service: PatientService) -> None:
    """View comprehensive patient dashboard."""
    print_header("PATIENT DASHBOARD")
    patient_id = get_int_input("Enter Patient ID: ")
    dashboard = service.get_patient_dashboard(patient_id)

    if dashboard is None:
        print_error(f"Patient with ID {patient_id} not found.")
    else:
        p = dashboard.patient
        print(f"\n{Colors.BOLD}=== PATIENT: {p.first_name} {p.last_name} (MRN: {p.mrn}) ==={Colors.ENDC}")
        print(f"DOB: {p.dob} | Gender: {p.gender} | Phone: {p.phone or 'N/A'}")

        print(f"\n{Colors.BOLD}--- Insurance Coverage ---{Colors.ENDC}")
        if dashboard.insurance_coverage:
            for ins in dashboard.insurance_coverage:
                end = ins.end_date or "Active"
                print(f"  - Policy #{ins.policy_number} | Type: {ins.coverage_type} | Copay: ${ins.copay} | Until: {end}")
        else:
            print("  No active insurance coverage.")

        print(f"\n{Colors.BOLD}--- Active Prescriptions ---{Colors.ENDC}")
        if dashboard.active_prescriptions:
            for rx in dashboard.active_prescriptions:
                print(f"  - Rx #{rx.rx_id}: {rx.dosage} | {rx.frequency} | Refills: {rx.refills}")
        else:
            print("  No active prescriptions.")

        print(f"\n{Colors.BOLD}--- Upcoming Appointments ---{Colors.ENDC}")
        if dashboard.upcoming_appointments:
            for appt in dashboard.upcoming_appointments:
                print(f"  - {appt.appt_date} at {appt.appt_time} | {appt.appt_type} | {appt.reason}")
        else:
            print("  No upcoming appointments.")

    pause()


def add_patient(service: PatientService) -> None:
    """Add a new patient."""
    print_header("ADD NEW PATIENT")

    mrn = get_input("MRN (10 digits): ")
    ssn = get_input("SSN (optional): ", required=False) or None
    first_name = get_input("First Name: ")
    last_name = get_input("Last Name: ")
    dob = get_date_input("Date of Birth")
    gender = get_input("Gender (male/female/other): ")
    phone = get_input("Phone (optional): ", required=False) or None
    email = get_input("Email (optional): ", required=False) or None
    address = get_input("Address: ")
    city = get_input("City: ")
    state = get_input("State: ")
    zip_code = get_input("ZIP Code: ")
    comm_pref = get_input("Communication Preference (email/phone/mail): ")
    pref_pharmacy = get_input("Preferred Pharmacy: ")

    patient = Patient(
        patient_id=None,
        mrn=mrn,
        ssn=ssn,
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        gender=gender,
        phone=phone,
        email=email,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        comm_pref=comm_pref,
        pref_pharmacy=pref_pharmacy,
    )

    try:
        created = service.create_patient(patient)
        print_success(f"Patient created with ID: {created.patient_id}")
    except Exception as e:
        print_error(f"Failed to create patient: {e}")

    pause()


def update_patient(service: PatientService) -> None:
    """Update an existing patient."""
    print_header("UPDATE PATIENT")
    patient_id = get_int_input("Enter Patient ID to update: ")
    existing = service.get_patient_by_id(patient_id)

    if existing is None:
        print_error(f"Patient with ID {patient_id} not found.")
        pause()
        return

    print(f"\nUpdating: {existing.first_name} {existing.last_name}")
    print("(Press Enter to keep current value)\n")

    mrn = get_input(f"MRN [{existing.mrn}]: ", required=False) or existing.mrn
    ssn = get_input(f"SSN [{existing.ssn or 'N/A'}]: ", required=False) or existing.ssn
    first_name = get_input(f"First Name [{existing.first_name}]: ", required=False) or existing.first_name
    last_name = get_input(f"Last Name [{existing.last_name}]: ", required=False) or existing.last_name
    dob_str = get_input(f"DOB [{existing.dob}]: ", required=False)
    dob = date.fromisoformat(dob_str) if dob_str else existing.dob
    gender = get_input(f"Gender [{existing.gender}]: ", required=False) or existing.gender
    phone = get_input(f"Phone [{existing.phone or 'N/A'}]: ", required=False) or existing.phone
    email = get_input(f"Email [{existing.email or 'N/A'}]: ", required=False) or existing.email
    address = get_input(f"Address [{existing.address}]: ", required=False) or existing.address
    city = get_input(f"City [{existing.city}]: ", required=False) or existing.city
    state = get_input(f"State [{existing.state}]: ", required=False) or existing.state
    zip_code = get_input(f"ZIP [{existing.zip_code}]: ", required=False) or existing.zip_code
    comm_pref = get_input(f"Comm Pref [{existing.comm_pref}]: ", required=False) or existing.comm_pref
    pref_pharmacy = get_input(f"Pharmacy [{existing.pref_pharmacy}]: ", required=False) or existing.pref_pharmacy

    patient = Patient(
        patient_id=patient_id,
        mrn=mrn,
        ssn=ssn,
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        gender=gender,
        phone=phone,
        email=email,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        comm_pref=comm_pref,
        pref_pharmacy=pref_pharmacy,
    )

    try:
        updated = service.update_patient(patient_id, patient)
        if updated:
            print_success("Patient updated successfully.")
        else:
            print_error("Failed to update patient.")
    except Exception as e:
        print_error(f"Failed to update patient: {e}")

    pause()


def delete_patient(service: PatientService) -> None:
    """Delete a patient."""
    print_header("DELETE PATIENT")
    patient_id = get_int_input("Enter Patient ID to delete: ")
    existing = service.get_patient_by_id(patient_id)

    if existing is None:
        print_error(f"Patient with ID {patient_id} not found.")
        pause()
        return

    print(f"\nPatient: {existing.first_name} {existing.last_name} (MRN: {existing.mrn})")
    confirm = get_input("Are you sure you want to delete this patient? (yes/no): ")

    if confirm.lower() == 'yes':
        try:
            if service.delete_patient(patient_id):
                print_success("Patient deleted successfully.")
            else:
                print_error("Failed to delete patient.")
        except Exception as e:
            print_error(f"Failed to delete patient: {e}")
    else:
        print_warning("Deletion cancelled.")

    pause()


def search_patients(service: PatientService) -> None:
    """Search patients by name."""
    print_header("SEARCH PATIENTS")
    search_term = get_input("Enter name to search: ")
    patients = service.search_patients_by_name(search_term)

    if not patients:
        print_warning(f"No patients found matching '{search_term}'.")
    else:
        print(f"\n{'ID':<6} {'MRN':<12} {'Name':<25} {'DOB':<12}")
        print("-" * 55)
        for p in patients:
            print(f"{p.patient_id:<6} {p.mrn:<12} {p.first_name + ' ' + p.last_name:<25} {str(p.dob):<12}")

    print(f"\nFound: {len(patients)} patient(s)")
    pause()


def polypharmacy_report(service: PatientService) -> None:
    """Show patients with polypharmacy risk."""
    print_header("POLYPHARMACY RISK REPORT")
    print("Patients with 5+ active prescriptions:\n")

    results = service.get_polypharmacy_patients(threshold=5)

    if not results:
        print_warning("No patients with polypharmacy risk found.")
    else:
        print(f"{'ID':<6} {'Name':<25} {'MRN':<12} {'Active Rx Count':<15}")
        print("-" * 60)
        for patient, count in results:
            print(f"{patient.patient_id:<6} {patient.first_name + ' ' + patient.last_name:<25} {patient.mrn:<12} {count:<15}")

    print(f"\nTotal at-risk patients: {len(results)}")
    pause()


# =============================================================================
# APPOINTMENT MANAGEMENT
# =============================================================================

def appointment_menu(service: AppointmentService) -> None:
    """Appointment management submenu."""
    while True:
        print_header("APPOINTMENT MANAGEMENT")
        print("1. List All Appointments")
        print("2. View Appointment Details")
        print("3. View Upcoming Appointments")
        print("4. Schedule New Appointment")
        print("5. Update Appointment")
        print("6. Cancel Appointment")
        print("7. Delete Appointment")
        print("8. View Appointments by Date")
        print("0. Back to Main Menu")

        choice = get_input("\nEnter your choice: ")

        if choice == '1':
            list_appointments(service)
        elif choice == '2':
            view_appointment(service)
        elif choice == '3':
            view_upcoming_appointments(service)
        elif choice == '4':
            schedule_appointment(service)
        elif choice == '5':
            update_appointment(service)
        elif choice == '6':
            cancel_appointment(service)
        elif choice == '7':
            delete_appointment(service)
        elif choice == '8':
            view_appointments_by_date(service)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice. Please try again.")


def list_appointments(service: AppointmentService) -> None:
    """List all appointments."""
    print_header("ALL APPOINTMENTS")
    appointments = service.get_all_appointments()

    if not appointments:
        print_warning("No appointments found.")
    else:
        print(f"{'ID':<6} {'Date':<12} {'Time':<8} {'Patient ID':<12} {'Status':<12} {'Type':<15}")
        print("-" * 70)
        for a in appointments:
            print(f"{a.appt_id:<6} {str(a.appt_date):<12} {str(a.appt_time)[:5]:<8} {a.patient_id:<12} {a.status:<12} {a.appt_type:<15}")

    print(f"\nTotal: {len(appointments)} appointment(s)")
    pause()


def view_appointment(service: AppointmentService) -> None:
    """View appointment details."""
    print_header("VIEW APPOINTMENT")
    appt_id = get_int_input("Enter Appointment ID: ")
    detail = service.get_appointment_detail(appt_id)

    if detail is None:
        print_error(f"Appointment with ID {appt_id} not found.")
    else:
        a = detail.appointment
        print(f"\n{Colors.BOLD}Appointment Information:{Colors.ENDC}")
        print(f"  ID:          {a.appt_id}")
        print(f"  Date:        {a.appt_date}")
        print(f"  Time:        {a.appt_time}")
        print(f"  Duration:    {a.duration} minutes")
        print(f"  Status:      {a.status}")
        print(f"  Type:        {a.appt_type}")
        print(f"  Reason:      {a.reason}")
        print(f"  Notes:       {a.notes or 'N/A'}")

        if detail.patient:
            print(f"\n{Colors.BOLD}Patient:{Colors.ENDC}")
            print(f"  {detail.patient.first_name} {detail.patient.last_name} (MRN: {detail.patient.mrn})")

        if detail.provider:
            print(f"\n{Colors.BOLD}Provider:{Colors.ENDC}")
            print(f"  Dr. {detail.provider.first_name} {detail.provider.last_name} ({detail.provider.speciality})")

    pause()


def view_upcoming_appointments(service: AppointmentService) -> None:
    """View upcoming scheduled appointments."""
    print_header("UPCOMING APPOINTMENTS")
    appointments = service.get_upcoming_appointments()

    if not appointments:
        print_warning("No upcoming appointments.")
    else:
        print(f"{'Date':<12} {'Time':<8} {'Patient':<25} {'Provider':<25} {'Type':<15}")
        print("-" * 90)
        for detail in appointments:
            a = detail.appointment
            patient_name = f"{detail.patient.first_name} {detail.patient.last_name}" if detail.patient else "N/A"
            provider_name = f"Dr. {detail.provider.last_name}" if detail.provider else "N/A"
            print(f"{str(a.appt_date):<12} {str(a.appt_time)[:5]:<8} {patient_name:<25} {provider_name:<25} {a.appt_type:<15}")

    print(f"\nTotal: {len(appointments)} upcoming appointment(s)")
    pause()


def schedule_appointment(service: AppointmentService) -> None:
    """Schedule a new appointment."""
    print_header("SCHEDULE NEW APPOINTMENT")

    patient_id = get_int_input("Patient ID: ")
    provider_id = get_int_input("Provider ID: ")
    appt_date = get_date_input("Appointment Date")
    appt_time = get_time_input("Appointment Time")
    duration = get_int_input("Duration (minutes): ") or 30
    appt_type = get_input("Appointment Type (routine/followup/urgent/new_patient): ")
    reason = get_input("Reason for Visit: ")
    notes = get_input("Notes (optional): ", required=False) or None

    appointment = Appointment(
        appt_id=None,
        patient_id=patient_id,
        provider_id=provider_id,
        appt_date=appt_date,
        appt_time=appt_time,
        duration=duration,
        status='scheduled',
        appt_type=appt_type,
        reason=reason,
        notes=notes,
    )

    try:
        created = service.create_appointment(appointment)
        print_success(f"Appointment scheduled with ID: {created.appt_id}")
    except Exception as e:
        print_error(f"Failed to schedule appointment: {e}")

    pause()


def update_appointment(service: AppointmentService) -> None:
    """Update an existing appointment."""
    print_header("UPDATE APPOINTMENT")
    appt_id = get_int_input("Enter Appointment ID to update: ")
    existing = service.get_appointment_by_id(appt_id)

    if existing is None:
        print_error(f"Appointment with ID {appt_id} not found.")
        pause()
        return

    print(f"\nUpdating appointment on {existing.appt_date} at {existing.appt_time}")
    print("(Press Enter to keep current value)\n")

    patient_id_str = get_input(f"Patient ID [{existing.patient_id}]: ", required=False)
    patient_id = int(patient_id_str) if patient_id_str else existing.patient_id

    provider_id_str = get_input(f"Provider ID [{existing.provider_id}]: ", required=False)
    provider_id = int(provider_id_str) if provider_id_str else existing.provider_id

    date_str = get_input(f"Date [{existing.appt_date}]: ", required=False)
    appt_date = date.fromisoformat(date_str) if date_str else existing.appt_date

    time_str = get_input(f"Time [{existing.appt_time}]: ", required=False)
    if time_str:
        parts = time_str.split(':')
        appt_time = time(int(parts[0]), int(parts[1]))
    else:
        appt_time = existing.appt_time

    duration_str = get_input(f"Duration [{existing.duration}]: ", required=False)
    duration = int(duration_str) if duration_str else existing.duration

    status = get_input(f"Status [{existing.status}]: ", required=False) or existing.status
    appt_type = get_input(f"Type [{existing.appt_type}]: ", required=False) or existing.appt_type
    reason = get_input(f"Reason [{existing.reason}]: ", required=False) or existing.reason
    notes = get_input(f"Notes [{existing.notes or 'N/A'}]: ", required=False) or existing.notes

    appointment = Appointment(
        appt_id=appt_id,
        patient_id=patient_id,
        provider_id=provider_id,
        appt_date=appt_date,
        appt_time=appt_time,
        duration=duration,
        status=status,
        appt_type=appt_type,
        reason=reason,
        notes=notes,
    )

    try:
        updated = service.update_appointment(appt_id, appointment)
        if updated:
            print_success("Appointment updated successfully.")
        else:
            print_error("Failed to update appointment.")
    except Exception as e:
        print_error(f"Failed to update appointment: {e}")

    pause()


def cancel_appointment(service: AppointmentService) -> None:
    """Cancel an appointment."""
    print_header("CANCEL APPOINTMENT")
    appt_id = get_int_input("Enter Appointment ID to cancel: ")
    existing = service.get_appointment_by_id(appt_id)

    if existing is None:
        print_error(f"Appointment with ID {appt_id} not found.")
        pause()
        return

    print(f"\nAppointment: {existing.appt_date} at {existing.appt_time} - {existing.reason}")
    confirm = get_input("Are you sure you want to cancel? (yes/no): ")

    if confirm.lower() == 'yes':
        try:
            cancelled = service.cancel_appointment(appt_id)
            if cancelled:
                print_success("Appointment cancelled successfully.")
            else:
                print_error("Failed to cancel appointment.")
        except Exception as e:
            print_error(f"Failed to cancel appointment: {e}")
    else:
        print_warning("Cancellation aborted.")

    pause()


def delete_appointment(service: AppointmentService) -> None:
    """Delete an appointment."""
    print_header("DELETE APPOINTMENT")
    appt_id = get_int_input("Enter Appointment ID to delete: ")
    existing = service.get_appointment_by_id(appt_id)

    if existing is None:
        print_error(f"Appointment with ID {appt_id} not found.")
        pause()
        return

    print(f"\nAppointment: {existing.appt_date} at {existing.appt_time}")
    confirm = get_input("Are you sure you want to permanently delete? (yes/no): ")

    if confirm.lower() == 'yes':
        try:
            if service.delete_appointment(appt_id):
                print_success("Appointment deleted successfully.")
            else:
                print_error("Failed to delete appointment.")
        except Exception as e:
            print_error(f"Failed to delete appointment: {e}")
    else:
        print_warning("Deletion cancelled.")

    pause()


def view_appointments_by_date(service: AppointmentService) -> None:
    """View appointments for a specific date."""
    print_header("APPOINTMENTS BY DATE")
    target_date = get_date_input("Enter date")
    appointments = service.get_appointments_by_date(target_date)

    print(f"\nAppointments for {target_date}:\n")

    if not appointments:
        print_warning("No appointments found for this date.")
    else:
        print(f"{'Time':<8} {'Patient':<25} {'Provider':<25} {'Type':<12} {'Status':<12}")
        print("-" * 85)
        for detail in appointments:
            a = detail.appointment
            patient_name = f"{detail.patient.first_name} {detail.patient.last_name}" if detail.patient else "N/A"
            provider_name = f"Dr. {detail.provider.last_name}" if detail.provider else "N/A"
            print(f"{str(a.appt_time)[:5]:<8} {patient_name:<25} {provider_name:<25} {a.appt_type:<12} {a.status:<12}")

    print(f"\nTotal: {len(appointments)} appointment(s)")
    pause()


# =============================================================================
# PRESCRIPTION MANAGEMENT
# =============================================================================

def prescription_menu(service: PrescriptionService) -> None:
    """Prescription management submenu."""
    while True:
        print_header("PRESCRIPTION MANAGEMENT")
        print("1. List All Prescriptions")
        print("2. View Prescription Details")
        print("3. View Active Prescriptions")
        print("4. Create New Prescription")
        print("5. Update Prescription")
        print("6. Discontinue Prescription")
        print("7. Delete Prescription")
        print("8. View Patient Prescriptions")
        print("9. Controlled Substances Report")
        print("0. Back to Main Menu")

        choice = get_input("\nEnter your choice: ")

        if choice == '1':
            list_prescriptions(service)
        elif choice == '2':
            view_prescription(service)
        elif choice == '3':
            view_active_prescriptions(service)
        elif choice == '4':
            create_prescription(service)
        elif choice == '5':
            update_prescription(service)
        elif choice == '6':
            discontinue_prescription(service)
        elif choice == '7':
            delete_prescription(service)
        elif choice == '8':
            view_patient_prescriptions(service)
        elif choice == '9':
            controlled_substances_report(service)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice. Please try again.")


def list_prescriptions(service: PrescriptionService) -> None:
    """List all prescriptions."""
    print_header("ALL PRESCRIPTIONS")
    prescriptions = service.get_all_prescriptions()

    if not prescriptions:
        print_warning("No prescriptions found.")
    else:
        print(f"{'ID':<6} {'Date':<12} {'Patient ID':<12} {'Dosage':<20} {'Status':<12} {'Controlled':<10}")
        print("-" * 80)
        for rx in prescriptions:
            controlled = "Yes" if rx.is_controlled else "No"
            print(f"{rx.rx_id:<6} {str(rx.date_written):<12} {rx.patient_id:<12} {rx.dosage[:18]:<20} {rx.status:<12} {controlled:<10}")

    print(f"\nTotal: {len(prescriptions)} prescription(s)")
    pause()


def view_prescription(service: PrescriptionService) -> None:
    """View prescription details."""
    print_header("VIEW PRESCRIPTION")
    rx_id = get_int_input("Enter Prescription ID: ")
    detail = service.get_prescription_detail(rx_id)

    if detail is None:
        print_error(f"Prescription with ID {rx_id} not found.")
    else:
        rx = detail.prescription
        print(f"\n{Colors.BOLD}Prescription Information:{Colors.ENDC}")
        print(f"  ID:            {rx.rx_id}")
        print(f"  Date Written:  {rx.date_written}")
        print(f"  Dosage:        {rx.dosage}")
        print(f"  Frequency:     {rx.frequency}")
        print(f"  Quantity:      {rx.quantity}")
        print(f"  Refills:       {rx.refills}")
        print(f"  Status:        {rx.status}")
        print(f"  Controlled:    {'Yes' if rx.is_controlled else 'No'}")
        if rx.is_controlled:
            print(f"  Schedule:      {rx.controlled_substance_schedule}")
            print(f"  DEA Number:    {rx.prescriber_dea_number}")

        if detail.medication:
            print(f"\n{Colors.BOLD}Medication:{Colors.ENDC}")
            print(f"  {detail.medication.name} ({detail.medication.generic_name})")
            print(f"  Class: {detail.medication.drug_class} | Form: {detail.medication.form}")

        if detail.patient:
            print(f"\n{Colors.BOLD}Patient:{Colors.ENDC}")
            print(f"  {detail.patient.first_name} {detail.patient.last_name} (MRN: {detail.patient.mrn})")

        if detail.provider:
            print(f"\n{Colors.BOLD}Prescriber:{Colors.ENDC}")
            print(f"  Dr. {detail.provider.first_name} {detail.provider.last_name} (NPI: {detail.provider.npi})")

    pause()


def view_active_prescriptions(service: PrescriptionService) -> None:
    """View all active prescriptions."""
    print_header("ACTIVE PRESCRIPTIONS")
    prescriptions = service.get_active_prescriptions()

    if not prescriptions:
        print_warning("No active prescriptions found.")
    else:
        print(f"{'ID':<6} {'Medication':<25} {'Patient':<25} {'Dosage':<20} {'Refills':<8}")
        print("-" * 90)
        for detail in prescriptions:
            rx = detail.prescription
            med_name = detail.medication.name[:23] if detail.medication else "N/A"
            patient_name = f"{detail.patient.first_name} {detail.patient.last_name}" if detail.patient else "N/A"
            print(f"{rx.rx_id:<6} {med_name:<25} {patient_name:<25} {rx.dosage[:18]:<20} {rx.refills:<8}")

    print(f"\nTotal: {len(prescriptions)} active prescription(s)")
    pause()


def create_prescription(service: PrescriptionService) -> None:
    """Create a new prescription."""
    print_header("CREATE NEW PRESCRIPTION")

    patient_id = get_int_input("Patient ID: ")
    provider_id = get_int_input("Provider ID: ")
    med_id = get_int_input("Medication ID: ")
    date_written = get_date_input("Date Written")
    dosage = get_input("Dosage: ")
    frequency = get_input("Frequency: ")
    quantity = get_int_input("Quantity: ")
    refills = get_int_input("Number of Refills: ")

    is_controlled_str = get_input("Is this a controlled substance? (yes/no): ")
    is_controlled = is_controlled_str.lower() == 'yes'

    controlled_schedule = None
    dea_number = None
    if is_controlled:
        controlled_schedule = get_input("Schedule (I/II/III/IV/V): ")
        dea_number = get_input("Prescriber DEA Number: ")

    prescription = Prescription(
        rx_id=None,
        patient_id=patient_id,
        provider_id=provider_id,
        med_id=med_id,
        date_written=date_written,
        dosage=dosage,
        frequency=frequency,
        quantity=quantity,
        refills=refills,
        is_controlled=is_controlled,
        controlled_substance_schedule=controlled_schedule,
        prescriber_dea_number=dea_number,
        status='active',
    )

    try:
        created = service.create_prescription(prescription)
        print_success(f"Prescription created with ID: {created.rx_id}")
    except Exception as e:
        print_error(f"Failed to create prescription: {e}")

    pause()


def update_prescription(service: PrescriptionService) -> None:
    """Update an existing prescription."""
    print_header("UPDATE PRESCRIPTION")
    rx_id = get_int_input("Enter Prescription ID to update: ")
    existing = service.get_prescription_by_id(rx_id)

    if existing is None:
        print_error(f"Prescription with ID {rx_id} not found.")
        pause()
        return

    print(f"\nUpdating prescription from {existing.date_written}")
    print("(Press Enter to keep current value)\n")

    patient_id_str = get_input(f"Patient ID [{existing.patient_id}]: ", required=False)
    patient_id = int(patient_id_str) if patient_id_str else existing.patient_id

    provider_id_str = get_input(f"Provider ID [{existing.provider_id}]: ", required=False)
    provider_id = int(provider_id_str) if provider_id_str else existing.provider_id

    med_id_str = get_input(f"Medication ID [{existing.med_id}]: ", required=False)
    med_id = int(med_id_str) if med_id_str else existing.med_id

    date_str = get_input(f"Date Written [{existing.date_written}]: ", required=False)
    date_written = date.fromisoformat(date_str) if date_str else existing.date_written

    dosage = get_input(f"Dosage [{existing.dosage}]: ", required=False) or existing.dosage
    frequency = get_input(f"Frequency [{existing.frequency}]: ", required=False) or existing.frequency

    quantity_str = get_input(f"Quantity [{existing.quantity}]: ", required=False)
    quantity = int(quantity_str) if quantity_str else existing.quantity

    refills_str = get_input(f"Refills [{existing.refills}]: ", required=False)
    refills = int(refills_str) if refills_str else existing.refills

    status = get_input(f"Status [{existing.status}]: ", required=False) or existing.status

    prescription = Prescription(
        rx_id=rx_id,
        patient_id=patient_id,
        provider_id=provider_id,
        med_id=med_id,
        date_written=date_written,
        dosage=dosage,
        frequency=frequency,
        quantity=quantity,
        refills=refills,
        is_controlled=existing.is_controlled,
        controlled_substance_schedule=existing.controlled_substance_schedule,
        prescriber_dea_number=existing.prescriber_dea_number,
        status=status,
    )

    try:
        updated = service.update_prescription(rx_id, prescription)
        if updated:
            print_success("Prescription updated successfully.")
        else:
            print_error("Failed to update prescription.")
    except Exception as e:
        print_error(f"Failed to update prescription: {e}")

    pause()


def discontinue_prescription(service: PrescriptionService) -> None:
    """Discontinue a prescription."""
    print_header("DISCONTINUE PRESCRIPTION")
    rx_id = get_int_input("Enter Prescription ID to discontinue: ")
    existing = service.get_prescription_by_id(rx_id)

    if existing is None:
        print_error(f"Prescription with ID {rx_id} not found.")
        pause()
        return

    print(f"\nPrescription: {existing.dosage} - {existing.frequency}")
    confirm = get_input("Are you sure you want to discontinue? (yes/no): ")

    if confirm.lower() == 'yes':
        try:
            discontinued = service.discontinue_prescription(rx_id)
            if discontinued:
                print_success("Prescription discontinued successfully.")
            else:
                print_error("Failed to discontinue prescription.")
        except Exception as e:
            print_error(f"Failed to discontinue prescription: {e}")
    else:
        print_warning("Action cancelled.")

    pause()


def delete_prescription(service: PrescriptionService) -> None:
    """Delete a prescription."""
    print_header("DELETE PRESCRIPTION")
    rx_id = get_int_input("Enter Prescription ID to delete: ")
    existing = service.get_prescription_by_id(rx_id)

    if existing is None:
        print_error(f"Prescription with ID {rx_id} not found.")
        pause()
        return

    print(f"\nPrescription: {existing.dosage} - Status: {existing.status}")
    confirm = get_input("Are you sure you want to permanently delete? (yes/no): ")

    if confirm.lower() == 'yes':
        try:
            if service.delete_prescription(rx_id):
                print_success("Prescription deleted successfully.")
            else:
                print_error("Failed to delete prescription.")
        except Exception as e:
            print_error(f"Failed to delete prescription: {e}")
    else:
        print_warning("Deletion cancelled.")

    pause()


def view_patient_prescriptions(service: PrescriptionService) -> None:
    """View all prescriptions for a patient."""
    print_header("PATIENT PRESCRIPTIONS")
    patient_id = get_int_input("Enter Patient ID: ")
    prescriptions = service.get_patient_prescriptions(patient_id)

    if not prescriptions:
        print_warning(f"No prescriptions found for patient ID {patient_id}.")
    else:
        if prescriptions[0].patient:
            p = prescriptions[0].patient
            print(f"Patient: {p.first_name} {p.last_name} (MRN: {p.mrn})\n")

        print(f"{'ID':<6} {'Date':<12} {'Medication':<25} {'Dosage':<20} {'Status':<12}")
        print("-" * 80)
        for detail in prescriptions:
            rx = detail.prescription
            med_name = detail.medication.name[:23] if detail.medication else "N/A"
            print(f"{rx.rx_id:<6} {str(rx.date_written):<12} {med_name:<25} {rx.dosage[:18]:<20} {rx.status:<12}")

    print(f"\nTotal: {len(prescriptions)} prescription(s)")
    pause()


def controlled_substances_report(service: PrescriptionService) -> None:
    """Show controlled substances report for DEA compliance."""
    print_header("CONTROLLED SUBSTANCES REPORT")
    print("DEA Compliance Report - All Controlled Substance Prescriptions\n")

    prescriptions = service.get_controlled_substances()

    if not prescriptions:
        print_warning("No controlled substance prescriptions found.")
    else:
        print(f"{'ID':<6} {'Schedule':<10} {'Patient':<20} {'Prescriber':<20} {'DEA#':<15} {'Date':<12}")
        print("-" * 90)
        for detail in prescriptions:
            rx = detail.prescription
            patient_name = f"{detail.patient.last_name}" if detail.patient else "N/A"
            prescriber_name = f"Dr. {detail.provider.last_name}" if detail.provider else "N/A"
            schedule = rx.controlled_substance_schedule or "N/A"
            dea = rx.prescriber_dea_number or "N/A"
            print(f"{rx.rx_id:<6} {schedule:<10} {patient_name:<20} {prescriber_name:<20} {dea:<15} {str(rx.date_written):<12}")

    print(f"\nTotal controlled substance prescriptions: {len(prescriptions)}")
    pause()


# =============================================================================
# MAIN MENU
# =============================================================================

def main_menu() -> None:
    """Main application menu."""
    patient_service = PatientService()
    appointment_service = AppointmentService()
    prescription_service = PrescriptionService()

    while True:
        print_header("HEALTHCARE MANAGEMENT SYSTEM")
        print("1. Patient Management")
        print("2. Appointment Management")
        print("3. Prescription Management")
        print("4. Quick View: Upcoming Appointments")
        print("5. Quick View: Active Prescriptions")
        print("6. Quick View: Polypharmacy Risk")
        print("0. Exit")

        choice = get_input("\nEnter your choice: ")

        if choice == '1':
            patient_menu(patient_service)
        elif choice == '2':
            appointment_menu(appointment_service)
        elif choice == '3':
            prescription_menu(prescription_service)
        elif choice == '4':
            view_upcoming_appointments(appointment_service)
        elif choice == '5':
            view_active_prescriptions(prescription_service)
        elif choice == '6':
            polypharmacy_report(patient_service)
        elif choice == '0':
            print_success("Thank you for using Healthcare Management System. Goodbye!")
            break
        else:
            print_error("Invalid choice. Please try again.")


def main() -> None:
    """Application entry point."""
    try:
        print("\nInitializing Healthcare Management System...")
        main_menu()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
    finally:
        close_pool()
        print("Database connections closed.")


if __name__ == "__main__":
    main()
