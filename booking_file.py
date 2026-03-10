
import os
from events import load_all_events, overwrite_event_file
from tickets import save_all_tickets,load_all_tickets,generate_ticket_id
BOOKING_FILE = "bookings.txt"
CANCELLED_FILE = "cancelled_bookings.txt"
from rich.console import Console
from rich.table import Table

def load_all_bookings():
    if not os.path.exists(BOOKING_FILE):
        return []

    bookings = []

    with open(BOOKING_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")

            if len(parts) == 4:
                booking_id, user_id, event_id, quantity = parts

                bookings.append({
                    "id": booking_id,
                    "user_id": user_id,
                    "event_id": event_id,
                    "quantity": int(quantity)
                })

    return bookings



def save_all_bookings(bookings):
    with open(BOOKING_FILE, "w") as f:
        for b in bookings:
            f.write(f"{b['id']} | {b['user_id']} | {b['event_id']} | {b['quantity']}\n")


def load_all_cancelled_bookings():
    if not os.path.exists(CANCELLED_FILE):
        return []

    cancelled = []

    with open(CANCELLED_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")

            if len(parts) >= 4:
                ticket_id, booking_id, user_id, event_id = parts

                cancelled.append({
                    "ticket_id": ticket_id,
                    "booking_id": booking_id,
                    "user_id": user_id,
                    "event_id": event_id,
                    
                })

    return cancelled

def save_all_cancelled_bookings(cancelled_tickets):
    with open(CANCELLED_FILE, "w") as f:
        for t in cancelled_tickets:
            f.write(
                f"{t['ticket_id']} | {t['booking_id']} | {t['user_id']} | {t['event_id']}\n"         
            )


def generate_booking_id(bookings):
    if not bookings:
        return "B001"
    ids=[]
    ids = [int(b["id"][1:]) for b in bookings if b["id"].startswith("B")]
    next_id = max(ids) + 1 if ids else 1
    return f"B{next_id:03d}"

def create_booking(user_id, event_id, quantity):

    events = load_all_events()
    bookings = load_all_bookings()
    tickets = load_all_tickets()

    target_event = next((e for e in events if e["id"] == event_id), None)

    if not target_event:
        print("Event not found.")
        return

    seats_available = int(target_event["seats_input"])

    if seats_available < quantity:
        print("Not enough seats.")
        return

    ticket_price = float(target_event["price"])
    total_price = ticket_price * quantity
  
    console = Console()

    table = Table(title="Payment Table")

    table.add_column("Ticket Price", style="cyan")
    table.add_column("Quantity", justify="right", style="magenta")
    table.add_column("Total Price", justify="right", style="green")

    # 3. Add the Data (The Row)
    # Use f-strings to convert your variables into strings
    table.add_row(
        f"${ticket_price:.2f}", 
        str(quantity), 
        f"${total_price:.2f}"
    )

    console.print(table)

    payment = float(input("Enter payment amount: $"))

    if payment < total_price:
        print("Payment not enough.")
        return

    change = payment - total_price
    print(f"Payment successful. Change: ${change}")

    # create booking
    booking_id = generate_booking_id(bookings)

    bookings.append({
        "id": booking_id,
        "user_id": user_id,
        "event_id": event_id,
        "quantity": quantity
    })

    save_all_bookings(bookings)

    # create tickets
    print("\nYour Ticket IDs:")

    for i in range(quantity):

        ticket_id = generate_ticket_id(tickets)

        new_ticket = {
            "ticket_id": ticket_id,
            "booking_id": booking_id,
            "user_id": user_id,
            "event_id": event_id
        }

        tickets.append(new_ticket)
        print(ticket_id, end = " ")

    save_all_tickets(tickets)

    # reduce seats
    target_event["seats_input"] = str(seats_available - quantity)
    overwrite_event_file(events)

    print("\nBooking completed successfully.")

def get_tickets_by_event(event_id):
    all_tickets = load_all_tickets()
    return [t for t in all_tickets if t["event_id"] == event_id]

def get_total_seats_sold(event_id,):
    tickets = get_tickets_by_event(event_id)
    return sum(t["quantity"] for t in tickets)

def cancel_ticket(user_id, ticket_id):

    tickets = load_all_tickets()

    # find ticket belonging to this user
    target = next((t for t in tickets if t["ticket_id"] == ticket_id and t["user_id"] == user_id), None)

    if not target:
        print("Ticket not found or does not belong to you.")
        return

    # restore event seat
    events = load_all_events()
    event = next((e for e in events if e["id"] == target["event_id"]), None)

    if event:
        event["seats_input"] = str(int(event["seats_input"]) + 1)
        overwrite_event_file(events)

    # remove ticket from ticket list
    tickets = [t for t in tickets if t["ticket_id"] != ticket_id]
    save_all_tickets(tickets)

    # update booking quantity
    bookings = load_all_bookings()

    for b in bookings:
        if b["id"] == target["booking_id"]:
            b["quantity"] -= 1

    # remove booking if no tickets left
    bookings = [b for b in bookings if b["quantity"] > 0]

    save_all_bookings(bookings)
    # save into cancelled bookings
    cancelled_bookings = load_all_cancelled_bookings()

    cancelled_bookings.append({
        "ticket_id": target["ticket_id"],
        "booking_id": target["booking_id"],
        "user_id": target["user_id"],
        "event_id": target["event_id"],
        
    })
    save_all_cancelled_bookings(cancelled_bookings)

    print(f"Ticket {ticket_id} cancelled successfully.")
    
def view_cancelled_bookings(user_id=None):

    cancelled = load_all_cancelled_bookings()

    if not cancelled:
        print("No cancelled tickets found.")
        return

    print("\n======= Cancelled Tickets =======")

    for t in cancelled:

        if user_id and t["user_id"] != user_id:
            continue

        print(f"\nTicket ID    : {t['ticket_id']}")
        print(f"Booking ID   : {t['booking_id']}")
        print(f"User ID      : {t['user_id']}")
        print(f"Event ID     : {t['event_id']}")

    print("\n===============================")
def view_tickets(user_id=None):
    tickets = load_all_tickets()
    events = load_all_events()

    if not tickets:
        print("No tickets found.")
        return

    print("\n======= Booking History =======")
    idx = 1
    for b in tickets:
        if user_id and b["user_id"] != user_id:
            continue


        # Find the event linked to this booking
        event = next((e for e in events if e["id"] == b["event_id"]), None)

        print(f"\nTickets #{idx}")
        print(f"Ticket ID    : {b['ticket_id']}")
        print(f"Booking ID   : {b['booking_id']}")
        print(f"User ID      : {b['user_id']}")
        print(f"Event ID     : {b['event_id']}")
        

    idx += 1
    print("\n================= ==============")

def view_booking(user_id=None):
    bookings = load_all_bookings()
    events = load_all_events()

    if not bookings:
        print("No bookings found.")
        return

    print("\n======= Booking History =======")
    idx = 1
    for b in bookings:
        if user_id and b["user_id"] != user_id:
            continue


        # Find the event linked to this booking
        event = next((e for e in events if e["id"] == b["event_id"]), None)

        print(f"\nBooking #{idx}")
        print(f"Booking ID   : {b['id']}")
        print(f"User ID      : {b['user_id']}")
        print(f"Event ID     : {b['event_id']}")
        print(f"Quantity     : {b['quantity']}")

        if event:
            print("----- Event Details -----")
            print(f"Title        : {event['title']}")
            print(f"Date         : {event['date']}")
            print(f"Location     : {event['location']}")
            print(f"Description  : {event['description']}")
            print(f"Price        : {event['price']}")
            print(f"Seats Available   : {event['seats_input']}")
    idx += 1
    print("\n================= ==============")



   
