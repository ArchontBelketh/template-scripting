import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class VariableNode(ExpressionNode):
    NODE_TYPE = "variable"
    DISPLAY_NAME = "Variable"

    def __init__(self, name):
        self.name = name

    def render(
        self,
        indent=0,
        context=None,
    ):
        return self.name

    def build_ast(
        self,
        context=None,
    ):
        return ast.Name(
            id=self.name,
            ctx=ast.Load(),
        )