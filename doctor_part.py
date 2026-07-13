# Load appointment data from file
def load_appointments():
    appointments = []

    try:
        with open("appointments.txt", "r") as f:
            for line in f:
                data = line.strip().split("|")

                # skip bad lines
                if len(data) != 6:
                    continue

                appointment = {
                    "appointment_id": data[0].strip().upper(),
                    "patient_id": data[1].strip().upper(),
                    "doctor_id": data[2].strip().upper(),
                    "date": data[3].strip(),
                    "time": data[4].strip(),
                    "status": data[5].strip()
                }

                appointments.append(appointment)

    except FileNotFoundError:
        # default data
        appointments = [
            {"appointment_id": "A001", "patient_id": "P001", "doctor_id": "D001",
             "date": "30/03/2026", "time": "10:00AM", "status": "Scheduled"},
            {"appointment_id": "A002", "patient_id": "P002", "doctor_id": "D001",
             "date": "30/03/2026", "time": "11:00AM", "status": "Scheduled"},
            {"appointment_id": "A003", "patient_id": "P003", "doctor_id": "D002",
             "date": "31/03/2026", "time": "10:30AM", "status": "Scheduled"}
        ]

    return appointments


# Save appointment to file
def save_appointments(appointments):
    with open("appointments.txt", "w") as f:
        for i in appointments:
            f.write(
                i["appointment_id"] + "|" +
                i["patient_id"] + "|" +
                i["doctor_id"] + "|" +
                i["date"] + "|" +
                i["time"] + "|" +
                i["status"] + "\n"
            )


# Load consultation file
def load_consultations():
    consultations = []

    try:
        with open("consultations.txt", "r") as f:
            for line in f:
                data = line.strip().split("|")

                if len(data) != 5:
                    continue

                consultation = {
                    "appointment_id": data[0].strip().upper(),
                    "patient_id": data[1].strip().upper(),
                    "doctor_id": data[2].strip().upper(),
                    "diagnosis": data[3].strip(),
                    "treatment": data[4].strip()
                }

                consultations.append(consultation)

    except FileNotFoundError:
        pass

    return consultations


# Save consultation file
def save_consultations(consultations):
    with open("consultations.txt", "w") as f:
        for c in consultations:
            f.write(
                c["appointment_id"] + "|" +
                c["patient_id"] + "|" +
                c["doctor_id"] + "|" +
                c["diagnosis"] + "|" +
                c["treatment"] + "\n"
            )


# Doctor Menu
def doctor_menu():
    appointments = load_appointments()
    consultations = load_consultations()

    # View appointment
    def view_appointment():

        doctor_id = input("Enter doctor id:\n").strip().upper()

        found = False

        for i in appointments:
            if i["doctor_id"] == doctor_id:
                print(
                    f"ID:{i['appointment_id']} | "
                    f"Patient ID:{i['patient_id']} | "
                    f"Date:{i['date']} | "
                    f"Time:{i['time']} | "
                    f"Status:{i['status']}"
                )

                found = True

        if not found:
            print("No appointment found")

    # Record consultation
    def record_consultation():

        appointment_id = input("Enter appointment id:\n").strip().upper()

        # check if appointment exists
        exists = False
        for i in appointments:
            if i["appointment_id"] == appointment_id:
                exists = True
                break

        if not exists:
            print("Appointment ID not found")
            return

        for c in consultations:
            if c["appointment_id"] == appointment_id:
                print("Consultation already exists for this appointment")
                return

        diagnosis = input("Enter diagnosis:\n")
        treatment = input("Enter treatment:\n")

        patient_id = ""
        doctor_id = ""

        for i in appointments:
            if i["appointment_id"] == appointment_id:
                patient_id = i["patient_id"]
                doctor_id = i["doctor_id"]
                break

        consultation = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "diagnosis": diagnosis,
            "treatment": treatment
        }

        consultations.append(consultation)
        save_consultations(consultations)

        print("Consultation saved successfully")

    # Update status
    def mark_appointment_status():

        appointment_id = input("Enter appointment id:\n").strip().upper()

        found = False

        # check appointment id first
        for i in appointments:

            if i["appointment_id"] == appointment_id:
                found = True
                break

        if not found:
            print("Appointment not found")
            return

        # only ask status if appointment exists
        status = input("Enter status (Completed / Missed / Cancelled):\n").strip()

        for i in appointments:

            if i["appointment_id"] == appointment_id:
                i["status"] = status
                break

        save_appointments(appointments)

        print("Status updated successfully")

    # Menu
    while True:

        print("\n" + "=" * 40)
        print("              DOCTOR MENU")
        print("=" * 40)

        try:
            doctor_option = int(input(
                "\n1.View Appointment"
                "\n2.Record Consultation"
                "\n3.Mark Appointment Status"
                "\n0.Exit"
                 "\n========================================"
                "\nEnter your choice: "
            ))

        except ValueError:
            print("Please enter number")
            continue

        if doctor_option == 1:
            view_appointment()
            input("\nPress Enter to continue...")

        elif doctor_option == 2:
            record_consultation()
            input("\nPress Enter to continue...")

        elif doctor_option == 3:
            mark_appointment_status()
            input("\nPress Enter to continue...")

        elif doctor_option == 0:
            print("Exiting Doctor Menu...")
            input("\nPress Enter to continue...")
            break

        else:
            print("Invalid choice. Please try again.")