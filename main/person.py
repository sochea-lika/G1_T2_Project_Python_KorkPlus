class Person:
    """
    Base class representing a person.
    Demonstrates inheritance and encapsulation.
    """
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self._password = password  

    def get_email(self):
        return self.email

    def set_password(self, new_password):
        self._password = new_password

    def check_password(self, password):
        return self._password == password

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.email.lower() == other.email.lower()

    def __repr__(self):
        return f"Person('{self.name}', '{self.email}')"
