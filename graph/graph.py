from typing import Dict
from graph.graph_node import GraphNode
from graph.connection import Connection
from graph.type_propagator import GraphTypePropagator


class Graph:
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.connections: list[Connection] = []

    def add_node(self, node: GraphNode):
        self.nodes[node.id] = node

    def remove_node(self, node_id: str):
        if node_id in self.nodes:
            # Удаляем связи ноды перед удалением самой ноды
            node = self.nodes[node_id]
            for pin in list(node.inputs.values()) + list(node.outputs.values()):
                for conn in list(pin.connections):
                    self.remove_connection(conn)
            del self.nodes[node_id]

    def add_connection(self, source_node_id: str, source_pin_name: str, target_node_id: str, target_pin_name: str):
        source_node = self.nodes.get(source_node_id)
        target_node = self.nodes.get(target_node_id)

        if source_node and target_node:
            source_pin = source_node.outputs.get(source_pin_name)
            target_pin = target_node.inputs.get(target_pin_name)

            if source_pin and target_pin:
                connection = Connection(source_pin, target_pin)
                source_pin.connections.append(connection)
                target_pin.connections.append(connection)
                self.connections.append(connection)
                self.propagate_types()

    def remove_connection(self, connection: Connection):
        if connection in self.connections:
            connection.source_pin.connections.remove(connection)
            connection.target_pin.connections.remove(connection)
            self.connections.remove(connection)
            self.propagate_types()

    def propagate_types(self):
        """Запускает процесс обновления типов данных на пинах по всему графу."""
        propagator = GraphTypePropagator(self)
        propagator.propagate()