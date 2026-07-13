def generate_bill_id(filename):
    try:
        with open(filename,"r") as file:
            lines = file.readlines()

        # remove empty lines
        lines = [line for line in lines if line.strip() != ""]

        if not lines:
            return "B001"
        
        last_line = lines[-1].strip().split("|")
        last_bill_id = last_line[0]
        last_number = int(last_bill_id[1:])
        new_number = last_number + 1

        return f"B{new_number:03d}"
    
    except FileNotFoundError:
        print("File NOT FOUND")
        return "B001"

def find_appointment(appointment_id, filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                data = line.strip().split("|")

                # check if appoinment ID matches
                if data[0] == appointment_id:
                    return data
                
            # if no match found
            return None
        
    except FileNotFoundError:
        print("File NOT FOUND")
        return None

def get_doctor_fee(doctor_id, filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                data = line.strip().split("|")
                if data[0] == doctor_id:
                    return float(data[3])
                
        return None
    except FileNotFoundError:
        print("Doctor file not found")
        return None

def generate_bill():
    appointment_id = input("Enter Appointment ID: ").strip()
    if bill_exists(appointment_id, "billing.txt"):
                print("Bill already exists for this appointment.")
                return

    appointment = find_appointment(appointment_id, "appointments.txt")

    if appointment is None:
        print("Appointment not found")
        return
    
    # check status
    if appointment[5].lower() != "completed":
        print("Bill can only be generated for completed appointments")
        return
    
    doctor_id = appointment[2]

    consultation_fee = get_doctor_fee(doctor_id,"doctors.txt")

    if consultation_fee is None:
        print("Doctor fee not found")
        return
                
    # input optional charges
    try:
        optional_charges = float(input("Enter optional charges: RM ").strip())
        if optional_charges < 0:
            print("Charges cannot be negative.")
            return
    except ValueError:
        print("Invalid input")
        return

    total = consultation_fee + optional_charges

    bill_id = generate_bill_id("billing.txt")

    from datetime import datetime
    today = datetime.now().strftime("%d/%m/%Y")
    record = f"{bill_id}|{appointment_id}|{doctor_id}|{consultation_fee:.2f}|{optional_charges:.2f}|{total:.2f}|Unpaid|-|{today}\n"
                                                       
    with open("billing.txt", "a") as file:
        file.write(record)

    print("\nBill generated successfully!")
    print("Bill ID:", bill_id)
    print("Total: RM", total)

def bill_exists(appointment_id, filename):
    try:
        with open(filename,"r") as file:
            for line in file:
                data = line.strip().split("|")

                if len(data) >= 2 and data[1] == appointment_id:
                    return True
        return False
    
    except FileNotFoundError:
        return False
    
def record_payment():
    bill_id = input("Enter Bill ID: ").strip()

    valid_payment_methods = ("cash", "card", "e-wallet")

    try:
        with open("billing.txt", "r") as file:
            lines = file.readlines()

        found = False

        for i in range(len(lines)):
            data = lines[i].strip().split("|")

            if data[0].strip() == bill_id:
                found = True

                if data[6].lower() == "paid":
                    print("This bill is already paid.")
                    return
                
                payment_method = input("Enter payment method (Cash/Card/E-Wallet): ").strip().lower()

                if payment_method not in valid_payment_methods:
                    print("Invalid payment method.")
                    return

                if payment_method == "cash":
                    payment_method = "Cash"
                elif payment_method == "card":
                    payment_method = "Card"
                else:
                    payment_method = "E-Wallet"

                data[6] = "Paid"
                data[7] = payment_method

                # rebuild line
                lines[i] = "|".join(data) + "\n"
                break

        if not found:
            print("Bill not found.")
            return
        
        # write back to file
        with open("billing.txt", "w") as file:
            file.writelines(lines)

        print("Payment recorded successfully")

    except FileNotFoundError:
        print("Billing file not found.")

def view_outstanding_payments():
    try:
        with open("billing.txt", "r") as file:
            found = False

            print("\n--- Outstanding Payments ---")

            for line in file:
                data = line.strip().split("|")

                if len(data) < 9:
                    continue

                if data[6].lower() == "unpaid":
                    found = True
                    print(f"Bill ID: {data[0]} | Amount: RM {data[5]}")

            if not found:
                print("No outstanding payments.")

    except FileNotFoundError:
        print("Billing file not found.")

def view_daily_revenue():
    target_date = input("Enter date (DD/MM/YYYY): ").strip()
    total_revenue = 0.0

    try:
        with open("billing.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")

                # skip invalid lines
                if len(data) < 9:
                    continue

                if data[6].lower() == "paid" and data[8] == target_date:
                    total_revenue += float(data[5])

        print(f"Total revenue on {target_date}: RM {total_revenue:.2f}")

    except FileNotFoundError:
        print("Billing file not found.")

def view_revenue_by_doctor():
    revenue_dict = {}

    try:
        with open("billing.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")

                if len(data) < 9:
                    continue

                if data[6].lower() == "paid":
                    doctor_id = data[2]
                    total_amount = float(data[5])

                    if doctor_id in revenue_dict:
                        revenue_dict[doctor_id] += total_amount
                    else:
                        revenue_dict[doctor_id] = total_amount

        print("\n---- Revenue by Doctor ----")

        if not revenue_dict:
            print("No paid bills found.")
        else:
            for doctor_id, revenue in revenue_dict.items():
                print(f"{doctor_id}: RM {revenue:.2f}")
                print("---------------------------")
    
    except FileNotFoundError:
        print("Billing file not found.")

def view_bill_details():
    bill_id = input("Enter Bill ID: ").strip()

    try:
        with open("billing.txt", "r") as file:
            found = False

            for line in file:
                data = line.strip().split("|")

                if len(data) < 9:
                    continue

                if data[0] == bill_id:
                    found = True

                    print("\n------ Bill Details ------")
                    print("Bill ID:", data[0])
                    print("Appointment ID:", data[1])
                    print("Doctor ID:", data[2])
                    print("Consultation Fee:", data[3])
                    print("Extra Charges:", data[4])
                    print("Total:", data[5])
                    print("Status:", data[6])
                    print("Payment Method:", data[7])
                    print("Date:", data[8])
                    print("--------------------------")
                    break

            if not found:
                print("Bill not found.")

    except FileNotFoundError:
        print("Billing file not found.")

def pause():
    input("\nPress Enter to continue...")

def display_header(title):
    print("\n" + "=" * 40)
    print(f"            {title}")
    print("=" * 40)

def finance_menu():
    while True:
        display_header("FINANCE MENU")
        print("1. Generate Bill")
        print("2. Record Payment")
        print("3. View Outstanding Payments")
        print("4. View Daily Revenue")
        print("5. View Revenue by Doctor")
        print("6. View Bill Details")
        print("0. Exit")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_bill()
            pause()
        elif choice == "2":
            record_payment()
            pause()
        elif choice == "3":
            view_outstanding_payments()
            pause()
        elif choice == "4":
            view_daily_revenue()
            pause()
        elif choice == "5":
            view_revenue_by_doctor()
            pause()
        elif choice == "6":
            view_bill_details()
            pause()
        elif choice == "0":
            print("Exiting Finance Menu...")
            input("\nPress Enter to continue...")
            break
        else:
            print("Invalid choice. Please try again.")