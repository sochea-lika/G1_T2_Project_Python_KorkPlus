from booking_file import load_all_bookings
from events import load_all_events

from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.progress import BarColumn, Progress, TextColumn

console = Console()

def calculate_total_revenue():
    # 1. Load Data
    bookings = load_all_bookings()
    events = load_all_events()
    
    # 2. Calculation Logic
    price_map = {e["id"]: float(e["price"]) for e in events}
    
    total = 0
    total_tickets = 0
    
    for b in bookings:
        event_id = b["event_id"]
        qty = int(b["quantity"])
        if event_id in price_map:
            total += qty * price_map[event_id]
            total_tickets += qty
            
    # 3. Design the Revenue Card
    revenue_text = Text.assemble(
        ("TOTAL REVENUE\n", "bold cyan"),
        (f"${total:,.2f}", "bold green underline"),
        (f"\n\nTickets Sold: ", "dim white"),
        (f"{total_tickets}", "bold yellow")
    )

    # 4. Display as a centered "Stat Card"
    console.print("\n")
    console.print(Align.center(
        Panel(
            revenue_text,
            title="[bold gold1] 💵 FINANCIAL SUMMARY [/]",
            border_style="bright_blue",
            padding=(1, 4),
            expand=False
        )
    ))

    # 5. Pause to prevent screen clearing (Crucial!)
    console.input("\n[dim]Press Enter to return to Admin Dashboard...[/]")


def view_top_events():
    bookings = load_all_bookings()
    events = load_all_events()
    
    # 1. Count tickets per event
    sales_count = {}
    for b in bookings:
        e_id = b["event_id"]
        sales_count[e_id] = sales_count.get(e_id, 0) + int(b["quantity"])
        
    # 2. Setup the Table
    table = Table(
        title="[bold reverse #6272a4]  SALES PERFORMANCE REPORT  [/]",
        header_style="bold cyan",
        border_style="bright_blue",
        show_lines=True,
        expand=True
    )

    table.add_column("Event Title", style="white", width=25)
    table.add_column("Sold / Capacity", justify="center")
    table.add_column("Fill Rate %", justify="center")
    table.add_column("Performance Status", justify="center")

    # 3. Calculate and Populate
    for e in events:
        sold = sales_count.get(e["id"], 0)
        # Assuming 'seat_total' is the original capacity
        capacity = int(e.get("seat_total", 0)) 
        fill_rate = (sold / capacity * 100) if capacity > 0 else 0
        
        # Determine Color and Status based on performance
        if fill_rate >= 90:
            status = "[bold reverse green] 🔥 TOP SELLER [/]"
            color = "green"
        elif fill_rate >= 50:
            status = "[bold blue]STABLE[/]"
            color = "blue"
        elif fill_rate > 0:
            status = "[bold yellow]GROWING[/]"
            color = "yellow"
        else:
            status = "[dim red]NO SALES[/]"
            color = "red"

        # Create a visual percentage string
        fill_display = f"[{color}]{fill_rate:.1f}%[/]"
        
        table.add_row(
            f"{e['title']}\n[dim]{e['id']}[/]",
            f"{sold} / {capacity}",
            fill_display,
            status
        )

    # 4. Display
    console.print("\n")
    console.print(table)
    console.input("\n[bold cyan]Press Enter to return to Admin Dashboard...[/]")

from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

def view_sales_extremes():
    bookings = load_all_bookings()
    events = load_all_events()
    
    if not events:
        console.print("[bold red]No events found.[/]")
        return

    # 1. Map Sales Quantity
    sales_map = {e["id"]: 0 for e in events}
    for b in bookings:
        e_id = b["event_id"]
        if e_id in sales_map:
            sales_map[e_id] += int(b["quantity"])
    
    # 2. Pair titles with sales and sort
    # results = [('Title', qty), ...]
    results = []
    for e in events:
        results.append((e["title"], sales_map[e["id"]]))
    
    # Sort: Highest sales first
    results.sort(key=lambda x: x[1], reverse=True)

    # 3. Extract the two extremes
    highest_name, highest_qty = results[0]
    lowest_name, lowest_qty = results[-1]

    # 4. Create Styled Content
    high_text = Text.assemble(
        (f"{highest_name}\n", "bold green"),
        (f"Sold: {highest_qty} tickets", "white")
    )
    
    low_text = Text.assemble(
        (f"{lowest_name}\n", "bold red"),
        (f"Sold: {lowest_qty} tickets", "white")
    )

    # 5. Display side-by-side in "Stat Boxes"
    console.print("\n")
    console.print(Columns([
        Panel(high_text, title="[bold green]🏆 BEST PERFORMANCE[/]", border_style="green", expand=True),
        Panel(low_text, title="[bold red]📉 LOWEST PERFORMANCE[/]", border_style="red", expand=True)
    ]))
    
    # 6. Safety Pause
    console.input("\n[dim]Press Enter to return to Dashboard...[/]")

def menu_analyze():
    pass

import matplotlib.pyplot as plt
from datetime import datetime

def view_sales_trend_graph():
    bookings = load_all_bookings()
    
    if not bookings:
        console.print("[bold red]No booking data available for graphing.[/]")
        return

    # 1. Aggregate Sales by Date
    # Expected format: {"2026-03-10": 5, "2026-03-11": 12, ...}
    daily_sales = {}
    for b in bookings:
        # If you don't have date_booked, this will default to 'Today' for demo
        date = b.get("date_booked", datetime.now().strftime("%Y-%m-%d"))
        qty = int(b.get("quantity", 0))
        daily_sales[date] = daily_sales.get(date, 0) + qty

    # 2. Sort dates chronologically for the X-axis
    sorted_dates = sorted(daily_sales.keys())
    sales_values = [daily_sales[d] for d in sorted_dates]

    # 3. Create the Plot
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sales_values, marker='o', linestyle='-', color='b', linewidth=2)
    
    # Styling the Graph
    plt.title('Daily Sales Velocity (Trend Analysis)', fontsize=14, fontweight='bold')
    plt.xlabel('Date of Booking', fontsize=12)
    plt.ylabel('Tickets Sold', fontsize=12)
    plt.xticks(rotation=45) # Tilt dates so they don't overlap
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 4. Show it!
    console.print("[bold green]📊 Generating Graph... Look for the popup window![/]")
    plt.show()

if __name__ == "__main__":
    # calculate_total_revenue()
    # view_top_events()
    # view_sales_extremes()
    view_sales_trend_graph()