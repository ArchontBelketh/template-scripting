class GraphNode:
    def __init__(
        self,
        node_id,
        node_type,
        title,
        position=(0, 0),
        properties=None,
    ):
        self.node_id = node_id

        self.node_type = node_type
        self.title = title

        self.position = position

        self.properties = properties or {}

        self.input_pins = []
        self.output_pins = []

    def add_input_pin(self, pin):
        pin.owner = self
        self.input_pins.append(pin)

    def add_output_pin(self, pin):
        pin.owner = self
        self.output_pins.append(pin)

    def get_input_pin(self, name):
        for pin in self.input_pins:
            if pin.name == name:
                return pin

        return None

    def get_output_pin(self, name):
        for pin in self.output_pins:
            if pin.name == name:
                return pin

        return None