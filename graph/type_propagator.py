class GraphTypePropagator:
    def __init__(self, graph):
        self.graph = graph

    def propagate(self):
        changed = True

        iterations = 0

        while changed and iterations < 20:
            iterations += 1

            changed = False

            for connection in self.graph.connections:
                source = connection.output_pin
                target = connection.input_pin

                source_type = (
                    source.effective_type
                )

                if (
                    target.inferred_type
                    != source_type
                ):
                    target.inferred_type = (
                        source_type
                    )

                    changed = True