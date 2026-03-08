


from person import Person
from event import Event
from system_manager import SystemManager
from booking_file import cancel_booking, create_booking, view_bookings,view_cancelled_bookings
from admin import view_events
from events import load_all_events

class User(Person):
    system = SystemManager() 
    def __init__(self, user_id, name, email, password):
        super().__init__(name, email, password)  
        self.user_id = user_id

# -------------------------------
# Password Validation
# -------------------------------
def password_strength_validation(password):
    if len(password) < 8:
        print("Password too short. Must be at least 8 characters.")
        return False
    
    special_character = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in special_character for c in password)

    if not has_lower:
        print("Password must contain at least one lowercase letter.")
    elif not has_upper:
        print("Password must contain at least one uppercase letter.")
    elif not has_digit:
        print("Password must contain at least one digit.")
    elif not has_special:
        print("Password must contain at least one special character.")
    else:
        return True
    
    return False

# -------------------------------
# Registration / Login
# -------------------------------
def register(system):
    users = system.load_users()
    user_id = f"U{len(users)+1:03d}"

    while True:
        username = input("Enter a username to register: ")
        if username in users:
            print("Username is already taken. Please choose a different one.")
            continue
        break

    email = input("Enter your email: ")

    while True:
        password = input("Enter a password: ")
        if password_strength_validation(password):
            print("Registration successful with a strong password!")
            break

    user_obj = User(user_id, username, email, password)
    system.save_user(user_obj)
    return user_obj

def login(system):
    users = system.load_users()
    attempt = 3

    while attempt > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username not in users or password != users[username]["password"]:
            attempt -= 1
            print(f"Invalid credentials. You have {attempt} attempts left.")
        else:
            print(f"Login successful! Welcome, {username}")
            user_data = users[username]
            return User(user_data["id"], username, user_data["email"], password)

    print("Too many failed attempts. Access blocked.")
    return None


def forgot_password(system):
    users = system.load_users()
    username = input("Enter your username to retrieve your password: ")
    if username not in users:
        print("This username is not registered. Please try again or register a new account.")
    else:
        print(f"Your password is: {users[username]['password']}")

# -------------------------------
# User Dashboard
# -------------------------------
def user_dashboard_menu(user_obj):
    while True:
        events = load_all_events()  # refresh events

        print("\n===== USER DASHBOARD =====")
        print("1. Create Booking")
        print("2. Cancel Booking")
        print("3. View All Events")
        print("4. View My Bookings")
        print("5. View My Cancelled Booking")
        print("6. Logout")

        choice = input("Enter option: ").strip()

        if choice == "1":
            view_events()
            event_id = input("Enter Event ID (e.g., E001): ").strip()
            qty = int(input("Enter quantity: ").strip())
            create_booking(user_obj.user_id, event_id, qty)

        elif choice == "2":
            view_bookings(user_obj.user_id)
            booking_id = input("Enter Booking ID (e.g., B001): ").strip()
            cancel_booking(user_obj.user_id,booking_id)

        elif choice == "3":
            view_events()

        elif choice == "4":
            view_bookings(user_obj.user_id)
            
        elif choice == "5":
            view_cancelled_bookings(user_obj.user_id)

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid option. Try again.")

# -------------------------------
# Main Menu
# -------------------------------
def menu():
    system = SystemManager()

    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        op = input("Choose an option (1-4): ").strip()

        if op == "1":
            user_obj = register(system)
            user_dashboard_menu(user_obj)
        elif op == "2":
            user_obj = login(system)
            if user_obj:
                user_dashboard_menu(user_obj)
        elif op == "3":
            forgot_password(system)
        elif op == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Please choose option 1 - 4.")

if __name__ == "__main__":
    menu()


