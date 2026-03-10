from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Sample Table")

table.add_column("Name", style="cyan")
table.add_column("Age", justify="right", style="magenta")
table.add_column("City", style="green")

table.add_row("Alice", "24", "New York")
table.add_row("Bob", "30", "Los Angeles")
table.add_row("Charlie", "35", "San Francisco")

console.print(table)