import os

class SystemManager:
    """
    Handles File Handling and Business Logic.
    """
    def __init__(self, users_file="users.txt", events_file="events.txt"):
        self.users_file = users_file
        self.events_file = events_file
    def save_user(self, user):
        try:
            with open(self.users_file, "a") as f:
                f.write(f"{user.user_id},{user.name},{user._password}\n")
        except Exception as e:
            print("Error saving user:", e)
    def load_users(self):
        users = {}
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) == 3:
                            user_id, name, password = parts
                            users[name] = password
            except Exception as e:
                print("Error loading users:", e)
        return users
