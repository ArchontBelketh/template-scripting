from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class ImportStatementNode(StatementNode):
    NODE_TYPE = "import_statement"
    DISPLAY_NAME = "Import Statement"

    def __init__(
        self,
        import_node,
        next_node=None,
    ):
        super().__init__(next_node)

        self.import_node = import_node

    def render(self, indent=0, context=None):
        self.import_node.render(
            context=context,
        )

        return self.render_next(
            indent,
            context,
        )