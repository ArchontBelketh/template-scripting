class ASTSourceMapper:
    def __init__(self):
        self.ast_to_graph = {}

    def register(
        self,
        ast_node,
        graph_node_id,
    ):
        self.ast_to_graph[
            id(ast_node)
        ] = graph_node_id

    def resolve_graph_node(
        self,
        ast_node,
    ):
        return self.ast_to_graph.get(
            id(ast_node)
        )