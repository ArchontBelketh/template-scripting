import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class LiteralNode(ExpressionNode):
    NODE_TYPE = "literal"
    DISPLAY_NAME = "Literal"

    def __init__(self, value):
        self.value = value

    def render(
        self,
        indent=0,
        context=None,
    ):
        return repr(self.value)

    def build_ast(
        self,
        context=None,
    ):
        return ast.Constant(
            value=self.value
        )