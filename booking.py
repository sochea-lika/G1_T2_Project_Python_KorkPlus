import os

class Booking:
    BOOKINGS_FILE = "bookings.txt"
    CANCELED_FILE = "canceled.txt"

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    # -------------------------------
    # File Helpers
    # -------------------------------
    @staticmethod
    def load_bookings():
        bookings = []
        if os.path.exists(Booking.BOOKINGS_FILE):
            with open(Booking.BOOKINGS_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        user_id, event_id = parts
                        bookings.append(Booking(int(user_id), int(event_id)))
        return bookings

    @staticmethod
    def save_bookings(bookings):
        with open(Booking.BOOKINGS_FILE, "w") as f:
            for b in bookings:
                f.write(f"{b.user_id},{b.event_id}\n")

    @staticmethod
    def log_canceled(booking):
        with open(Booking.CANCELED_FILE, "a") as f:
            f.write(f"{booking.user_id},{booking.event_id}\n")

    # -------------------------------
    # Booking Actions
    # -------------------------------

    @staticmethod
    def book_event(user, events, bookings):
        bookings = Booking.load_bookings()
        event_id = int(input("Enter the Event ID you want to book: "))
        for event in events:
            if event.event_id == event_id:
                if event.available_seats > 0:
                    event.available_seats -= 1
                    booking = Booking(user.user_id, event_id)
                    bookings.append(booking)
                    Booking.save_bookings(bookings) 
                    print(f"Successfully booked '{event.title}'!")
                else:
                    print("Sorry, this event is sold out.")
                return
        print("Invalid Event ID.")
    @staticmethod
    def cancel_event(user, events):
        bookings = Booking.load_bookings()
        event_id = int(input("Enter the Event ID you want to cancel: "))

        for booking in bookings:
            if booking.user_id == user.user_id and booking.event_id == event_id:
                bookings.remove(booking)
                Booking.save_bookings(bookings)
                Booking.log_canceled(booking)

                for event in events:
                    if event.event_id == event_id:
                        event.available_seats += 1
                        print(f"Booking for '{event.title}' has been canceled.")
                        return
        print("You don’t have a booking for this event.")

    @staticmethod
    def view_bookings(user, events):
        bookings = Booking.load_bookings()
        user_bookings = [b for b in bookings if b.user_id == user.user_id]

        if not user_bookings:
            print("You have no bookings.")
            return

        print("\nYour Bookings:")
        for booking in user_bookings:
            for event in events:
                if event.event_id == booking.event_id:
                    print(f"- {event.title} on {event.date}")
