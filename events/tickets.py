import os

TICKET_FILE = "events/tickets.txt"

def save_all_tickets(tickets):
    with open(TICKET_FILE, "w") as f:
        # 1. Write the Header
        f.write("Ticket ID | Booking ID | User ID | Event ID\n")
        
        # 2. Write the Data
        for t in tickets:
            f.write(f"{t['ticket_id']} | {t['booking_id']} | {t['user_id']} | {t['event_id']}\n")
            
def load_all_tickets():
    if not os.path.exists(TICKET_FILE):
        return []

    tickets = []

    with open(TICKET_FILE, "r") as f:
        lines = f.readlines()
        
        # 3. Skip header if file has data
        if len(lines) <= 1:
            return []

        for line in lines[1:]:
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

