from core.types import normalize_type


class Pin:
    def __init__(
        self,
        name,
        pin_type,
        is_input,
        owner=None,
    ):
        self.name = name

        self.pin_type = normalize_type(
            pin_type
        )

        self.is_input = is_input

        self.owner = owner

        self.connections = []

        self.inferred_type = None

    def connect(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)

    def disconnect(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

    @property
    def effective_type(self):
        return (
            self.inferred_type
            or self.pin_type
        )

    @property
    def type_name(self):
        return str(
            self.effective_type
        )