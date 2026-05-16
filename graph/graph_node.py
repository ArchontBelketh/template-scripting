class GraphNode:
    def __init__(self, runtime_node):
        self.runtime_node = runtime_node

        self.input_pins = []
        self.output_pins = []