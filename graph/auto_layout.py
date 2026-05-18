class GraphAutoLayout:
    def __init__(self, graph):
        self.graph = graph

    def apply(self):
        x = 0
        y = 0

        spacing_x = 450

        for node in self.graph.nodes:
            node.position = (
                x,
                y,
            )

            x += spacing_x