from booking_file import load_all_bookings
from events import load_all_events

def calculate_total_revenue():
    bookings = load_all_bookings()
    events = load_all_events()
    
    # Create a dictionary for quick price lookup: {event_id: price}
    price_map = {e["id"]: float(e["price"]) for e in events}
    
    total = 0
    for b in bookings:
        event_id = b["event_id"]
        if event_id in price_map:
            total += b["quantity"] * price_map[event_id]
            
    print(f"💰 Total System Revenue: ${total:.2f}")

def view_top_events():
    bookings = load_all_bookings()
    events = load_all_events()
    
    # Count tickets per event
    sales_count = {}
    for b in bookings:
        e_id = b["event_id"]
        sales_count[e_id] = sales_count.get(e_id, 0) + b["quantity"]
        
    print("\n--- Sales Performance ---")
    for e in events:
        sold = sales_count.get(e["id"], 0)
        capacity = int(e["seats_input"]) + sold # Total original seats
        fill_rate = (sold / capacity * 100) if capacity > 0 else 0
        print(f"Event: {e['title']} | Sold: {sold} | Fill Rate: {fill_rate:.1f}%")