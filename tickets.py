# # Format of each line:
# # ticket_id|event_id|user_email|quantity|date_purchased
import os
# import uuid
# from datetime import datetime

# Ticket_file = "tickets.txt"
# tickets = []
# def load_all_tickets():
#     tickets = []
#     if os.path.exists(Ticket_file):
#         with open(Ticket_file,"r") as file:
#             for line in file:
#                 parts = line.strip().split("|")

#                 if len(parts) == 5:
#                     ticket = {
#                         "ticket_id": parts[0],
#                         "event_id": parts[1],
#                         "user_email": parts[2],
#                         "quantity": int(parts[3]),
#                         "date_purchased": parts[4]
#                     }
#                     tickets.append(ticket)
#     return tickets

# def save_new_ticket(ticket):
#     with open(Ticket_file,"w") as file:
#         for ticket in tickets:
#             file.write(f"{ticket['ticket_id']}|{ticket['event_id']}|{ticket['user_email']}|{ticket['quantity']}|{ticket['date_purchased']}\n")

# def overwrite_ticket_file(tickets):
#     with open(Ticket_file,"w") as file:
#         for ticket in tickets:
#             file.write(f"{ticket['ticket_id']}|{ticket['event_id']}|{ticket['user_email']}|{ticket['quantity']}|{ticket['date_purchased']}\n")

# def get_tickets_by_event(event_id):
#     all_tickets = load_all_tickets()
#     return [t for t in all_tickets if t["event_id"] == event_id]

# def get_total_seats_sold(event_id,):
#     tickets = get_tickets_by_event(event_id)
#     return sum(t["quantity"] for t in tickets)

# def buy_ticket(event_id, user_email, quantity):
#     ticket = {
#         "ticket_id": str(uuid.uuid4())[:8],   # short unique ID
#         "event_id":  event_id,
#         "user_email": user_email,
#         "quantity": quantity,
#         "date_purchased": datetime.now().strftime("%Y-%m-%d")  # today's date
#     }
#     save_new_ticket(ticket)
#     return ticket

# def cancel_ticket(ticket_id):
#     all_tickets = load_all_tickets()
#     target = None

#     for ticket in all_tickets:
#         if ticket["ticket_id"] == ticket_id:
#             target = ticket
#             break

#     if target is None:
#         return 0 
    
#     updated_tickets = [t for t in all_tickets if t["ticket_id"] != ticket_id]
#     overwrite_ticket_file(updated_tickets)

#     return target["quantity"]  
TICKET_FILE = "tickets.txt"
def save_all_tickets(tickets):
    with open(TICKET_FILE, "w") as f:
        for t in tickets:
            f.write(f"{t['ticket_id']} | {t['booking_id']} | {t['user_id']} | {t['event_id']}\n")
            
def load_all_tickets():
    if not os.path.exists(TICKET_FILE):
        return []

    tickets = []

    with open(TICKET_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")

            if len(parts) == 4:
                ticket_id, booking_id, user_id, event_id = parts

                tickets.append({
                    "ticket_id": ticket_id,
                    "booking_id": booking_id,
                    "user_id": user_id,
                    "event_id": event_id
                })

    return tickets
def generate_ticket_id(tickets):

    if not tickets:
        return "T001"

    ids = [int(t["ticket_id"][1:]) for t in tickets]
    next_id = max(ids) + 1

    return f"T{next_id:03d}"