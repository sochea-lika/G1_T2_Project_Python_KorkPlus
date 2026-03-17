import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

console = Console()

Event_file = "event.txt"
def load_all_events():
    events = []
    if os.path.exists(Event_file):
        with open(Event_file,"r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 8:
                    event ={
                        "id" : parts[0],
                        "title" : parts[1],
                        "date": parts[2],
                        "location":parts[3],
                        "description": parts[4],
                        "price": parts[5],
                        "seats_input":int(parts[6]),
                        "seat_total"  : int(parts[7]) 
                    }
                    events.append(event)
    return events

def save_new_event(event):
    with open(Event_file, "a") as file:
        file.write(f"{event['id']}|{event['title']}|{event['date']}|{event['location']}|{event['description']}|{event['price']}|{event['seats_input']}|{event['seat_total']}\n")

def overwrite_event_file(events):
     with open(Event_file, "w") as file:
        for event in events:
            file.write(f"{event['id']}|{event['title']}|{event['date']}|{event['location']}|{event['description']}|{event['price']}|{event['seats_input']}|{event['seat_total']}\n")
            
def is_valid_date(date_text):
    # Check if date matches YYYY-MM-DD format
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        # Create a stylized error message
        error_content = Text.assemble(
            ("📅 ", "yellow"),
            ("Invalid Date Format!\n", "bold white"),
            ("Expected: ", "dim"), ("YYYY-MM-DD", "bold cyan"),
            ("\nExample : ", "dim"), ("2026-03-16", "green")
        )

        console.print(Panel(
            error_content,
            title="[bold red]Format Error[/]",
            border_style="red",
            expand=False
        ))
        return False