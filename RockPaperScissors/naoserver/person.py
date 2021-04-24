class Person:
    """
    Represents a person, holds ip address, socket client and name
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """
        Sets the person's name
        """
        self.name = name

    def __repr__(self):
        return f"Person({self.addr}, {self.name})"
