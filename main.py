from admin import main as admin_menu  # your existing admin panel
from user import menu as user_menu   # your user registration/login + dashboard

def main():
    while True:
        print("\n===== EVENT BOOKING SYSTEM =====")
        print("1. Admin Panel")
        print("2. User Panel")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            # Run the admin menu
            admin_menu()
            
        elif choice == "2":
            # Run the user menu
            user_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-3.")

if __name__ == "__main__":
    main()
