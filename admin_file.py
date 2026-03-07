# handles the admin class and all functions
# Read write data to admin.txt
import os
from person import Person
Admin_file = "admin.txt" # store admin account

# admin class inherirs from Person class so admin need have username password and email
class Admin(Person):
    def __init__(self,name,email,password):
        super().__init__(name,email,password)
    
    def to_file_line(self): # this method to convert info admin in one line
        return f"{self.name}|{self.email}|{self._password}\n"

    @staticmethod
    def from_file_line(line):
        # Read one line from admin.txt and turn it back into an admin abject
        parts = line.strip().split("|")
        if len(parts) == 3:
            name = parts[0]
            email = parts[1]
            password = parts[2]
            return Admin(name,email,password) #create object
        return None
# read and write admin data to admin.txt

#return list all admins
def load_all_admins():
    admins = []
    if os.path.exists(Admin_file):
        with open(Admin_file,"r") as file:
            for line in file:
                admin = Admin.from_file_line(line)
                if admin:
                    admins.append(admin)
    return admins
# add new admin into file admin.txt
def save_new_admin(admin):
    with open(Admin_file,"a") as file:
        file.write(admin.to_file_line())

# rewrite the whole admin.txt (use after password reset)
def overwrite_admin_file(admins):
    with open(Admin_file,"w") as file:
        for admin in admins:
            file.write(admin.to_file_line())

def find_admin_by_email(email):
    for admin in load_all_admins():
        if admin.get_email() == email:
            return admin
    return None