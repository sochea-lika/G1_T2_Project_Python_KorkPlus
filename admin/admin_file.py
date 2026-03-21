# handles the admin class and all functions
# Read write data to admin.txt
import os
from main.person import Person
Admin_file = "admin/admin.txt" # store admin account

# admin class inherirs from Person class so admin need have username password and email
class Admin(Person):
    def __init__(self, name, email, password): # Fixed: should be __init__
        super().__init__(name, email, password)
    
    def to_file_line(self): 
        return f"{self.name}|{self.email}|{self._password}\n"

    @staticmethod
    def from_file_line(line):
        # Skip the line if it is the header
        if line.startswith("Name|Email|Password"):
            return None
            
        parts = line.strip().split("|")
        if len(parts) == 3:
            return Admin(parts[0], parts[1], parts[2])
        return None

# --- File Operations ---

def load_all_admins():
    admins = []
    if os.path.exists(Admin_file):
        with open(Admin_file, "r") as file:
            lines = file.readlines()
            
            # 1. Skip the first line (header)
            if len(lines) <= 1:
                return admins

            for line in lines[1:]:
                admin = Admin.from_file_line(line)
                if admin:
                    admins.append(admin)
    return admins

def save_new_admin(admin):
    # Check if we need to write a header for a brand new file
    file_exists = os.path.exists(Admin_file)
    
    with open(Admin_file, "a") as file:
        if not file_exists:
            file.write("Name|Email|Password\n")
        file.write(admin.to_file_line())

def overwrite_admin_file(admins):
    with open(Admin_file, "w") as file:
        # 2. Always write the Header first when overwriting
        file.write("Name|Email|Password\n")
        
        for admin in admins:
            file.write(admin.to_file_line())

def find_admin_by_email(email):
    for admin in load_all_admins():
        if admin.get_email() == email:
            return admin
    return None