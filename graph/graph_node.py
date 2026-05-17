class GraphNode:
    def __init__(
        self,
        node_type,
        title,
        position=(0, 0),
    ):
        self.node_type = node_type
        self.title = title
        self.position = position

        self.input_pins = []
        self.output_pins = []