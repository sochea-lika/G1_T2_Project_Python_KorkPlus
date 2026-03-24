from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def password_strength_validation(password):
    special_characters = "!@#$%^&*()"

    checks = {
        "Length (8+)": len(password) >= 8,
        "Lowercase": any(c.islower() for c in password),
        "Uppercase": any(c.isupper() for c in password),
        "Digit": any(c.isdigit() for c in password),
        "Special Character": any(c in special_characters for c in password)
    }

    if all(checks.values()):
        console.print("[bold green]✔ Password meets all security requirements![/]")
        return True

    feedback = Text()
    feedback.append("Password Security Requirements:\n\n", style="bold white")

    for requirement, passed in checks.items():
        icon = "✅" if passed else "❌"
        color = "green" if passed else "red"
        feedback.append(f"{icon} {requirement}\n", style=color)

    console.print(Panel(
        feedback, 
        title="[bold red]Weak Password[/]", 
        border_style="red",
        expand=False
    ))
    
    return False