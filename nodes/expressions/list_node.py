import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class ListNode(ExpressionNode):
    NODE_TYPE = "list"
    DISPLAY_NAME = "List"

    def __init__(
        self,
        elements=None,
    ):
        self.elements = elements or []

    def render(
        self,
        indent=0,
        context=None,
    ):
        elements_code = ", ".join(
            element.render(
                context=context
            )
            for element
            in self.elements
        )

        return (
            f"[{elements_code}]"
        )

    def build_ast(
        self,
        context=None,
    ):
        return ast.List(
            elts=[
                element.build_ast(
                    context
                )
                for element
                in self.elements
            ],
            ctx=ast.Load(),
        )