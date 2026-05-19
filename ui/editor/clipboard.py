import copy


class GraphClipboard:
    def __init__(self):
        self.data = None

    def copy(self, nodes):
        serialized = []

        for node in nodes:
            serialized.append(
                {
                    "node_type": node.node_type,
                    "x": node.pos().x(),
                    "y": node.pos().y(),
                    "properties": copy.deepcopy(
                        node.properties
                    ),
                }
            )

        self.data = serialized

    def paste(self, main_window, offset=40):
        if not self.data:
            return

        created = []

        for node_data in self.data:
            node = main_window.create_node(
                node_data["node_type"],
                node_data["x"] + offset,
                node_data["y"] + offset,
                node_data["properties"],
            )

            created.append(node)

        return created