
from main.person import Person
from user.system_manager import SystemManager
from events.booking_file import cancel_ticket, create_booking, view_booking,view_cancelled_bookings,view_tickets
from admin.admin import view_events
from events.events import load_all_events
from main.password import password_strength_validation
from main.password_dot import get_password_with_dots
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.box import DOUBLE
from rich.box import ROUNDED
from rich.prompt import Prompt
from rich.progress import track
from rich.prompt import Confirm

console = Console()

class User(Person):
    system = SystemManager() 
    def __init__(self, user_id, name, email, password):
        super().__init__(name, email, password)  
        self.user_id = user_id
    
    def __str__(self):
        return f"[bold cyan]User ID:[/] {self.user_id} | [bold]Name:[/] {self.name}"

    def __repr__(self):
        return f"User(id='{self.user_id}', name='{self.name}')"
    
# -------------------------------
# Registration / Login
# -------------------------------
def register(system):
    users = system.load_users()
    # Dynamic ID generation
    user_id = f"U{len(users)+1:03d}"

    console.print("\n[bold cyan]✨ CREATE YOUR ACCOUNT[/]")
    console.print("[dim]Please fill in your details below[/]\n")

    # --- STEP 1: USERNAME ---
    while True:
        username = Prompt.ask("[bold white]Step 1/3:[/] Enter Username")
        if username in users:
            console.print("[italic red]⚠ This username is already taken. Try another.[/]")
            continue
        break

    # --- STEP 2: EMAIL ---
    email = Prompt.ask("[bold white]Step 2/3:[/] Enter Email Address")

    # --- STEP 3: PASSWORD ---
    while True:
        password = get_password_with_dots("Step 3/3: Enter Password:")
        
        # Validation feedback
        if password_strength_validation(password):
            with console.status("[bold green]Validating password strength...", spinner="point"):
                time.sleep(1)
            break
        else:
            # The validation function likely prints its own error, 
            # but we can add a general hint here.
            console.print("[dim red]Try a stronger password (e.g., 8+ chars, mix of types).[/]")

    # --- FINALIZING ---
    # Create a nice "saving" animation
    for _ in track(range(10), description="[cyan]Syncing with database..."):
        time.sleep(0.1)

    user_obj = User(user_id, username, email, password)
    system.append_user(user_obj)

    # Success Summary Panel
    success_text = Text.assemble(
        ("Welcome to the community, ", "white"),
        (f"{username}", "bold cyan"),
        ("!\n", "white"),
        (f"Your User ID is: ", "dim"),
        (f"{user_id}", "bold yellow")
    )
    
    console.print("\n")
    console.print(Panel(success_text, title="[bold green]Registration Successful[/]", border_style="green", expand=False))
    time.sleep(2)

    return user_obj

def login(system):
    users = system.load_users()
    attempt = 3

    while attempt > 0:
        # Create a header for the login attempt
        login_header = Text.assemble( 
            ("\n🔒 SECURITY ACCESS ", "bold yellow"),
            (f"| Attempt: {attempt}/3", "dim white")
        )
        console.print(login_header)
        
        # Using Rich Prompt for the username
        username = Prompt.ask("[bold cyan]Username[/]")
        
        # Use your existing dot function for the password
        password = get_password_with_dots("Password: ")
     
        if username in users and password == users[username]["password"]:
            # Success Animation
            with console.status("[bold green]Authenticating...", spinner="aesthetic"):
                time.sleep(1)
            
            console.print(f"\n[bold green]✔ Login successful![/] Welcome back, [bold cyan]{username}[/].")
            time.sleep(1)
            
            user_data = users[username]
            # Returning the User object
            return User(user_data["id"], username, user_data["email"], password)
        
        else:
            attempt -= 1
            if attempt > 0:
                # Warning for failed attempt
                error_msg = Text.assemble(
                    ("❌ Invalid credentials. ", "bold red"),
                    (f"{attempt} attempts remaining.", "italic white")
                )
                console.print(Panel(error_msg, border_style="red", expand=False))
            else:
                # Final lockout message
                console.print(Panel(
                    "[bold white on red] ACCESS BLOCKED [/]\n\nToo many failed attempts.", 
                    title="System Alert", 
                    border_style="bold red"
                ))
                time.sleep(2)

    return None

def forgot_password(system):
    users = system.load_users()
    
    # 1. Identification
    username = Prompt.ask("\n[bold yellow]Enter username for reset[/]").strip()

    if username not in users:
        console.print(Panel("[bold red]❌ User not found.[/]", border_style="red", expand=False))
        return

    # 2. Verified State
    console.print(f"[bold green]✔ Identity Verified:[/] Resetting password for [bold cyan]{username}[/]\n")

    # 3. Use your custom "Dot" input
    while True:
        new_pw = get_password_with_dots("Enter New Password: ")
        confirm_pw = get_password_with_dots("Confirm New Password: ")
        
        if new_pw == "":
            console.print("[bold red]❌ Password cannot be empty![/]")
            continue

        if new_pw != confirm_pw:
            console.print("[bold red]❌ Passwords do not match. Try again.[/]")
            continue
        break

    # 4. Save Logic
    with console.status("[bold yellow]Updating security records...", spinner="dots"):
        # 1. Update the password in the dictionary
        users[username]['password'] = new_pw
        
        # 2. Save the WHOLE dictionary back to the file
        system.save_all_users(users) 
        time.sleep(1.5)

    console.print("\n", Align.center(Panel("[bold green]SUCCESS![/] Your password has been updated.", border_style="green", expand=False)))

    # 7. Success Summary
    success_msg = Text.assemble(
        ("PASSWORD RESET SUCCESSFUL\n\n", "bold green"),
        ("The credentials for ", "white"),
        (f"{username}", "bold cyan"),
        (" have been updated. You can now log in with your new password.", "white")
    )

    console.print("\n", Align.center(
        Panel(
            success_msg, 
            title="🔐 SECURITY UPDATED", 
            border_style="bright_green", 
            expand=False,
            padding=(1, 2)
        )
    ))
    
    console.input("\n[dim]Press Enter to return to main menu...[/]")
# -------------------------------
# User Dashboard
# -------------------------------
def user_dashboard_menu(user_obj):
    while True:
        # 1. Refresh and Clear
        events = load_all_events() 
        os.system('cls' if os.name == 'nt' else 'clear')

        # 2. Personalized Header
        header_text = Text.assemble(
            (" Welcome back, ", "white"),
            (f"{user_obj.user_id}", "bold magenta"),
            ("! ", "white")
        )
        
        # 3. Menu Options - Categorized for better UX
        menu_content = Text()
        menu_content.append("\n [1] ", style="bold magenta")
        menu_content.append("Create New Booking      ", style="bold magenta")
        menu_content.append(" [2] ", style="bold red")
        menu_content.append("Cancel a Booking\n", style="bold red")
        
        menu_content.append(" [3] ", style="bold cyan")
        menu_content.append("Explore All Events      ", style="bold cyan")
        menu_content.append(" [4] ", style="bold green")
        menu_content.append("My Active Bookings\n", style="bold green")
        
        menu_content.append(" [5] ", style="bold yellow")
        menu_content.append("View Cancellation Log   ", style="bold yellow")
        menu_content.append(" [6] ", style="bold white")
        menu_content.append("Logout System\n", style="bold white")
        menu_content.append(" [7] ", style="bold red")
        menu_content.append("Shutdown System\n", style="bold red")

        # 4. Dashboard Panel
        dashboard_panel = Panel(
            Align.center(menu_content),
            title=header_text,
            subtitle="[dim]Kork Plus User Portal[/]",
            border_style="magenta",
            box=ROUNDED, # Rounded corners look friendlier for users
            width=max(50, min(90, int(console.width * 0.6)))
        )

        console.print("\n" * 2)
        console.print(Align.center(dashboard_panel))

        # 5. Input Prompt
        prompt_space = " " * (int(console.width / 2) - 12)
        choice = console.input(f"{prompt_space}[bold magenta]Action ❱ [/]").strip()

        # --- Logic Handling ---
        if choice == "1":
            view_events()
            event_id = console.input("\n[bold cyan]Enter Event ID (e.g., E001): [/]").strip().upper()
            qty_str = console.input("[bold cyan]Enter quantity: [/]").strip()
            if qty_str.isdigit():
                create_booking(user_obj.user_id, event_id, int(qty_str))
            else:
                console.print("[red]Invalid quantity![/]")
                time.sleep(1)

        elif choice == "2":
            view_tickets(user_obj.user_id)
            ticket_id = console.input("\n[bold red]Enter Ticket ID to cancel: [/]").strip().upper()
            cancel_ticket(user_obj.user_id, ticket_id)

        elif choice == "3":
            view_events()
            console.input("\n[dim]Press Enter to return to dashboard...[/]")

        elif choice == "4":
            view_booking(user_obj.user_id)
            console.input("\n[dim]Press Enter to return to dashboard...[/]")
            
        elif choice == "5":
            view_cancelled_bookings(user_obj.user_id)
            console.input("\n[dim]Press Enter to return to dashboard...[/]")

        elif choice == "6":
            with console.status("[bold red]Logging out...", spinner="dots"):
                time.sleep(1)
            break
        elif choice == "7":
            confirm = Confirm.ask("[bold red]Are you sure you want to SHUT DOWN the entire system?[/]")
            if confirm:
                console.print("\n[bold reverse red] SYSTEM SHUTDOWN INITIATED [/]")
                time.sleep(1)
                exit()
        else:
            console.print(Align.center("[bold white on red] INVALID CHOICE [/]"))
            time.sleep(1)

# -------------------------------
# Main Menu
# -------------------------------
def menu():
    system = SystemManager()

    while True:
        # 1. Clear screen for a fresh "App" feel
        os.system('cls' if os.name == 'nt' else 'clear')

        # 2. Setup Responsive Width
        menu_width = max(40, min(70, int(console.width * 0.5)))

        # 3. Design the Menu Content
        menu_content = Text()
        menu_content.append("\n") # Padding
        menu_content.append(" [1] ", style="bold cyan")
        menu_content.append("Create Account\n", style="white")
        menu_content.append(" [2] ", style="bold cyan")
        menu_content.append("Sign In\n", style="white")
        menu_content.append(" [3] ", style="bold yellow")
        menu_content.append("Forgot Password\n", style="white")
        menu_content.append(" [4] ", style="bold red")
        menu_content.append("Exit Program\n", style="white")
        menu_content.append("\n") # Padding

        # 4. Create the Panel
        main_panel = Panel(
            Align.center(menu_content),
            title="[bold reverse #6272a4]  WELCOME TO KORK PLUS  [/]",
            subtitle="[dim]Secure Event Booking Portal[/]",
            border_style="bright_blue",
            box=DOUBLE,
            width=menu_width
        )

        # 5. Display
        console.print("\n" * 3) # Top margin
        console.print(Align.center(main_panel))
        
        # 6. Styled Input
        # This calculates space to try and put the prompt near the center
        prompt_indent = " " * (int(console.width / 2) - 12)
        op = console.input(f"{prompt_indent}[bold yellow]Selection (1-4): [/]").strip()

        # --- Logic Handling ---
        if op == "1":
            user_obj = register(system)
            if user_obj: # Ensure registration was successful
                user_dashboard_menu(user_obj)
        elif op == "2":
            user_obj = login(system)
            if user_obj:
                user_dashboard_menu(user_obj)
        elif op == "3":
            forgot_password(system)
        elif op == "4":
            console.print("\n[bold red]Exiting the program. Goodbye![/]\n")
            break
        else:
            # Show a brief error message before the screen clears again
            console.print(Align.center("[bold red]⚠ Please choose option 1 - 4.[/]"))
            import time
            time.sleep(1.5)

if __name__ == "__main__":
    menu()


