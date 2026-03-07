class Person:
    """
    Base class representing a person.
    Demonstrates inheritance and encapsulation.
    """
    def __init__(self, name, password):
        self.name = name
        self._password = password  

    def set_password(self, new_password):
        self._password = new_password

    def check_password(self, password):
        return self._password == password
