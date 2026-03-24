
import os
from events.events import load_all_events, overwrite_event_file
from events.tickets import save_all_tickets,load_all_tickets,generate_ticket_id
BOOKING_FILE = "events/bookings.txt"
CANCELLED_FILE = "events/cancelled_bookings.txt"
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import inspect
from rich.rule import Rule
from datetime import datetime

def load_all_bookings():
    if not os.path.exists(BOOKING_FILE):
        return []

    bookings = []
    with open(BOOKING_FILE, "r") as f:
        lines = f.readlines()
        if len(lines) <= 1: 
            return []

        for line in lines[1:]: 
            parts = line.strip().split(" | ")

            if len(parts) >= 4:
                bookings.append({
                    "id": parts[0],
                    "user_id": parts[1],
                    "event_id": parts[2],
                    "quantity": int(parts[3]),
                    "date_booked": parts[4] if len(parts) > 4 else "2026-03-20",
                    "time_booked": parts[5] if len(parts) > 5 else "12:00:00"
                })
    return bookings

def save_all_bookings(bookings):
    with open(BOOKING_FILE, "w") as f:
        f.write("Booking ID | User ID | Event ID | Quantity | Date Booked | Time Booked\n")
        
        for b in bookings:
            line = f"{b['id']} | {b['user_id']} | {b['event_id']} | {b['quantity']} | {b['date_booked']} | {b['time_booked']}\n"
            f.write(line)

def save_all_cancelled_bookings(cancelled_tickets):
    with open(CANCELLED_FILE, "w") as f:
        f.write("Ticket_ID | Booking_ID | User_ID | Event_ID\n")

        for t in cancelled_tickets:
            f.write(
                f"{t['ticket_id']} | {t['booking_id']} | {t['user_id']} | {t['event_id']}\n"         
            )

def load_all_cancelled_bookings():
    if not os.path.exists(CANCELLED_FILE):
        return []

    cancelled = []
    with open(CANCELLED_FILE, "r") as f:
        header = f.readline() 
        
        for line in f:
            if not line.strip():
                continue
                
            parts = line.strip().split(" | ")

            if len(parts) >= 4:
                ticket_id, booking_id, user_id, event_id = parts[:4]

                cancelled.append({
                    "ticket_id": ticket_id,
                    "booking_id": booking_id,
                    "user_id": user_id,
                    "event_id": event_id,
                    "quantity": 1  
                })

    return cancelled

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
    console = Console()

    target_event = next((e for e in events if e["id"] == event_id), None)

    if not target_event:
        console.print(Panel("[bold red]❌ Event not found.[/]", border_style="red"))
        console.input("\n[bold cyan]Press Enter to return to Dashboard...[/]")
        return

    try:
        today = datetime.now().date()
        event_date = datetime.strptime(target_event["date"], "%Y-%m-%d").date()

        if event_date < today:
            console.print(Panel(
                f"[bold red]❌ BOOKING DENIED[/]\n\n"
                f"The event '[bold white]{target_event['title']}[/]' occurred on [cyan]{target_event['date']}[/].\n"
                "You cannot book tickets for past events.",
                title="Expired Event",
                border_style="red",
                expand=False
            ))
            console.input("\n[bold cyan]Press Enter to return to Dashboard...[/]")
            return
    except ValueError:
        console.print("[yellow]⚠ Warning: Event date format is invalid. Proceeding with caution...[/]")

    seats_available = int(target_event["seats_input"])

    if seats_available < quantity:
        console.print(Panel("[bold red]❌ Not enough seats available.[/]", border_style="red"))
        console.input("\n[bold cyan]Press Enter to return to Dashboard...[/]")
        return

    ticket_price = float(target_event["price"])
    total_price = ticket_price * quantity
  
    table = Table(title="Payment Table")
    table.add_column("Ticket Price", style="cyan")
    table.add_column("Quantity", justify="right", style="magenta")
    table.add_column("Total Price", justify="right", style="green")

    table.add_row(
        f"${ticket_price:.2f}", 
        str(quantity), 
        f"${total_price:.2f}"
    )

    console.print(table)
    while True:
        try:
            payment = float(input(f"Total is ${total_price:.2f}. Enter payment amount: $"))

            if payment >= total_price:
                change = payment - total_price
                print(f"Payment successful! Your change is: ${change:.2f}")
                break
            else:
                print(f"Payment not enough. You still owe ${total_price - payment:.2f}. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a numeric amount (e.g., 10.50).")

    now = datetime.now()
    date_booked = now.strftime("%Y-%m-%d") 
    time_booked = now.strftime("%H:%M:%S") 

    booking_id = generate_booking_id(bookings)

    # Add the date and time to the booking record
    bookings.append({
        "id": booking_id,
        "user_id": user_id,
        "event_id": event_id,
        "quantity": quantity,
        "date_booked": date_booked,  
        "time_booked": time_booked   
    })

    save_all_bookings(bookings)

    ticket_panels = []
    for i in range(quantity):
        ticket_id = generate_ticket_id(tickets)
        new_ticket = {
            "ticket_id": ticket_id,
            "booking_id": booking_id,
            "user_id": user_id,
            "event_id": event_id,
            "booked_at": f"{date_booked} {time_booked}" 
        }
        tickets.append(new_ticket)
        
        ticket_content = Text.assemble(("🎫 ", "yellow"), (ticket_id, "bold white"))
        ticket_panels.append(Panel(ticket_content, border_style="bright_blue", expand=False, subtitle=f"[dim]Qty: {i+1}/{quantity}[/]"))

    console.print("\n" + "━" * 30, style="dim")
    console.print("[bold reverse #6272a4]  YOUR TICKETS  [/]", justify="left")
    console.print("━" * 30 + "\n", style="dim")

    console.print(Columns(ticket_panels, padding=(0, 1)))
    console.print(f"\n[bold green]✔[/] {quantity} tickets added.\n")

    save_all_tickets(tickets)

    target_event["seats_input"] = str(seats_available - quantity)
    overwrite_event_file(events)

    print("\nBooking completed successfully.")
    console.input("\n[bold cyan]Press Enter to return to Dashboard...[/]")

def get_tickets_by_event(event_id):
    all_tickets = load_all_tickets()
    return [t for t in all_tickets if t["event_id"] == event_id]

def get_total_seats_sold(event_id,):
    tickets = get_tickets_by_event(event_id)
    return sum(t["quantity"] for t in tickets)

def cancel_ticket(user_id, ticket_id):
    console = Console()
    tickets = load_all_tickets()

    target = next((t for t in tickets if t["ticket_id"] == ticket_id and t["user_id"] == user_id), None)

    if not target:
        print("Ticket not found or does not belong to you.")
        console.input("\n[bold cyan]Press Enter to return to Dashboard...[/]")
        return

    events = load_all_events()
    event = next((e for e in events if e["id"] == target["event_id"]), None)

    if event:
        event["seats_input"] = str(int(event["seats_input"]) + 1)
        overwrite_event_file(events)

    # remove ticket from ticket list
    tickets = [t for t in tickets if t["ticket_id"] != ticket_id]
    save_all_tickets(tickets)

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
    console.input("\n[bold cyan]Press Enter to return to Dashboard...[/]")
    
def view_cancelled_bookings(user_id=None):
    console = Console()
    cancelled = load_all_cancelled_bookings()

    if not cancelled:
        console.print(Panel("No cancelled tickets found.", style="yellow", title="[bold]Notice[/]"))
        return

    table = Table(
        title="[bold red]CANCELLED TICKETS[/]", 
        caption="Review your cancellation history",
        border_style="dim red",
        header_style="bold red"
    )

    table.add_column("Ticket ID", style="dim cyan")
    table.add_column("Booking ID", style="dim white")
    table.add_column("User ID", style="dim white")
    table.add_column("Event ID", style="dim white")

    found_any = False
    for t in cancelled:
        if user_id and t["user_id"] != user_id:
            continue
        
        found_any = True
        table.add_row(
            t['ticket_id'], 
            str(t['booking_id']), 
            str(t['user_id']), 
            str(t['event_id'])
        )

    if found_any:
        console.print(table)
    else:
        console.print("[italic red]No matches found for your User ID.[/]")

def view_tickets(user_id=None):
    tickets = load_all_tickets()
    events = load_all_events()
    console = Console()

    console.print("\n[bold reverse #6272a4]  BOOKING HISTORY  [/]\n")

    ticket_cards = []
    found_any = False

    for idx, b in enumerate(tickets, 1):
        if user_id and b["user_id"] != user_id:
            continue
        
        found_any = True
        event = next((e for e in events if e["id"] == b["event_id"]), None)
        event_name = event["title"] if event else "N/A"

        ticket_content = (
            f"[bold white]TICKET ID :[/] [yellow]{b['ticket_id']}[/]\n"
            f"[bold white]EVENT     :[/] [green]{event_name}[/]\n"
            f"[dim]Booking: {b['booking_id']}[/]"
        )

        ticket_cards.append(
            Panel(
                ticket_content, 
                title=f"[bold]Ticket #{idx}[/]", 
                border_style="bright_blue",
                expand=False,
                width=35  
            )
        )

    if found_any:
        console.print(Columns(ticket_cards, padding=(1, 1)))
    else:
        console.print("[italic red]No bookings available.[/]")

def view_booking(user_id=None):
    bookings = load_all_bookings()
    events = load_all_events()
    tickets = load_all_tickets()
    console = Console()

    if not bookings:
        console.print("[bold yellow]No bookings found.[/]")
        return

    console.print("\n[bold reverse #6272a4]  📜 YOUR BOOKING HISTORY  [/]\n")

    for idx, b in enumerate(bookings, 1):
        if user_id and b["user_id"] != user_id:
            continue

        # Find the Event
        event = next((e for e in events if e["id"] == b["event_id"]), None)
        
        # Find ALL Ticket IDs linked to this Booking ID
        # use a list comprehension to get all matching IDs
        matching_tickets = [t['ticket_id'] for t in tickets if t['booking_id'] == b['id']]
        ticket_str = ", ".join(matching_tickets) if matching_tickets else "No tickets generated"

        event_info = ""
        if event:
            event_info = (
                f"\n[bold underline]Event Details[/]\n"
                f"Title      : [green]{event['title']}[/]\n"
                f"Date       : [cyan]{event['date']}[/]\n"
                f"Location   : {event['location']}\n"
                f"Price      : ${event['price']}"
            )

        content = Group(
            f"[bold white]Booking ID[/]  : {b['id']}",
            f"[bold white]User ID[/]     : {b['user_id']}",
            f"[bold white]Quantity[/]    : {b['quantity']}",
            f"[bold magenta]Ticket IDs[/]  : [orchid]{ticket_str}[/]", # Included Ticket IDs here
            Rule(style="dim"),
            event_info
        )

        console.print(Panel(
            content, 
            title=f"Booking #{idx}", 
            border_style="bright_blue",
            expand=False,
            padding=(1, 2)
        ))

    console.print("\n" + "━" * 40, style="dim")


   
