
import os
from events import load_all_events, overwrite_event_file
from tickets import save_all_tickets,load_all_tickets,generate_ticket_id
BOOKING_FILE = "bookings.txt"
CANCELLED_FILE = "cancelled_bookings.txt"
# TICKET_FILE = "tickets.txt"
# def load_all_tickets():
#     if not os.path.exists(TICKET_FILE):
#         return []

#     tickets = []

#     with open(TICKET_FILE, "r") as f:
#         for line in f:
#             parts = line.strip().split(" | ")

#             if len(parts) == 4:
#                 ticket_id, booking_id, user_id, event_id = parts

#                 tickets.append({
#                     "ticket_id": ticket_id,
#                     "booking_id": booking_id,
#                     "user_id": user_id,
#                     "event_id": event_id
#                 })

#     return tickets
# def save_all_tickets(tickets):
#     with open(TICKET_FILE, "w") as f:
#         for t in tickets:
#             f.write(f"{t['ticket_id']} | {t['booking_id']} | {t['user_id']} | {t['event_id']}\n")
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

            if len(parts) >= 10:
                booking_id, user_id, event_id, quantity, title, date, location, description, price, seats = parts

                cancelled.append({
                    "id": booking_id,
                    "user_id": user_id,
                    "event_id": event_id,
                    "quantity": int(quantity),
                    "title": title,
                    "date": date,
                    "location": location,
                    "description": description,
                    "price": price,
                    "seats_input": seats
                })

    return cancelled


def save_all_cancelled_bookings(cancelled_bookings):
    with open(CANCELLED_FILE, "w") as f:
        for b in cancelled_bookings:
            f.write(
                f"{b['id']} | {b['user_id']} | {b['event_id']} | {b['quantity']} | "
                f"{b['title']} | {b['date']} | {b['location']} | {b['description']} | "
                f"{b['price']} | {b['seats_input']}\n"
            )


def generate_booking_id(bookings):
    if not bookings:
        return "B001"
    ids=[]
    ids = [int(b["id"][1:]) for b in bookings if b["id"].startswith("B")]
    next_id = max(ids) + 1 if ids else 1
    return f"B{next_id:03d}"

# def generate_ticket_id(bookings):

#     if not bookings:
#         return "T001"
#     ids=[]
#     ids = [int(b["ticket_id"][1:]) for b in bookings if b["ticket_id"].startswith("T")]
#     next_id = max(ids) + 1 if ids else 1

#     return f"T{next_id:03d}"
# def generate_ticket_id(tickets):

#     if not tickets:
#         return "T001"

#     ids = [int(t["ticket_id"][1:]) for t in tickets]
#     next_id = max(ids) + 1

#     return f"T{next_id:03d}"
# def create_booking(user_id, event_id, quantity):
#     events = load_all_events()
#     bookings = load_all_bookings()

#     target_event = None
#     for e in events:
#         if e["id"] == event_id:
#             target_event = e
#             break
#     if not target_event:
#         print("Event not found.")
#         return

#     seats_available = int(target_event["seats_input"])
#     if seats_available < quantity:
#         print("Not enough seats available.")
#         return

#     # calculate total price
#     ticket_price = float(target_event["price"])
#     total_price = ticket_price * quantity

#     print("\n------ Payment Summary ------")
#     print(f"Ticket Price : ${ticket_price}")
#     print(f"Quantity     : {quantity}")
#     print(f"Total Price  : ${total_price}")

#     # payment input
#     payment = float(input("Enter payment amount: $"))

#     if payment < total_price:
#         print("Payment not enough. Booking cancelled.")
#         return

#     change = payment - total_price
#     print(f"Payment successful. Change: ${change}")

    
#     booking_id = generate_booking_id(bookings)
#     for i in range(quantity):
#         ticket_id = generate_ticket_id(bookings)

#         new_row = {
#             "id": booking_id,
#             "user_id": user_id,
#             "event_id": event_id,
#             "quantity": 1,
#             "ticket_id": ticket_id
#         }

#         bookings.append(new_row)
#         save_all_bookings(bookings)
#         print("\n All tickets hve been booked successfully")
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

    print("\n------ Payment Summary ------")
    print(f"Ticket Price : ${ticket_price}")
    print(f"Quantity     : {quantity}")
    print(f"Total Price  : ${total_price}")

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

        print(ticket_id)

    save_all_tickets(tickets)

    # reduce seats
    target_event["seats_input"] = str(seats_available - quantity)
    overwrite_event_file(events)

    print("\nBooking completed successfully.")
def get_tickets_by_event(event_id):
    all_tickets = load_all_bookings()
    return [t for t in all_tickets if t["event_id"] == event_id]

def get_total_seats_sold(event_id,):
    tickets = get_tickets_by_event(event_id)
    return sum(t["quantity"] for t in tickets)

def cancel_booking(user_id, tickets):
    

    tickets = load_all_tickets()

    # Find ticket belonging to this user only
    target = next((b for b in tickets if b["id"] == ti and b["user_id"] == user_id), None)

    if not target:
        print("Booking not found or this booking does not belong to you.")
        return

    # restore seats
    events = load_all_events()
    event = next((e for e in events if e["id"] == target["event_id"]), None)

    if event:
        event["seats_input"] = str(int(event["seats_input"]) + target["quantity"])
        overwrite_event_file(events)

    # remove from active bookings
    bookings = [b for b in bookings if b["id"] != booking_id]
    save_all_bookings(bookings)

    # save into cancelled bookings
    cancelled_bookings = load_all_cancelled_bookings()

    cancelled_bookings.append({
        "id": target["id"],
        "user_id": target["user_id"],
        "event_id": target["event_id"],
        "quantity": target["quantity"],
        "title": event["title"],
        "date": event["date"],
        "location": event["location"],
        "description": event["description"],
        "price": event["price"],
        "seats_input": event["seats_input"]
    })

    save_all_cancelled_bookings(cancelled_bookings)

    print(f"Booking {booking_id} cancelled successfully.")


def view_cancelled_bookings(user_id=None):
    cancelled = load_all_cancelled_bookings()

    if not cancelled:
        print("No cancelled bookings found.")
        return

    print("\n======= Cancelled Bookings =======")

    for b in cancelled:

        # show only this user's data
        if user_id and b["user_id"] != user_id:
            continue

        print(f"\nBooking ID   : {b['id']}")
        print(f"User ID      : {b['user_id']}")
        print(f"Event ID     : {b['event_id']}")
        print(f"Quantity     : {b['quantity']}")

        print("----- Event Details -----")
        print(f"Title        : {b['title']}")
        print(f"Date         : {b['date']}")
        print(f"Location     : {b['location']}")
        print(f"Description  : {b['description']}")
        print(f"Price        : {b['price']}")
        print(f"Seats Left   : {b['seats_input']}")

    print("\n==================================")


def view_bookings(user_id=None):
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



   
