class Graph:
    def __init__(self):
        self.nodes = []
        self.connections = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_connection(self, connection):
        self.connections.append(connection)

    def find_node_by_type(self, node_type):
        for node in self.nodes:
            if node.node_type == node_type:
                return node

        return None