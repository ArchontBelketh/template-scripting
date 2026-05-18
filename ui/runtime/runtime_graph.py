from graph.graph import Graph
from graph.graph_node import GraphNode
from graph.connection import Connection
from graph.auto_layout import GraphAutoLayout

from graph.execution_pin import ExecutionPin
from graph.data_pin import DataPin

from ui.node_metadata import NODE_METADATA


class RuntimeGraph:
    def __init__(self):
        self.graph = Graph()

    def create_node_from_item(self, node_item):
        metadata = NODE_METADATA[node_item.node_type]

        graph_node = GraphNode(
            node_id=id(node_item),
            node_type=node_item.node_type,
            title=metadata["title"],
            position=(
                node_item.pos().x(),
                node_item.pos().y(),
            ),
            properties=node_item.properties.copy(),
        )

        for pin_data in metadata["inputs"]:
            pin = self.create_pin(pin_data, True)
            graph_node.add_input_pin(pin)

        for pin_data in metadata["outputs"]:
            pin = self.create_pin(pin_data, False)
            graph_node.add_output_pin(pin)

        node_item.runtime_node = graph_node

        self.graph.add_node(graph_node)

    def create_pin(self, pin_data, is_input):
        pin_type = pin_data["type"]

        if pin_type == "execution":
            return ExecutionPin(
                pin_data["name"],
                is_input,
            )

        return DataPin(
            pin_data["name"],
            pin_type,
            is_input,
        )

    def create_connection(
        self,
        output_pin_item,
        input_pin_item,
    ):
        output_runtime_pin = output_pin_item.runtime_pin
        input_runtime_pin = input_pin_item.runtime_pin

        connection = Connection(
            output_runtime_pin,
            input_runtime_pin,
        )

        self.graph.add_connection(connection)

    def get_input_value(
        self,
        node,
        pin_name,
    ):
        pin = node.get_input_pin(pin_name)

        if not pin:
            return None

        if not pin.connections:
            return None

        return pin.connections[0]

    def clear(self):
        self.graph.nodes.clear()
        self.graph.connections.clear()

    def auto_layout(self):
        layout = GraphAutoLayout(
            self.graph
        )

        layout.apply()