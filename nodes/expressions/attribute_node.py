import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class AttributeNode(ExpressionNode):
    NODE_TYPE = "attribute"
    DISPLAY_NAME = "Attribute"

    def __init__(
        self,
        value,
        attribute,
    ):
        self.value = value
        self.attribute = attribute

    def render(
        self,
        indent=0,
        context=None,
    ):
        value_code = self.value.render(
            context=context,
        )

        return (
            f"{value_code}."
            f"{self.attribute}"
        )

    def build_ast(
        self,
        context=None,
    ):
        return ast.Attribute(
            value=self.value.build_ast(
                context
            ),
            attr=self.attribute,
            ctx=ast.Load(),
        )