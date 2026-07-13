from admin_part import admin_menu
from receptionist_part import receptionist_menu
from doctor_part import doctor_menu
from finance_officer_part import finance_menu

def main_menu():
    while True:
        print("\n" + "=" * 42)
        print("           SMARTCLINIC SYSTEM")
        print("=" * 42)
        print("1. Administrator")
        print("2. Receptionist")
        print("3. Doctor")
        print("4. Finance Officer")
        print("0. Exit")
        print("=" * 42)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            admin_menu()
        elif choice == "2":
            receptionist_menu()
        elif choice == "3":
            doctor_menu()
        elif choice == "4":
            finance_menu()
        elif choice == "0":
            print("Exiting SmartClinic System...")
            break
        else:
            print("Invalid choice. Please try again.")
            
main_menu()