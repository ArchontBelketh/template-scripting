class Pin:
    def __init__(
        self,
        name,
        pin_type,
        is_input,
        owner=None,
    ):
        self.name = name
        self.pin_type = pin_type
        self.is_input = is_input

        self.owner = owner

        self.connections = []

    def connect(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)

    def disconnect(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)