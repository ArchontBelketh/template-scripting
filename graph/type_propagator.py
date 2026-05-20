class GraphTypePropagator:
    def __init__(self, graph):
        self.graph = graph

    def propagate(self):
        """Проводит распространение типов по графу до стабилизации изменений."""
        iterations = 0
        max_iterations = 20
        changed = True

        while changed and iterations < max_iterations:
            changed = False
            iterations += 1

            for node in self.graph.nodes.values():
                # Каждая нода сама вычисляет свои выходные типы на основе входных данных
                if hasattr(node, "infer_output_types"):
                    old_types = {p.name: p.inferred_type for p in node.outputs.values()}
                    node.infer_output_types()
                    new_types = {p.name: p.inferred_type for p in node.outputs.values()}

                    if old_types != new_types:
                        changed = True