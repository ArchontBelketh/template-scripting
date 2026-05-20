import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class AwaitNode(ExpressionNode):
    NODE_TYPE = "await"
    DISPLAY_NAME = "Await"

    def __init__(
        self,
        expression,
    ):
        self.expression = expression

    def render(
        self,
        indent=0,
        context=None,
    ):
        expression_code = (
            self.expression.render(
                context=context,
            )
        )

        return (
            f"await "
            f"{expression_code}"
        )

    def build_ast(
        self,
        context=None,
    ):
        return ast.Await(
            value=self.expression.build_ast(
                context
            )
        )