from admin.admin import main as admin_menu  # your existing admin panel
from user.user import menu as user_menu   # your user registration/login + dashboard
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import DOUBLE
import os
import time

console = Console()

def main():
    while True:
        # 1. Clear the screen so the menu always stays at the top
        os.system('cls' if os.name == 'nt' else 'clear')

        # Calculate responsive width
        dynamic_width = max(40, min(80, int(console.width * 0.5)))

        # 2. Build Menu Content
        menu_content = Text()
        menu_content.append("\n") 
        menu_content.append(" [1] ", style="bold yellow")
        menu_content.append("ADMIN DASHBOARD\n", style="bold yellow")
        menu_content.append("\n [2] ", style="bold green")
        menu_content.append("USER DASHBOARD\n", style="bold green")
        menu_content.append("\n [3] ", style="bold red")
        menu_content.append("QUIT SYSTEM\n", style="bold red")
        menu_content.append("\n") 

        # 3. Create the Panel
        menu_panel = Panel(
            Align.center(menu_content),
            title="[bold reverse #6272a4]  KORK PLUS EVENT SYSTEM  [/]",
            subtitle="[italic dim]Select an option to continue[/]",
            width=dynamic_width,
            border_style="bright_blue",
            box=DOUBLE 
        )

        # 4. Print layout
        console.print("\n" * 2) 
        console.print(Align.center(menu_panel))
        
        # 5. Styled Prompt - Indented to look centered under the panel
        prompt_space = " " * (int(console.width / 2) - 12)
        choice = console.input(f"{prompt_space}[bold yellow]❱❱ Choice (1-3): [/]").strip()

        if choice == "1":
            try:
                admin_menu()
            except KeyboardInterrupt:
                console.print("\n[bold red]Terminating system... Goodbye![/]")
                exit() 
        elif choice == "2":
            user_menu()
        elif choice == "3":
            # A nice exit message
            console.print(Align.center("\n[bold red]Shutting down... Goodbye![/]\n"))
            break
        else:
            # Error message that actually stays on screen for a second
            console.print(Align.center("[bold white on red] INVALID OPTION [/] [red] Please choose 1-3[/]"))
            time.sleep(1.2)

if __name__ == "__main__":
    main()
