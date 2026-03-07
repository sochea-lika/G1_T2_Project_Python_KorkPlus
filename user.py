from person import Person
from event import Event
from system_manager import SystemManager

class User(Person):
    system = SystemManager() 
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def display_dashboard(self, events):
        print("\nUSER DASHBOARD")
        print("\nAvailable Events for Booking:\n")
        print("| ID | Event Name           | Date       | Price  | Available Seats       |")
        print("|----|----------------------|------------|--------|------------------------|")
        for event in events:
            if event.available_seats == 0:
                status = " SOLD OUT"
            elif event.available_seats < 15:
                status = f" {event.available_seats} Seats Remaining"
            else:
                status = f" {event.available_seats} Seats Remaining"
            print(f"| {event.event_id:02} | {event.title:<20} | {event.date} | ${event.price:<5.2f} | {status:<22} |")

        print("\nOptions: [1] Book Ticket | [2] Cancel Booking | [3] My Bookings | [4] Logout")


# -------------------------------
# Registration/Login System (file-based)
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


def register(system):
    users = system.load_users()
    while True:
        username = input("Enter a username to register: ")
        if username in users:
            print("Username is already taken. Please choose a different one.")
            continue
        break

    while True:
        password = input("Enter a password: ")
        if password_strength_validation(password):
            print("Registration successful with a strong password!")
            break

    user_obj = User(username, f"{username}@example.com", password)
    system.save_user(user_obj)
    return user_obj


def login(system):
    users = system.load_users()
    attempt = 3
    while attempt > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username not in users or password != users[username]:
            attempt -= 1
            print(f"Invalid credentials. You have {attempt} attempts left.")
        else:
            print(f"Login successful! Welcome, {username}")
            return User(username, f"{username}@example.com", password)
        if attempt == 0:
            print("Too many failed attempts. Access blocked.")
            return None


def forgot_password(system):
    users = system.load_users()
    username = input("Enter your username to retrieve your password: ")
    if username not in users:
        print("This username is not registered. Please try again or register a new account.")
    else:
        print(f"Your password is: {users[username]}")


# -------------------------------
# Unified User Dashboard Menu
# -------------------------------
def user_dashboard_menu(user_obj, events):
    while True:
        user_obj.display_dashboard(events)
        choice = int(input("Select an option: "))

        match choice:
            case 1:
                break
            case 2:
                break
            case 3: 
                break
            case 4:
                print("Logging out...")
                break
            case _:
                print("Invalid choice!")


def menu(events):
    system = SystemManager()

    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        op = int(input("Choose an option (1-4): "))

        match op:
            case 1:
                user_obj = register(system)
                user_dashboard_menu(user_obj, events)
            case 2:
                user_obj = login(system)
                
                user_dashboard_menu(user_obj, events)
            case 3:
                forgot_password(system)
            case 4:
                print("Exiting the program. Goodbye!")
                break
            case _:
                print("Please choose option 1 - 4.")



if __name__ == "__main__":
    # Sample events
    events = [
        Event(1, "Music Festival 2026", 25.00, 45),
        Event(2, "Python Tech Expo", 15.00, 12),
        Event(3, "AI Startup Night", 50.00, 0)
    ]
    events[0].date = "2026-05-20"
    events[1].date = "2026-06-12"
    events[2].date = "2026-07-05"

    menu(events)


