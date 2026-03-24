from events.booking_file import load_all_bookings
from events.events import load_all_events
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.progress import BarColumn, Progress, TextColumn
from rich.prompt import Prompt
import os

console = Console()

def calculate_total_revenue():
    bookings = load_all_bookings()
    events = load_all_events()
    
    price_map = {e["id"]: float(e["price"]) for e in events}
    
    total = 0
    total_tickets = 0
    
    for b in bookings:
        event_id = b["event_id"]
        qty = int(b["quantity"])
        if event_id in price_map:
            total += qty * price_map[event_id]
            total_tickets += qty
            
    revenue_text = Text.assemble(
        ("TOTAL REVENUE\n", "bold cyan"),
        (f"${total:,.2f}", "bold green underline"),
        (f"\n\nTickets Sold: ", "dim white"),
        (f"{total_tickets}", "bold yellow")
    )

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

    console.input("\n[dim]Press Enter to return to Admin Dashboard...[/]")

def view_top_events():
    bookings = load_all_bookings()
    events = load_all_events()
    
    # Count tickets per event
    sales_count = {}
    for b in bookings:
        e_id = b["event_id"]
        sales_count[e_id] = sales_count.get(e_id, 0) + int(b["quantity"])

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

    # Calculate and Populate
    for e in events:
        sold = sales_count.get(e["id"], 0)
        capacity = int(e.get("seat_total", 0)) 
        fill_rate = (sold / capacity * 100) if capacity > 0 else 0

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
    console.print("\n")
    console.print(table)
    console.input("\n[bold cyan]Press Enter to return to Admin Dashboard...[/]")

def view_sales_extremes():
    bookings = load_all_bookings()
    events = load_all_events() 
    
    if not events:
        console.print("[bold red]No events found.[/]")
        return

    sales_map = {str(e['id']).strip(): 0 for e in events}
    
    for b in bookings:
        # Use .get() to avoid crashes if a key is missing
        e_id = str(b.get("event_id", "")).strip()
        if e_id in sales_map:
            sales_map[e_id] += int(b.get("quantity", 0))

    results = []
    for e in events:
        qty = sales_map.get(str(e['id']).strip(), 0)
        results.append({
            "title": e['title'],
            "date": e['date'], 
            "qty": qty
        })
    
    # Highest sales first
    results.sort(key=lambda x: x['qty'], reverse=True)

    highest = results[0]
    lowest = results[-1]
    total_sales = sum(sales_map.values())

    console.print("\n")
    if total_sales == 0:
        console.print(Panel(Align.center("[yellow]No tickets sold yet.[/]")))
    else:
        high_text = Text.assemble(
            (f"{highest['title']}\n", "bold green"),
            (f"Date: {highest['date']}\n", "dim"),
            (f"Sold: {highest['qty']} tickets", "white")
        )
        
        low_text = Text.assemble(
            (f"{lowest['title']}\n", "bold red"),
            (f"Date: {lowest['date']}\n", "dim"),
            (f"Sold: {lowest['qty']} tickets", "white")
        )

        console.print(Columns([
            Panel(high_text, title="🏆 BEST", border_style="green", expand=True),
            Panel(low_text, title="📉 LOWEST", border_style="red", expand=True)
        ]))
    
    console.input("\n[dim]Press Enter to return...[/]")

def menu_analyze():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel("[bold magenta]📊 BUSINESS INTELLIGENCE & ANALYTICS[/]", style="magenta"))

        from admin.admin import admin_health_check
        admin_health_check() 
        
        console.print("\n[1] 📈 View Daily Sales Trend (Matplotlib Graph)")
        console.print("[2] 🏆 View Top & Lowest Performers (Spotlight)")
        console.print("[3] 💰 Detailed Revenue Breakdown")
        console.print("[0] ↩ Back to Main Dashboard")
        
        choice = Prompt.ask("\nSelect Analysis", choices=["1", "2", "3", "0"])
        
        if choice == "1":
            view_sales_trend_graph()
        elif choice == "2":
            view_top_events()
            view_sales_extremes()
        elif choice == "3":
            calculate_total_revenue() 
        elif choice == "0":
            break 

def view_sales_trend_graph():
    bookings = load_all_bookings()
    if not bookings:
        console.print("[bold red]No booking data available for analysis.[/]")
        return

    scale = Prompt.ask(
        "\n[bold white]View sales trend by[/]", 
        choices=["daily", "weekly", "monthly"], 
        default="daily"
    )

    trend_data = {}
    for b in bookings:
        date_str = b.get("date_booked", datetime.now().strftime("%Y-%m-%d"))
        
        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")

            if scale == "monthly":
                key = dt_obj.strftime("%Y-%m")    # e.g., 2026-03
            elif scale == "weekly":
                key = dt_obj.strftime("%Y-W%U")   # e.g., 2026-W12
            else:
                key = date_str                    # Default: 2026-03-20

            qty = int(b.get("quantity", 0))
            trend_data[key] = trend_data.get(key, 0) + qty
            
        except ValueError:
            continue 

    sorted_keys = sorted(trend_data.keys())
    values = [trend_data[k] for k in sorted_keys]

    plt.close('all')  
    plt.figure(figsize=(10, 6))

    plt.plot(sorted_keys, values, marker='o', linestyle='-', color='#6272a4', linewidth=2.5)
    
    plt.title(f'Sales Performance Trend: {scale.capitalize()}', fontsize=14, fontweight='bold')
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('Tickets Sold', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()


    console.print(f"\n[bold green]📊 Generating {scale} graph...[/]")
    console.print("[dim italic]Close the graph window to return to the menu.[/]")
    
    plt.show()  
    plt.close() 

    console.input("\n[bold cyan]Press Enter to return to Analysis Hub...[/]")

def view_daily_growth():
    bookings = load_all_bookings()
    
    # Get Date Strings
    today_dt = datetime.now()
    yesterday_dt = today_dt - timedelta(days=1)
    
    today_str = today_dt.strftime("%Y-%m-%d")
    yesterday_str = yesterday_dt.strftime("%Y-%m-%d")
    
    #  Calculate Totals
    today_sales = 0
    yesterday_sales = 0
    
    for b in bookings:
        date = b.get("date_booked", "")
        qty = int(b.get("quantity", 0))
        
        if date == today_str:
            today_sales += qty
        elif date == yesterday_str:
            yesterday_sales += qty

    # Calculate Growth Percentage
    if yesterday_sales > 0:
        growth = ((today_sales - yesterday_sales) / yesterday_sales) * 100
    else:
        # If yesterday was 0, and today is > 0, it's 100% growth
        growth = 100 if today_sales > 0 else 0

    table = Table(title="📈 Day-over-Day (DoD) Analysis", box=None)
    table.add_column("Period", style="cyan")
    table.add_column("Tickets Sold", justify="right")

    table.add_row("Yesterday", str(yesterday_sales))
    table.add_row("Today", f"[bold white]{today_sales}[/]")
    
    if today_sales > yesterday_sales:
        status = f"[bold green]▲ +{growth:.1f}% Growth[/]"
    elif today_sales < yesterday_sales:
        status = f"[bold red]▼ {growth:.1f}% Decline[/]"
    else:
        status = "[bold yellow]● No Change[/]"
        
    table.add_row("Status", status)
    
    console.print(Panel(table, title="[bold magenta]MOMENTUM CHECK[/]", border_style="magenta", expand=False))
