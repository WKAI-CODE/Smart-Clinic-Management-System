from datetime import datetime

patient_file = "patient.txt"
appointment_file = "appointments.txt"

def generate_patient_id():
    try:
        with open(patient_file, "r") as file:
            lines = [line for line in file.readlines() if "|" in line]
            count = len([l for l in lines if "|" in l])
    except:
        return "P001"

    return f"P{count + 1:03d}"

def generate_appointment_id():
    try:
        with open(appointment_file, "r") as file:
            lines = [line for line in file.readlines() if "|" in line]
            count = len([l for l in lines if "|" in l])
    except:
        return "A001"

    return f"A{count + 1:03d}"

def patient_exists(patient_id):
    try:
        with open(patient_file, "r") as file:

            for line in file:

                if "|" not in line:
                    continue

                data = line.strip().split("|")

                if data[0].upper() == patient_id:
                    return True

        return False

    except:
        return False
    
def doctor_exists(doctor_id):
    try:
        with open("doctors.txt", "r") as file:

            for line in file:

                if "|" not in line:
                    continue

                data = line.strip().split("|")

                if data[0].upper() == doctor_id:
                    return True

        return False

    except:
        return False


def register_patient():
    patient_id = generate_patient_id()

    while True:
        name = input("Enter Name: ").title()
        if name.replace(" ", "").isalpha():
            break
        print("Invalid name. Try again.")

    while True:
        age = input("Enter Age: ")
        if age.isdigit():
            break
        print("Invalid age. Try again.")

    while True:
        gender = input("Enter Gender: ").upper()
        if gender in ["MALE", "FEMALE"]:
            gender = gender.capitalize()
            break
        print("Invalid gender. Try again.")

    while True:
        contact = input("Enter Contact: ")

        if "-" in contact:
            if contact[3] != "-":
                print("Invalid contact. Try again.")
                continue
            cont = contact.replace("-", "")
        else:
            cont = contact
            contact = contact[:3] + "-" + contact[3:]

        if not cont.isdigit():
            print("Invalid contact. Try again.")
            continue

        if cont[:2] != "01":
            print("Invalid contact. Try again.")
            continue

        if len(cont) < 10 or len(cont) > 12:
            print("Invalid contact. Try again.")
            continue
        break
    try:
        with open(patient_file, "r") as file:
            lines = [line for line in file.readlines() if "|" in line]
            for line in lines:
                if "|" not in line:
                    continue
                data = line.strip().split("|")
                if data[1].upper() == name.upper() and data[4] == contact:
                    print("Patient already exists.")
                    return
    except:
        pass

    with open(patient_file, "a") as file:
        file.write(f"{patient_id}|{name}|{age}|{gender}|{contact}\n")

    print("Patient registered successfully.")
    print("Patient ID:", patient_id)

def book_appointment():
    appointment_id = generate_appointment_id()

    while True:
        patient_id = input("Enter Patient ID: ").strip().upper()

        if len(patient_id) >= 2 and patient_id[0] == "P" and patient_id[1:].isdigit():

            if patient_exists(patient_id):
                break

            print("Patient ID not found.")

        else:
            print("Invalid Patient ID.")
        
    while True:
        doctor_id = input("Enter Doctor ID: ").strip().upper()

        if len(doctor_id) >= 2 and doctor_id[0] == "D" and doctor_id[1:].isdigit():

            if doctor_exists(doctor_id):
                break

            print("Doctor ID not found.")

        else:
            print("Invalid Doctor ID.")

    while True:
        date = input("Enter Date (DD/MM/YYYY): ")
        try:
            day, month, year = date.split("/")

            if len(day) == 1:
                day = "0" + day
            if len(month) == 1:
                month = "0" + month

            date = f"{day}/{month}/{year}"

            input_date = datetime.strptime(date, "%d/%m/%Y")
            if input_date.date() < datetime.today().date():
                print("Cannot book past date.")
                continue
            break
        except:
            print("Invalid date.")

    while True:
        time = input("Enter Time (HH:MM): ")
        try:
            datetime.strptime(time, "%H:%M")
            break
        except:
            print("Invalid time.")
    try:
        with open(appointment_file, "r") as file:
            lines = [line for line in file.readlines() if "|" in line]
            for line in lines:
                if "|" not in line:
                    continue
                data = line.strip().split("|")

                if (
                    data[2] == doctor_id and
                    data[3] == date and
                    data[4] == time and
                    data[5] != "Cancelled"
                ):
                    print("Time slot already booked.")
                    return
    except:
        pass

    with open(appointment_file, "a") as file:
        file.write(f"{appointment_id}|{patient_id}|{doctor_id}|{date}|{time}|Booked\n")

    print("Appointment booked successfully.")
    print("Appointment ID:", appointment_id)

def reschedule_appointment():
    appointment_id = input("Enter Appointment ID: ").strip().upper()
    try:
        with open(appointment_file, "r") as file:
            lines = file.readlines()
    except:
        print("File error.")
        return

    found = False
    updated = []

    for line in lines:
        if "|" not in line:
            updated.append(line)
            continue

        data = line.strip().split("|")

        if data[0] == appointment_id and data[5] == "Booked":
            found = True
            data[5] = "Cancelled"
            updated.append("|".join(data) + "\n")
        else:
            updated.append(line)

    if not found:
        print("Appointment not found.")
        return

    with open(appointment_file, "w") as file:
        file.writelines(updated)

    print("Old appointment cancelled.")
    print("Now book new appointment:")
    book_appointment()

def cancel_appointment():
    appointment_id = input("Enter Appointment ID: ").strip().upper()

    try:
        with open(appointment_file, "r") as file:
            lines = file.readlines()
    except:
        print("File error.")
        return

    updated = []
    found = False

    for line in lines:
        if "|" not in line:
            updated.append(line)
            continue

        data = line.strip().split("|")

        if data[0] == appointment_id:
            found = True
            if data[5] == "Cancelled":
                print("Already cancelled.")
            else:
                data[5] = "Cancelled"
                print("Cancelled successfully.")
            updated.append("|".join(data) + "\n")
        else:
            updated.append(line)

    if not found:
        print("Appointment not found.")
        return

    with open(appointment_file, "w") as file:
        file.writelines(updated)

def check_availability():
    doctor_id = input("Enter Doctor ID: ").strip().upper()
    date = input("Enter Date (DD/MM/YYYY): ").strip()

    booked_slots = []

    try:
        with open(appointment_file, "r") as file:

            for line in file:
                data = line.strip().split("|")

                if len(data) >= 6:
                    if (
                        doctor_id == data[2] and
                        date == data[3] and
                        data[5] != "Cancelled"
                    ):
                        booked_slots.append(data[4])

    except FileNotFoundError:
        print("Appointments file not found.")
        return

    all_slots = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]

    print("\nAvailable Slots:")

    found_available = False

    for slot in all_slots:
        if slot not in booked_slots:
            print(slot)
            found_available = True

    if not found_available:
        print("No available slots.")

def receptionist_menu():
    while True:
        print("\n" + "=" * 40)
        print("           RECEPTIONIST MENU")
        print("=" * 40)
        print("1 Register Patient")
        print("2 Book Appointment")
        print("3 Reschedule Appointment")
        print("4 Cancel Appointment")
        print("5 Check Availability")
        print("6 Exit")
        print("=" * 40)

        try:
            choice = int(input("Enter choice: "))
        except:
            print("Invalid input.")
            continue

        if choice == 1:
            register_patient()
        elif choice == 2:
            book_appointment()
        elif choice == 3:
            reschedule_appointment()
        elif choice == 4:
            cancel_appointment()
        elif choice == 5:
            check_availability()
        elif choice == 6:
            break
        else:
            print("Invalid choice.")