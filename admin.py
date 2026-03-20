import uuid 
from admin_file import Admin, load_all_admins, save_new_admin, overwrite_admin_file, find_admin_by_email
from events import load_all_events, save_new_event, overwrite_event_file,is_valid_date
from password import password_strength_validation
# from tickets import get_tickets_by_event,get_total_seats_sold,load_all_tickets,cancel_ticket
from booking_file import get_tickets_by_event, get_total_seats_sold
from tickets import load_all_tickets
from password_dot import get_password_with_dots
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track, Progress, BarColumn, TextColumn
from rich.text import Text
from rich.align import Align
import os
from rich.table import Table
from rich.prompt import Confirm
from rich.box import DOUBLE_EDGE
from rich.columns import Columns
from rich.spinner import SPINNERS
from booking_file import load_all_bookings

console = Console()

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
    # Header for the Admin Registration
    console.print("\n" + "━" * 40, style="bright_blue")
    console.print("[bold gold1] 🔑 ADMIN ACCOUNT CREATION [/]", justify="center")
    console.print("━" * 40 + "\n", style="bright_blue")

    # 1. Get Admin Details using Rich Prompt
    name = Prompt.ask("[bold white]Username[/]").strip()
    email = Prompt.ask("[bold white]Admin Email[/]").strip()

    # 2. Duplicate Check
    if find_admin_by_email(email):
        console.print(Panel(
            f"[bold red]Error:[/] The email [italic cyan]{email}[/] is already registered to an administrator.",
            title="Duplicate Admin",
            border_style="red",
            expand=False
        ))
        return
    
    # 3. Secure Password Input
    while True:
        password = get_password_with_dots("Choose Admin Password:").strip()
        # This will call the styled validation function we created earlier
        if password_strength_validation(password):
            break
    
    # 4. "Saving" Animation for a professional feel
    print("\n")
    for _ in track(range(10), description="[bold blue]Encrypting and Saving Admin Data..."):
        time.sleep(0.1)
    
    # 5. Save Logic
    new_admin = Admin(name, email, password)
    save_new_admin(new_admin)

    # 6. Success Message in a Panel
    success_msg = Text.assemble(
        ("SUCCESS\n", "bold green"),
        ("Admin ", "white"), (f"{name}", "bold cyan"),
        (" has been granted system privileges.", "white")
    )
    
    console.print("\n")
    console.print(Panel(
        success_msg, 
        border_style="bright_blue", 
        title="[bold green]Registration Complete[/]",
        expand=False
    ))
    time.sleep(2)

def sign_in():
    # 1. Clear the screen for a clean terminal look
    os.system('cls' if os.name == 'nt' else 'clear')

    # 2. Create a "Secure Terminal" Header
    header = Panel(
        Align.center("[bold yellow]ADMINISTRATOR ACCESS CONTROL[/]"),
        style="on #282a36", # Dark background
        border_style="bright_blue"
    )
    console.print("\n", header)

    # 3. Get Credentials
    # Using Prompt.ask for a more integrated feel
    email = Prompt.ask("[bold cyan]Institutional Email[/]").strip()
    password = get_password_with_dots("Security Password: ").strip()

    # 4. Verification Logic
    admin = find_admin_by_email(email)
    
    # Simulate a "Security Handshake"
    with console.status("[bold blue]Verifying encrypted credentials...", spinner="bouncingBar"):
        time.sleep(1.2)

    if admin and admin.check_password(password):
        # Success Layout
        success_text = Text.assemble(
            ("✔ ACCESS GRANTED\n", "bold green"),
            ("Welcome, Administrator ", "white"),
            (f"{admin.name}", "bold cyan")
        )
        console.print("\n", Align.center(Panel(success_text, border_style="green", expand=False)))
        time.sleep(1.5)
        return admin
    else:
        # Failure Layout
        error_text = Text.assemble(
            ("✘ ACCESS DENIED\n", "bold red"),
            ("Invalid authentication parameters. Your attempt has been logged.", "dim white")
        )
        console.print("\n", Align.center(Panel(error_text, border_style="red", expand=False)))
        time.sleep(2)
        return None
    
def forget_password():
    console.print("\n[bold yellow]🔐 ADMIN PASSWORD RECOVERY[/]")
    console.print("[dim]Identify your account to continue[/]\n")

    email = Prompt.ask("[bold white]Registered Admin Email[/]").strip()
     
    # 1. Load and Search
    all_admins = load_all_admins()
    target_admin = None

    # UPDATED: Changed spinner="search" to spinner="dots"
    with console.status("[bold blue]Searching encrypted database...", spinner="dots"):
        time.sleep(1)
        for admin in all_admins:
            if admin.get_email() == email:
                target_admin = admin
                break
    
    # 2. Handle User Not Found
    if target_admin is None:
        console.print(Panel(
            f"[bold red]✘ Error:[/] No administrator found with email: [italic cyan]{email}[/]",
            title="Search Failed",
            border_style="red",
            expand=False
        ))
        return

    # 3. User Found
    console.print(f"[bold green]✔ Identity Verified:[/] Account linked to [bold cyan]{target_admin.name}[/]\n")

    while True:
        new_password = Prompt.ask("[bold white]Enter New Password[/]", password=True).strip()
        confirm_password = Prompt.ask("[bold white]Confirm New Password[/]", password=True).strip()
        
        if new_password != confirm_password:
            console.print("[bold red]❌ Passwords do not match. Please try again.[/]")
            continue

        if password_strength_validation(new_password):
            break

    # 4. Finalizing
    # UPDATED: Changed spinner="aesthetic" to spinner="dots"
    with console.status("[bold yellow]Updating security records...", spinner="dots"):
        target_admin.set_password(new_password)
        overwrite_admin_file(all_admins)
        time.sleep(1.5)

    # 5. Success Summary
    success_msg = Text.assemble(
        ("PASSWORD RESET SUCCESSFUL\n", "bold green"),
        ("The credentials for ", "white"),
        (f"{target_admin.name}", "bold cyan"),
        (" have been updated in the master file.", "white")
    )

    console.print("\n", Panel(success_msg, border_style="green", expand=False))
    console.input("\n[dim]Press Enter to return to main menu...[/]")

def add_event():
    # 1. Header and Auto-generated ID
    event_id = generate_event_id()
    
    console.print("\n" + "━" * 50, style="bright_blue")
    console.print(f"[bold gold1] 📅 CREATE NEW EVENT [/] [dim]| System ID: {event_id}[/]", justify="center")
    console.print("━" * 50 + "\n", style="bright_blue")

    # 2. Basic Information
    title = Prompt.ask("[bold white]Event Title[/]").strip()

    while True:
        date = Prompt.ask("[bold white]Date[/] [dim](YYYY-MM-DD)[/]").strip()
        if is_valid_date(date): # Using your styled validation
            break

    location = Prompt.ask("[bold white]Location[/]").strip()
    description = Prompt.ask("[bold white]Description[/]").strip()
    price = Prompt.ask("[bold white]Ticket Price[/] [dim]($)[/]").strip()

    # 3. Numeric Validation for Seats
    while True:
        seats_input = Prompt.ask("[bold white]Total Seats Available[/]").strip()
        if seats_input.isdigit() and int(seats_input) > 0:
            seats = int(seats_input)
            break
        console.print("[bold red]⚠ Invalid Input:[/] Please enter a positive whole number for seats.")

    # 4. "Creation" Animation
    print("\n")
    for _ in track(range(15), description="[bold blue]Registering event in database..."):
        time.sleep(0.05)

    # 5. Data Structuring
    new_event = {
        "id": event_id,
        "title": title,
        "date": date,
        "location": location,
        "description": description,
        "price": price,
        "seats_input": seats_input,
        "seat_total": seats_input
    }

    save_new_event(new_event)

    # 6. Success Card
    success_card = Text.assemble(
        ("EVENT CREATED SUCCESSFULLY\n\n", "bold green"),
        ("ID      : ", "dim"), (f"{event_id}\n", "bold yellow"),
        ("Title   : ", "dim"), (f"{title}\n", "white"),
        ("Capacity: ", "dim"), (f"{seats_input} seats", "cyan")
    )

    console.print("\n", Panel(
        success_card, 
        border_style="green", 
        title="[bold]System Update[/]", 
        expand=False
    ))
    time.sleep(2)

def view_events():
    events = load_all_events()
    
    if not events:
        console.print(Panel("[bold red]No events found in the database.[/]", border_style="red"))
        return

    # 1. Create the Table (SUBTITLE REMOVED TO PREVENT CRASH)
    table = Table(
        title="[bold reverse #6272a4]  AVAILABLE EVENTS  [/]",
        header_style="bold cyan",
        border_style="bright_blue",
        show_lines=True 
    )

    # 2. Add Columns
    table.add_column("#", justify="center", style="dim")
    table.add_column("ID", style="bold yellow")
    table.add_column("Title", style="white")
    table.add_column("Date", justify="center")
    table.add_column("Location", style="italic")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Seats", justify="center")

    # 3. Add Rows
    for i, event in enumerate(events, start=1):
        remaining = int(event.get('seats_input', 0))
        total = int(event.get('seat_total', 0))
        
        seat_style = "bold red" if remaining < 10 else "green"
        seat_display = f"[{seat_style}]{remaining}[/]/{total}"

        table.add_row(
            str(i),
            event['id'],
            event['title'],
            event['date'],
            event['location'],
            f"${event['price']}",
            seat_display
        )

    # 4. Print the table and then the subtitle separately
    console.print("\n")
    console.print(table)
    # This replaces the 'subtitle' argument you had earlier
    console.print(Align.center("[dim]Showing all currently registered events[/]"))
    console.print("\n")

def edit_event():
    console.print("\n[bold yellow]📝 EDIT EVENT MODULE[/]")
    events = load_all_events()
    
    if not events:
        console.print("[bold red]No events available to edit.[/]")
        return

    # 1. Search for Event
    event_id = Prompt.ask("[bold white]Enter Event ID to edit[/] [dim](e.g., E001)[/]").strip()

    target_event = next((e for e in events if e["id"] == event_id), None)

    if not target_event:
        console.print(Panel(f"[bold red]✘ Error:[/] Event [italic]{event_id}[/] not found.", border_style="red", expand=False))
        return

    # 2. Display Current Info in a mini-table
    console.print("\n[bold cyan]Current Event Details:[/]")
    info_table = Table(box=None, padding=(0, 2), show_header=False)
    info_table.add_row("[dim]Title:[/]", target_event['title'])
    info_table.add_row("[dim]Date:[/]", target_event['date'])
    info_table.add_row("[dim]Location:[/]", target_event['location'])
    console.print(info_table)
    
    console.print("\n[italic dim]Press Enter to keep the current value.[/]\n")

    # 3. Dynamic Updating using Prompt placeholders
    new_title = Prompt.ask(f"Title", default=target_event['title']).strip()
    
    while True:
        new_date = Prompt.ask(f"Date", default=target_event['date']).strip()
        # Validation check: if it's the same as before, skip validation
        if new_date == target_event['date'] or is_valid_date(new_date):
            break

    new_location = Prompt.ask(f"Location", default=target_event['location']).strip()
    new_description = Prompt.ask(f"Description", default=target_event['description']).strip()
    new_price = Prompt.ask(f"Price", default=target_event['price']).strip()
    new_seat = Prompt.ask(f"Total Seats", default=target_event['seat_total']).strip()

    # 4. Assigning values
    target_event["title"] = new_title
    target_event["date"] = new_date
    target_event["location"] = new_location
    target_event["description"] = new_description
    target_event["price"] = new_price
    target_event["seat_total"] = new_seat

    # 5. Save and Animation (SPINNER CHANGED TO 'dots')
    # Use 'dots' or 'aesthetic' for maximum compatibility
    with console.status("[bold yellow]Overwriting records...", spinner="dots"):
        overwrite_event_file(events)
        time.sleep(1.2)

    success_msg = Text.assemble(
        ("✔ UPDATE COMPLETE\n", "bold green"),
        ("Event ", "white"), (f"{event_id}", "bold cyan"),
        (" has been successfully modified.", "white")
    )
    
    console.print("\n", Panel(success_msg, border_style="green", expand=False))
    time.sleep(1.5)

def delete_event():
    console.print("\n[bold red]🗑 DELETE EVENT MODULE[/]")
    events = load_all_events()
    
    if not events:
        console.print("[bold yellow]No events found to delete.[/]")
        return
    
    # 1. Ask for ID
    event_id = console.input("\n[bold white]Enter Event ID to [red]DELETE[/]: [/]").strip()
    
    # 2. Find the event to show the admin WHAT they are deleting
    target_event = next((e for e in events if e["id"] == event_id), None)

    if not target_event:
        console.print(Panel(f"[bold red]✘ Error:[/] Event [italic]{event_id}[/] not found.", border_style="red", expand=False))
        return

    # 3. Warning Display
    warning_text = Text.assemble(
        ("⚠ WARNING: ", "bold red"),
        ("You are about to permanently delete:\n\n", "white"),
        (f"ID    : {target_event['id']}\n", "bold yellow"),
        (f"TITLE : {target_event['title']}\n", "bold yellow"),
        ("\nThis action cannot be undone!", "italic dim")
    )
    
    console.print("\n", Panel(warning_text, border_style="bold red", title="[blink red]CRITICAL ACTION[/]"))

    # 4. Confirmation Prompt
    # Confirm.ask is a Rich tool that forces a (y/n) response
    if Confirm.ask(f"[bold red]Are you absolutely sure you want to delete this event?[/]"):
        
        # 5. Execute Delete
        updated_events = [event for event in events if event["id"] != event_id]
        
        with console.status("[bold red]Purging record from database...", spinner="material"):
            overwrite_event_file(updated_events)
            time.sleep(1.5)

        console.print(f"\n[bold green]✔ Success:[/] Event [bold cyan]{event_id}[/] has been removed.")
    else:
        console.print("\n[bold blue]Deletion cancelled.[/] No changes were made.")
    
    time.sleep(1.5)

def view_admins():
    # 1. Load Data
    admins = load_all_admins()
    
    if not admins:
        console.print(Panel("[bold red]No administrators found in the database.[/]", border_style="red"))
        return

    # 2. Create the Admin Table (SUBTITLE REMOVED TO PREVENT TypeError)
    table = Table(
        title="[bold reverse #6272a4]  ADMINISTRATOR DIRECTORY  [/]",
        header_style="bold yellow",
        border_style="bright_blue",
        show_lines=True
    )

    # 3. Add Columns
    table.add_column("No.", justify="center", style="dim", width=4)
    table.add_column("Full Name", style="bold white", width=20)
    table.add_column("Email Address", style="cyan", width=25)
    table.add_column("Access Level", justify="center")

    # 4. Add Rows
    for i, admin in enumerate(admins, start=1):
        # Determine tag
        access_tag = "[bold green]System Admin[/]" if i == 1 else "[white]Staff[/]"
        
        table.add_row(
            str(i),
            admin.name,
            admin.get_email(),
            access_tag
        )

    # 5. Display (Using the safe 'dots' spinner)
    with console.status("[bold blue]Fetching directory...", spinner="dots"):
        time.sleep(1) 
        console.print("\n")
        console.print(table)
        # Manually print the "subtitle" info here
        console.print(Align.center(f"[dim]Total Records: {len(admins)}[/]"))
        console.print("\n")

def view_tickets():
    events = load_all_events()
    
    if not events:
        console.print(Panel("[bold red]No events found in the database.[/]", border_style="red"))
        return

    # 1. Create a Table (No subtitle argument here to avoid crashes)
    table = Table(
        title="[bold reverse #6272a4]  TICKET SALES OVERVIEW  [/]",
        header_style="bold cyan",
        border_style="bright_blue",
        expand=True
    )

    # 2. Define Columns
    table.add_column("Event Title", style="white", width=25)
    table.add_column("Sales Progress", width=30)
    table.add_column("Sold", justify="right", style="green")
    table.add_column("Remaining", justify="right", style="yellow")
    table.add_column("Status", justify="center")

    # 3. Populate Rows
    for event in events:
        total = int(event.get("seat_total", 0))
        remaining = int(event.get("seats_input", 0))
        sold = total - remaining
        percentage = (sold / total) if total > 0 else 0
        
        bar_width = 10
        filled = int(percentage * bar_width)
        bar = f"[green]{'━' * filled}[/][white]{'━' * (bar_width - filled)}[/]"
        
        if remaining == 0:
            status = "[bold red]SOLD OUT[/]"
        elif percentage > 0.8:
            status = "[bold orange1]ALMOST FULL[/]"
        else:
            status = "[bold green]OPEN[/]"

        table.add_row(
            f"{event['title']}\n[dim]{event['id']}[/]",
            f"{bar} [dim]{int(percentage*100)}%[/]",
            str(sold),
            str(remaining),
            status
        )

    # 4. Display (Using the standard 'dots' spinner)
    with console.status("[bold blue]Generating sales report...", spinner="dots"):
        time.sleep(1)
        console.print("\n", table)
        # Manually print the subtitle to be safe
        console.print(Align.center("[dim]Live ticket sales and availability data[/]\n"))

def admin_health_check():
    # 1. Calculate Actual Revenue (Re-using your existing logic)
    bookings = load_all_bookings()
    events = load_all_events()
    price_map = {e["id"]: float(e["price"]) for e in events}
    
    total_rev = 0
    for b in bookings:
        event_id = b["event_id"]
        if event_id in price_map:
            total_rev += int(b["quantity"]) * price_map[event_id]

    # 2. Get Top Performer
    sales_count = {}
    for b in bookings:
        e_id = b["event_id"]
        sales_count[e_id] = sales_count.get(e_id, 0) + int(b["quantity"])
    
    # Sort events by sales to find the top one
    sorted_events = sorted(events, key=lambda e: sales_count.get(e["id"], 0), reverse=True)
    top_event_title = sorted_events[0]["title"] if sorted_events else "N/A"

    # 3. Critical Seats (Events with less than 5 seats left)
    low_seats_count = len([e for e in events if int(e['seats_input']) < 5])

    # 4. Create the "Health" Table
    health_table = Table(box=None, show_header=False)
    
    # Adding the rows with the variables we just calculated
    health_table.add_row("💰 [bold white]Total Revenue:[/]", f"[green]${total_rev:,.2f}[/]")
    health_table.add_row("🔥 [bold white]Top Seller:[/]", f"[cyan]{top_event_title}[/]")
    health_table.add_row("⚠️  [bold white]Critical Seats:[/]", f"[red]{low_seats_count} Events almost sold out[/]")

    console.print(Panel(
        health_table, 
        title="[bold blue]SYSTEM HEALTH AT A GLANCE[/]", 
        border_style="blue",
        expand=False
    ))

def admin_dashboard(logged_in_admin):
    while True:
        # 1. Refresh Screen
        os.system('cls' if os.name == 'nt' else 'clear')

        admin_health_check()

        # 2. Top Status Bar
        status_text = Text.assemble(
            (" ADMIN SESSION ACTIVE ", "bold white on blue"),
            (f"  👤 User: {logged_in_admin.name} ", "bold blue"),
            (f"  📅 {time.strftime('%Y-%m-%d')}", "dim blue")
        )
        console.print(status_text, justify="right")
        console.print("━" * console.width, style="blue")

        # 3. Create Categorized Menu Content
        # Category A: Event Management
        event_mgmt = Text()
        event_mgmt.append("\n [1] ", style="bold yellow")
        event_mgmt.append("Add New Event\n")
        event_mgmt.append(" [2] ", style="bold yellow")
        event_mgmt.append("Edit Existing\n")
        event_mgmt.append(" [3] ", style="bold yellow")
        event_mgmt.append("Browse Events\n")
        event_mgmt.append(" [4] ", style="bold red")
        event_mgmt.append("Delete Event\n")

        # Category B: Ticketing & Data
        ticket_data = Text()
        ticket_data.append("\n [5] ", style="bold cyan")
        ticket_data.append("Sales Overview\n")
        ticket_data.append(" [6] ", style="bold red")
        ticket_data.append("Cancel Ticket\n")
        ticket_data.append(" [7] ", style="bold cyan")
        ticket_data.append("Admin Accounts\n")
        ticket_data.append(" [8] ", style="bold green")
        ticket_data.append("Analysis Event\n")

        # Category C: Session
        session_mgmt = Text()
        session_mgmt.append("\n [9] ", style="bold white")
        session_mgmt.append("Logout\n")
        session_mgmt.append(" [10] ", style="bold bright_red")
        session_mgmt.append("Shutdown System\n")

        # 4. Build Panels for a "Dashboard" Look
        # Using a width that allows them to sit side-by-side
        p1 = Panel(event_mgmt, title="[bold yellow]EVENT MGMT[/]", border_style="yellow", width=30)
        p2 = Panel(ticket_data, title="[bold cyan]TICKETS & USERS[/]", border_style="cyan", width=30)
        p3 = Panel(session_mgmt, title="[bold white]SESSION[/]", border_style="white", width=30)

        # 5. Display the Grid
        console.print("\n")
        console.print(Align.center(Columns([p1, p2, p3])))
        console.print("\n" + "━" * console.width, style="blue")

        # 6. Styled Input
        prompt_indent = " " * (int(console.width / 2) - 15)
        option = console.input(f"{prompt_indent}[bold yellow]Admin Action ❱ [/]").strip()

        # --- Logic Handling ---
        if option == "1":
            add_event()
        elif option == "2":
            edit_event()
        elif option == "3":
            view_events()
            console.input("\n[dim]Press Enter to return...[/]")
        elif option == "4":
            delete_event()
        elif option == "5":
            view_tickets()
            console.input("\n[dim]Press Enter to return...[/]")
        elif option == "6":
            # cancel_ticket_action()
            console.print("[yellow]Feature coming soon...[/]")
            time.sleep(1)
        elif option == "7":
            view_admins()
            console.input("\n[dim]Press Enter to return...[/]")
        elif option == "8":
            from analyze import menu_analyze
            menu_analyze()
            console.input("\n[dim]Press Enter to return...[/]")
        elif option == "9":
            console.print("\n[bold blue]Ending session... Goodbye![/]")
            time.sleep(1)
            return  
        elif option == "10":
            confirm = Confirm.ask("[bold red]Are you sure you want to SHUT DOWN the entire system?[/]")
            if confirm:
                console.print("\n[bold reverse red] SYSTEM SHUTDOWN INITIATED [/]")
                time.sleep(1)
                exit()
        else:
            console.print(Align.center("[bold white on red] INVALID SELECTION [/]"))
            time.sleep(1)


# =============================================
# MAIN MENU
# First screen the user sees when running the program
# =============================================

def main():
    while True:
        # 1. Clear Screen for that "App" feel
        os.system('cls' if os.name == 'nt' else 'clear')

        # 2. Dynamic Width Calculation (50% of terminal)
        dynamic_width = max(40, min(75, int(console.width * 0.5)))

        # 3. Design the Admin Entry Menu
        menu_content = Text()
        menu_content.append("\n") # Top Padding
        menu_content.append(" [1] ", style="bold cyan")
        menu_content.append("REGISTER NEW ADMIN\n", style="white")
        menu_content.append("\n [2] ", style="bold cyan")
        menu_content.append("ADMINISTRATOR LOGIN\n", style="white")
        menu_content.append("\n [3] ", style="bold yellow")
        menu_content.append("RECOVER PASSWORD\n", style="white")
        menu_content.append("\n [4] ", style="bold red")
        menu_content.append("EXIT SYSTEM\n", style="white")
        menu_content.append("\n") # Bottom Padding

        # 4. Create the Panel with a "High-Security" box style
        entry_panel = Panel(
            Align.center(menu_content),
            title="[bold reverse #1e1e2e] 🛡️  ADMIN MANAGEMENT SYSTEM  [/]",
            subtitle="[italic dim]Authorized Access Only[/]",
            width=dynamic_width,
            border_style="bright_blue",
            box=DOUBLE_EDGE # Uses a thick, double-edge border for impact
        )

        # 5. Print Layout
        console.print("\n" * 3) # Push down from top
        console.print(Align.center(entry_panel))
        
        # 6. Centered Input Prompt
        # Math to keep the prompt roughly centered under the panel
        indent = " " * (int(console.width / 2) - 12)
        option = console.input(f"\n{indent}[bold cyan]Security Action ❱ [/]").strip()

        # --- Logic Handling ---
        if option == "1":
            register()

        elif option == "2":
            logged_in_admin = sign_in()
            if logged_in_admin:
                # This opens your categorized admin_dashboard
                admin_dashboard(logged_in_admin)

        elif option == "3":
            forget_password()

        elif option == "4":
            console.print(Align.center("\n[bold red]System Offline. Goodbye![/]\n"))
            break

        else:
            console.print(Align.center("[bold white on red] INVALID SELECTION [/]"))
            time.sleep(1.2)


# Run the program
if __name__ == "__main__":
    main()
