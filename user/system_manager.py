import os

class SystemManager:
    """
    Handles File Handling and Business Logic.
    """
    def __init__(self, users_file="user/users.txt", events_file="event/events.txt"):
        self.users_file = users_file
        self.events_file = events_file

    def __str__(self):
        """Dunder method to show system status."""
        return f"SystemManager: Tracking {self.users_file} and {self.events_file}"

    def save_all_users(self, users_dict):
        try:
            with open(self.users_file, "w") as f:
                # 1. Write the Header
                f.write("ID,Name,Email,Password\n") 
                
                # 2. Write the Data
                for key, data in users_dict.items():
                    # Check if 'data' is a User object or a dictionary
                    if hasattr(data, 'user_id'): # It's an Object
                        u_id = data.user_id
                        u_name = data.name
                        u_email = data.email
                        u_pass = data._password
                    else: # It's still a Dictionary
                        u_id = data.get("id")
                        u_name = key # Or data.get("name")
                        u_email = data.get("email")
                        u_pass = data.get("password")
                    
                    f.write(f"{u_id},{u_name},{u_email},{u_pass}\n")
            return True
        except Exception as e:
            print(f"CRITICAL ERROR saving database: {e}")
            return False

    def load_users(self):
        users = {}
        if not os.path.exists(self.users_file):
            return users

        try:
            with open(self.users_file, "r") as f:
                lines = f.readlines()
                if len(lines) <= 1: return users

                for line in lines[1:]:
                    parts = line.strip().split(",") # Double check if you use , or |
                    if len(parts) == 4:
                        u_id, u_name, u_email, u_pass = parts
                        
                        # FIX: Use u_name as the KEY instead of u_email
                        users[u_name] = {
                            "id": u_id,
                            "email": u_email,
                            "password": u_pass
                        }
        except Exception as e:
            print(f"Error loading users: {e}")
            
        return users
    
    def append_user(self, user_data):
        """
        Safely adds a single user to the end of users.txt without overwriting.
        """
        # Check if file exists to decide if we need a header
        file_exists = os.path.isfile(self.users_file)

        try:
            # "a" = Append mode (pointer stays at the end of the file)
            with open(self.users_file, "a") as f:
                # If the file is brand new, write the header first
                if not file_exists or os.path.getsize(self.users_file) == 0:
                    f.write("ID,Name,Email,Password\n")

                # Extract data based on whether user_data is an Object or Dict
                if hasattr(user_data, 'user_id'): # Object case
                    u_id, u_name, u_email, u_pass = user_data.user_id, user_data.name, user_data.email, user_data._password
                else: # Dictionary case
                    u_id = user_data.get("id")
                    u_name = user_data.get("name")
                    u_email = user_data.get("email")
                    u_pass = user_data.get("password")

                # Write the new line
                f.write(f"{u_id},{u_name},{u_email},{u_pass}\n")
            return True
        except Exception as e:
            print(f"Append Error: {e}")
            return False