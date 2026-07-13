DOCTOR_FILE = "doctors.txt"
APPOINTMENT_FILE = "appointments.txt"
PATIENT_FILE = "patient.txt"

def admin_menu():
    while True:
        print("\n" + "=" * 40)
        print("              ADMINISTRATOR MENU")
        print("=" * 40)
        print("1. Add Doctor")
        print("2. Update Doctor")
        print("3. Remove Doctor")
        print("4. View Doctor")
        print("5. View Reports")
        print("0. Exit")
        print("=" * 40)

        try:
            choice = int(input("Enter your choice:"))
        except:
            print("Invalid input")
            continue

        if choice == 1:
            add_doctor()
            input("\nPress Enter to continue...")
        elif choice == 2:
            update_doctor()
            input("\nPress Enter to continue...")
        elif choice == 3:
            remove_doctor()
            input("\nPress Enter to continue...")
        elif choice == 4:
            view_doctors()
            input("\nPress Enter to continue...")
        elif choice == 5:
            view_reports()
            input("\nPress Enter to continue...")
        elif choice == 0:
            print("Exiting Admin Menu...")
            input("\nPress Enter to continue...")
            break

        else:
            print("Invalid Choice")

def generate_doctor_id():
    max_id = 0

    try:
        file = open(DOCTOR_FILE, "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            parts = line.strip().split("|")

            doctor_id = parts[0]   # Example: D003

            number = int(doctor_id[1:])   # Remove 'D'

            if number > max_id:
                max_id = number

    except:
        max_id = 0

    new_id = max_id + 1

    return "D" + str(new_id).zfill(3)

def add_doctor():
    print("\n==== Add Doctor ====")

    doctor_id = generate_doctor_id()

    while True:
        name = input("Enter doctor name: ").strip()

        if name == "":
            print("Name cannot be empty!")
        else:
            break

    while True:
        specialization = input("Enter specialization: ").strip()

        if specialization == "":
            print("Specialization cannot be empty!")
        else:
            break

    while True:
        try:
            fee = float(input("Enter consultation fee (RM): "))

            if fee <= 0:
                print("Fee must be greater than 0!")
                continue

            break

        except:
            print("Invalid input! Enter numbers only.")

    # Slots Validation
    while True:
        slots = input("Enter available slots (Example: 09:00AM-10:00PM): ").strip()

        if slots == "":
            print("Slots cannot be empty!")
        else:
            break

    file = open(DOCTOR_FILE, "a")

    file.write(
        doctor_id + "|" +
        name + "|" +
        specialization + "|" +
        str(fee) + "|" +
        slots + "\n"
    )

    file.close()

    print("Doctor added successfully!")
    print("Doctor ID:", doctor_id)


def remove_doctor():
    print("\n==== Remove Doctor ====")

    doctor_id = input("Enter Doctor ID to remove: ").strip().upper()

    try:
        file = open(DOCTOR_FILE, "r")
        lines = file.readlines()
        file.close()

    except:
        print("Doctor file not found.")
        return

    updated_lines = []
    found = False

    for line in lines:
        parts = line.strip().split("|")

        if parts[0] == doctor_id:
            found = True
            print("Doctor removed successfully!")

        else:
            updated_lines.append(line)

    if found:
        file = open(DOCTOR_FILE, "w")

        for line in updated_lines:
            file.write(line)

        file.close()

    else:
        print("Doctor ID not found!")


def view_doctors():
    print("\n==== Doctor List ====")

    try:
        file = open(DOCTOR_FILE, "r")
        lines = file.readlines()
        file.close()

        if len(lines) == 0:
            print("No doctors found.")
            return

        for line in lines:
            parts = line.strip().split("|")

            print("--------------------------------")
            print("Doctor ID      :", parts[0])
            print("Name           :", parts[1])
            print("Specialization :", parts[2])
            print("Fee            : RM", parts[3])
            print("Slots          :", parts[4])

    except:
        print("Doctor file not found.")


def update_doctor():
    print("\n==== Update Doctor ====")

    doctor_id = input("Enter Doctor ID to update: ").strip().upper()

    try:
        file = open(DOCTOR_FILE, "r")
        lines = file.readlines()
        file.close()

    except:
        print("Doctor file not found.")
        return

    updated_lines = []
    found = False

    for line in lines:
        parts = line.strip().split("|")

        if parts[0] == doctor_id:
            found = True

            print("Doctor found!")

            new_name = input("Enter new name: ").strip()
            new_specialization = input("Enter new specialization: ").strip()

            while True:
                try:
                    new_fee = float(input("Enter new fee: RM"))

                    if new_fee <= 0:
                        print("Fee must be greater than 0!")
                        continue

                    break

                except:
                    print("Invalid fee!")

            new_slots = input("Enter new slots: ").strip()

            updated_line = (
                parts[0] + "|" +
                new_name + "|" +
                new_specialization + "|" +
                str(new_fee) + "|" +
                new_slots + "\n"
            )

            updated_lines.append(updated_line)

        else:
            updated_lines.append(line)

    if found:
        file = open(DOCTOR_FILE, "w")

        for line in updated_lines:
            file.write(line)

        file.close()

        print("Doctor updated successfully!")

    else:
        print("Doctor ID not found!")

def view_reports():
    print("\n==== Clinic Reports ====")

    # Total Doctors
    try:
        file = open(DOCTOR_FILE, "r")
        doctor_lines = file.readlines()
        file.close()

        total_doctors = len([line for line in doctor_lines if line.strip() != ""])

    except:
        total_doctors = 0

    # Total Patients
    try:
        file = open(PATIENT_FILE, "r")
        patient_lines = file.readlines()
        file.close()

        total_patients = len([line for line in patient_lines if line.strip() != ""])

    except:
        total_patients = 0

    # Total Appointments
    try:
        file = open(APPOINTMENT_FILE, "r")
        appointment_lines = file.readlines()
        file.close()

        total_appointments = len([line for line in appointment_lines if line.strip() != ""])

    except:
        appointment_lines = []
        total_appointments = 0

    # Appointment Status Report
    completed = 0
    cancelled = 0
    missed = 0
    booked = 0

    for line in appointment_lines:
        parts = line.strip().split("|")

        if len(parts) >= 6:
            status = parts[5].strip().lower()

            if status == "completed":
                completed += 1
            elif status == "cancelled":
                cancelled += 1
            elif status == "missed":
                missed += 1
            elif status == "booked":
                booked += 1

    # Most Visited Doctor
    doctor_count = {}

    for line in appointment_lines:
        parts = line.strip().split("|")

        if len(parts) >= 6:
            doctor_id = parts[2].strip()

            if parts[5].strip().lower() != "cancelled":
                if doctor_id in doctor_count:
                    doctor_count[doctor_id] += 1
                else:
                    doctor_count[doctor_id] = 1

    if doctor_count:
        most_doctor = max(doctor_count, key=doctor_count.get)
        most_doctor_count = doctor_count[most_doctor]
    else:
        most_doctor = "N/A"
        most_doctor_count = 0

    # Display Reports
    print("--------------------------------")
    print("Total Doctors          :", total_doctors)
    print("Total Patients         :", total_patients)
    print("Total Appointments     :", total_appointments)
    print("--------------------------------")
    print("Booked Appointments    :", booked)
    print("Completed Appointments :", completed)
    print("Cancelled Appointments :", cancelled)
    print("Missed Appointments    :", missed)
    print("--------------------------------")
    print("Most Visited Doctor    :", most_doctor)
    print("Total Visits           :", most_doctor_count)
    print("--------------------------------")