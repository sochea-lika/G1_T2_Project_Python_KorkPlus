import os

class SystemManager:
    """
    Handles File Handling and Business Logic.
    """
    def __init__(self, users_file="users.txt", events_file="events.txt"):
        self.users_file = users_file
        self.events_file = events_file

    def __str__(self):
        """Dunder method to show system status."""
        return f"SystemManager: Tracking {self.users_file} and {self.events_file}"

    def save_all_users(self, users_dict):
        """
        Overwrites the users file with a header and the entire updated dictionary.
        """
        try:
            with open(self.users_file, "w") as f:
                # 1. Write the Header File
                f.write("ID,Name,Email,Password\n") 
                
                # 2. Write the Data
                for name, data in users_dict.items():
                    user_id = data["id"]
                    email = data["email"]
                    password = data["password"]
                    
                    f.write(f"{user_id},{name},{email},{password}\n")
            return True
        except Exception as e:
            print("Error saving users database:", e)
            return False

    def load_users(self):
        """
        Load users from file into a dictionary, skipping the header line.
        """
        users = {}
        if not os.path.exists(self.users_file):
            return users

        try:
            with open(self.users_file, "r") as f:
                lines = f.readlines()
                
                # Check if file has data beyond just the header
                if len(lines) <= 1: 
                    return users

                # 3. Skip the first line (header) using slicing [1:]
                for line in lines[1:]:
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