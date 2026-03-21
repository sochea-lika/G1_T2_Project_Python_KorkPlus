from events.booking_file import load_all_bookings
from events.events import load_all_events
import matplotlib.pyplot as plt
from datetime import datetime
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
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel("[bold magenta]📊 BUSINESS INTELLIGENCE & ANALYTICS[/]", style="magenta"))
        
        # Show the Health Check at the top so they see total revenue immediately
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
            view_sales_extremes() # The High/Low one we built
        elif choice == "3":
            calculate_total_revenue() # The detailed financial one
        elif choice == "0":
            break # Returns to the main admin_dashboard loop

def view_sales_trend_graph():
    # 1. Load Data
    bookings = load_all_bookings()
    if not bookings:
        console.print("[bold red]No booking data available for analysis.[/]")
        return

    # 2. Ask Admin for the Scale (Daily, Weekly, Monthly)
    scale = Prompt.ask(
        "\n[bold white]View sales trend by[/]", 
        choices=["daily", "weekly", "monthly"], 
        default="daily"
    )

    # 3. Aggregate Data into Time Buckets
    trend_data = {}
    for b in bookings:
        # Get the date string (or use today if missing)
        date_str = b.get("date_booked", datetime.now().strftime("%Y-%m-%d"))
        
        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Grouping Logic
            if scale == "monthly":
                key = dt_obj.strftime("%Y-%m")    # e.g., 2026-03
            elif scale == "weekly":
                key = dt_obj.strftime("%Y-W%U")   # e.g., 2026-W12
            else:
                key = date_str                    # Default: 2026-03-20

            qty = int(b.get("quantity", 0))
            trend_data[key] = trend_data.get(key, 0) + qty
            
        except ValueError:
            continue # Skips invalid date formats to prevent crash

    # 4. Sort keys chronologically for the X-axis
    sorted_keys = sorted(trend_data.keys())
    values = [trend_data[k] for k in sorted_keys]

    # 5. Plotting (CLEANED UP)
    plt.close('all')  # Close any ghost windows first
    plt.figure(figsize=(10, 6))
    
    # Using a professional theme-matching color (Slate Blue)
    plt.plot(sorted_keys, values, marker='o', linestyle='-', color='#6272a4', linewidth=2.5)
    
    # Styling the Canvas
    plt.title(f'Sales Performance Trend: {scale.capitalize()}', fontsize=14, fontweight='bold')
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('Tickets Sold', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # 6. Display to Admin
    console.print(f"\n[bold green]📊 Generating {scale} graph...[/]")
    console.print("[dim italic]Close the graph window to return to the menu.[/]")
    
    plt.show()  # Execution pauses here until window is closed
    plt.close() # Clean memory after closing

    console.input("\n[bold cyan]Press Enter to return to Analysis Hub...[/]")

from datetime import datetime, timedelta

def view_daily_growth():
    bookings = load_all_bookings()
    
    # 1. Get Date Strings
    today_dt = datetime.now()
    yesterday_dt = today_dt - timedelta(days=1)
    
    today_str = today_dt.strftime("%Y-%m-%d")
    yesterday_str = yesterday_dt.strftime("%Y-%m-%d")
    
    # 2. Calculate Totals
    today_sales = 0
    yesterday_sales = 0
    
    for b in bookings:
        date = b.get("date_booked", "")
        qty = int(b.get("quantity", 0))
        
        if date == today_str:
            today_sales += qty
        elif date == yesterday_str:
            yesterday_sales += qty

    # 3. Calculate Growth Percentage
    if yesterday_sales > 0:
        growth = ((today_sales - yesterday_sales) / yesterday_sales) * 100
    else:
        # If yesterday was 0, and today is > 0, it's 100% growth
        growth = 100 if today_sales > 0 else 0

    # 4. Create the Visual Table
    table = Table(title="📈 Day-over-Day (DoD) Analysis", box=None)
    table.add_column("Period", style="cyan")
    table.add_column("Tickets Sold", justify="right")

    table.add_row("Yesterday", str(yesterday_sales))
    table.add_row("Today", f"[bold white]{today_sales}[/]")
    
    # Status Logic
    if today_sales > yesterday_sales:
        status = f"[bold green]▲ +{growth:.1f}% Growth[/]"
    elif today_sales < yesterday_sales:
        status = f"[bold red]▼ {growth:.1f}% Decline[/]"
    else:
        status = "[bold yellow]● No Change[/]"
        
    table.add_row("Status", status)
    
    console.print(Panel(table, title="[bold magenta]MOMENTUM CHECK[/]", border_style="magenta", expand=False))

def view_daily_comparison_graph():
    bookings = load_all_bookings()
    
    # 1. Get the exact date strings for Today and Yesterday
    # Based on your current system time: 2026-03-20
    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 2. Initialize counters
    today_count = 0
    yesterday_count = 0
    
    # 3. Loop through and only sum up the quantities for these two days
    for b in bookings:
        b_date = b.get("date_booked", "")
        b_qty = int(b.get("quantity", 0))
        
        if b_date == today_str:
            today_count += b_qty
        elif b_date == yesterday_str:
            yesterday_count += b_qty

    # 4. Create the Bar Chart
    plt.close('all')
    plt.figure(figsize=(7, 6))
    
    labels = [f"Yesterday\n({yesterday_str})", f"Today\n({today_str})"]
    counts = [yesterday_count, today_count]
    colors = ['#ffb86c', '#50fa7b'] # Orange for yesterday, Green for today

    bars = plt.bar(labels, counts, color=colors, edgecolor='black', width=0.6)

    # Add the actual number on top of each bar so the Admin doesn't have to guess
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                 f'{int(height)}', ha='center', va='bottom', 
                 fontsize=12, fontweight='bold')

    # Styling the Graph
    plt.title('Daily Sales Volume: Yesterday vs Today', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Tickets Sold', fontsize=12)
    plt.ylim(0, max(counts) * 1.2 if max(counts) > 0 else 10) # Auto-scale height
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    plt.close()
    
    console.input("\n[dim]Press Enter to return...[/]")

if __name__ == "__main__":
    # calculate_total_revenue()
    # view_top_events()
    # view_sales_extremes()
    # view_sales_trend_graph()
    # view_daily_growth()
    view_daily_comparison_graph()