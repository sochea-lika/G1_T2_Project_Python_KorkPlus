class Event:
    """
    Represents an event object.
    """
    def __init__(self, event_id, title, price, total_seats):
        self.event_id = event_id
        self.title = title
        self.price = price
        self.total_seats = total_seats
        self.available_seats = total_seats

    def __str__(self):
        return f"Event({self.event_id}): {self.title}, Price: {self.price}, Seats: {self.available_seats}/{self.total_seats}"

