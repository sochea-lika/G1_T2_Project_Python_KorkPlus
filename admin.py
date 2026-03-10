import uuid 
from admin_file import Admin, load_all_admins, save_new_admin, overwrite_admin_file, find_admin_by_email
from events import load_all_events, save_new_event, overwrite_event_file,is_valid_date
from password import password_strength_validation
# from tickets import get_tickets_by_event,get_total_seats_sold,load_all_tickets,cancel_ticket
from booking_file import get_tickets_by_event, get_total_seats_sold
def generate_event_id():
    events = load_all_events()
    if not events:
        return "E001"

    ids = []
    for event in events:
        if "id" in event and event["id"].startswith("E"):
            try:
                ids.append(int(event["id"][1:]))
            except ValueError:
                # Skip malformed IDs
                continue

    if not ids:   # safeguard against empty list
        return "E001"

    next_id = max(ids) + 1
    return f"E{next_id:03d}"


def register():
    print("======== Register=========")
    name = input("Enter name:").strip()
    email = input("Enter email:").strip()

    if find_admin_by_email(email):
        print("This email is already registered.")
        return
    
    while True:
        password = input("Enter password:").strip()
        if password_strength_validation(password):
            break
    
    # save new admin to admin.txt
    new_admin = Admin(name,email,password)
    save_new_admin(new_admin)
    print(f"Admin {name} registered succesffully!")

def sign_in():
    print("======== Sign in =========")
    email = input("Enter email :").strip()
    password = input("Enter password:").strip()

    admin = find_admin_by_email(email)
    
    if admin and admin.check_password(password):
        print(f"Welcome back {admin.name}")
        return admin
    else:
        print("Wrong password or email!")
        return None
    
def forget_password():
    print("======== Forget Password =========")
    email = input("Enter your registered email : ").strip()
     
    #load all admins and find the one with this email
    all_admins = load_all_admins()
    target_admin = None

    for admin in all_admins:
        if admin.get_email() == email:
            target_admin = admin
            break
    
    if target_admin is None:
        print("Email not found.")
        return

    # ask new password
    while True:
        new_password     = input("Enter new password   : ").strip()
        confirm_password = input("Confirm new password : ").strip()
        if new_password != confirm_password:
            print("Passwords do not match. Try again.")
            continue

        if password_strength_validation(new_password):
            break

    
    # update password and save to  file
    target_admin.set_password(new_password)
    overwrite_admin_file(all_admins)
    print("Password reset successfully!")

def add_event():
    print("======== Add Event =========")
    event_id = generate_event_id()
    title = input("Title : ").strip()

    while True:
        date = input("Date (YYYY-MM-DD) : ").strip()
        if is_valid_date(date):
            break

    location = input("Location : ").strip()
    description = input("Description : ").strip()
    price=input("Price: ").strip()
    while True:
        seats_input = input("Total seats : ").strip()
        if seats_input.isdigit() and int(seats_input) > 0:
            seats = int(seats_input)
            break
        print("  Please enter a valid number of seats.")

    new_event = {
        "id": event_id,
        "title": title,
        "date": date,
        "location": location,
        "description": description,
        "price": price,
        "seats_input": seats_input
    }

    save_new_event(new_event)
    print(f"Event '{title}' added! (ID: {event_id})")

def view_events():
    print("======== View all Event =========")
    events = load_all_events()
    if not events:
        print("No events found.")
        return

    # Print each event with a number
    for i, event in enumerate(events, start=1):
        print(f"\n  Event #{i}")
        print(f"    ID          : {event['id']}")
        print(f"    Title       : {event['title']}")
        print(f"    Date        : {event['date']}")
        print(f"    Location    : {event['location']}")
        print(f"    Description : {event['description']}")
        print(f"    Price       : {event['price']}")
        print(f"    Seat       : {event['seats_input']}")
        

def edit_event():
    print("======== Edit event =========")
    events = load_all_events()
    if not events:
        print("No events found.")
        return

    event_id = input("Enter Event ID to edit : ").strip()

    target_event = None
    for event in events:
        if event["id"] == event_id:
            target_event = event
            break

    if target_event is None:
        print("Event not found.")
        return
    print("Press Enter to keep the current value.")
    new_title = input(f"Title [{target_event['title']}] : ").strip()
    new_date = input(f"Date [{target_event['date']}]        : ").strip()
    new_location  = input(f"Location [{target_event['location']}]    : ").strip()
    new_description = input(f"Description [{target_event['description']}] : ").strip()
    new_price = input(f"Price [{target_event['price']}] : ").strip()
    new_seat = input(f"Seat [{target_event['seats_input']}] : ").strip()
    

    if new_title:  target_event["title"] = new_title
    if new_date: target_event["date"]  = new_date
    if new_location: target_event["location"] = new_location
    if new_description: target_event["description"] = new_description
    if new_price: target_event["price"] = new_price
    if new_seat: target_event["seats_input"] = new_seat
    overwrite_event_file(events)
    print("Event updated successfully.")

def delete_event():
    print("======== Delete Event =========")

    events = load_all_events()
    if not events:
        print("No events found.")
        return
    
    event_id = input("Enter Event ID to delete : ").strip()
    updated_events = [event for event in events if event["id"] != event_id]

    if len(updated_events) == len(events):
        print("Event not found.")
        return

    overwrite_event_file(updated_events)
    print("Event deleted successfully.")

def view_admins():
    print("======== View Admin =========")

    admins = load_all_admins()
    if not admins:
        print("No admins registered.")
        return

    for i, admin in enumerate(admins, start=1):
        print(f"\n  Admin #{i}")
        print(f"    Name  : {admin.name}")
        print(f"    Email : {admin.get_email()}")

def view_tickets():
    print("======== View Tickets Per Event =========")
    events = load_all_events()

    if not events:
        print("No events found.")
        return

    for i, event in enumerate(events, start=1):
        tickets = get_tickets_by_event(event["id"])
        seats_sold = get_total_seats_sold(event["id"])
        seats_remaining = event["seats_input"] - seats_sold

        print(f"\n  Event #{i}: {event['title']} (ID: {event['id']})")
        print(f"    Total Seats     : {event['seats_input']}")
        print(f"    Seats Sold      : {seats_sold}")
        print(f"    Seats Remaining : {seats_remaining}")

        if not tickets:
            print("    No tickets sold yet.")
        else:
            print("    Tickets:")
            for ticket in tickets:
                print(f"      - Ticket ID : {ticket['ticket_id']}")
                print(f"        User      : {ticket['user_email']}")
                print(f"        Quantity  : {ticket['quantity']}")
                print(f"        Purchased : {ticket['date_purchased']}")

# def cancel_ticket_action():
#     print("======== Cancel Ticket =========")
#     view_tickets()

#     ticket_id = input("\nEnter Ticket ID to cancel : ").strip()

#     # Find the ticket first to know which event to update seats for
#     all_tickets  = load_all_tickets()
#     target       = None

#     for ticket in all_tickets:
#         if ticket["ticket_id"] == ticket_id:
#             target = ticket
#             break

#     if target is None:
#         print("Ticket not found.")
#         return

#     # Cancel the ticket and get back how many seats were freed
#     seats_freed = cancel_ticket(ticket_id)

#     # Add the freed seats back to the event
#     event = get_event_by_id(target["event_id"])
#     if event:
#         update_event_seats(target["event_id"], event["seats"] + seats_freed)

#     print(f"Ticket '{ticket_id}' cancelled. {seats_freed} seat(s) returned to event.")


def admin_dashboard(logged_in_admin):
    while True:
        print(f"\n===== ADMIN PANEL ({logged_in_admin.name}) =====")
        print("1. Add Event")
        print("2. Edit Event")
        print("3. View Events")
        print("4. Delete Event")
        print("5. View Tickets Per Event")
        print("6. Cancel a Ticket")
        print("7. View Admin Accounts")
        print("8. logout")
        print("9. Exit Program")

        option = input("Enter your option : ").strip()

        if option == "1":
            add_event()
        elif option == "2":
            edit_event()
        elif option == "3":
            view_events()
        elif option == "4":
            delete_event()
        elif option == "5":
            view_tickets()
        elif option == "6":
            # cancel_ticket_action()
            break
        elif option == "7":
            view_admins()
        elif option == "8":
            print("Logged out.")
            return   # go back to the main menu
        elif option == "9":
            print("Goodbye!")
            exit()
        else:
            print("Invalid option. Please enter a number from 1 to 9.")


# =============================================
# MAIN MENU
# First screen the user sees when running the program
# =============================================

def main():
    
    while True:
        print("\n===== ADMIN SYSTEM =====")
        print("1. Register")
        print("2. Sign In")
        print("3. Forget Password")
        print("4. Exit Program")

        option = input("Enter your option : ").strip()

        if option == "1":
            register()

        elif option == "2":
            # Try to log in — if successful, open the dashboard
            logged_in_admin = sign_in()
            if logged_in_admin:
                admin_dashboard(logged_in_admin)

        elif option == "3":
            forget_password()

        elif option == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")


# Run the program
if __name__ == "__main__":
    main()
