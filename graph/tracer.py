class ExecutionTracer:
    def __init__(self):
        self.execution_log = []

    def clear(self):
        self.execution_log.clear()

    def trace_node(self, node):
        self.execution_log.append(
            {
                "node_id": node.node_id,
                "node_type": node.node_type,
                "title": node.title,
            }
        )

    def get_log(self):
        return self.execution_log.copy()