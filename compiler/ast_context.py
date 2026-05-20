class ASTContext:
    def __init__(self):
        self.node_line_mapping = {}

    def register_mapping(
        self,
        graph_node_id,
        ast_node,
    ):
        self.node_line_mapping[
            id(ast_node)
        ] = graph_node_id