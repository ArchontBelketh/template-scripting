from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class ExpressionStatementNode(StatementNode):
    NODE_TYPE = "expression_statement"
    DISPLAY_NAME = "Expression Statement"

    def __init__(
        self,
        expression,
        next_node=None,
    ):
        super().__init__(next_node)

        self.expression = expression

    def render(self, indent=0, context=None):
        ind = "    " * indent

        expression_code = self.expression.render(
            context=context,
        )

        code = f"{ind}{expression_code}\n"

        return code + self.render_next(
            indent,
            context,
        )