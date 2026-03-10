import os

class SystemManager:
    """
    Handles File Handling and Business Logic.
    """
    def __init__(self, users_file="users.txt", events_file="events.txt"):
        self.users_file = users_file
        self.events_file = events_file

    def save_user(self, user):
        """Save user with ID, name, email, and password."""
        try:
            with open(self.users_file, "a") as f:
                f.write(f"{user.user_id},{user.name},{user.email},{user._password}\n")
        except Exception as e:
            print("Error saving user:", e)

    def load_users(self):
        """
        Load users from file into a dictionary:
        {username: {"id": user_id, "email": email, "password": password}}
        """
        users = {}
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r") as f:
                    lines = f.readlines()
                    if not lines: return users

                    #skip first line / header
                    for line in lines:
                        parts = line.strip().split(",")
                        if len(parts) == 4:
                            user_id, name, email, password = parts
                            users[name] = {
                                "id": user_id,
                                "email": email,
                                "password": password
                            }
            except Exception as e:
                print("Error loading users:", e)
        return users
