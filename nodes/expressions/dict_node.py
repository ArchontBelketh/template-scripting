import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class DictNode(ExpressionNode):
    NODE_TYPE = "dict"
    DISPLAY_NAME = "Dict"

    def __init__(
        self,
        items=None,
    ):
        self.items = items or []

    def render(
        self,
        indent=0,
        context=None,
    ):
        parts = []

        for key, value in self.items:
            key_code = key.render(
                context=context,
            )

            value_code = value.render(
                context=context,
            )

            parts.append(
                f"{key_code}: "
                f"{value_code}"
            )

        return "{%s}" % ", ".join(parts)

    def build_ast(
        self,
        context=None,
    ):
        return ast.Dict(
            keys=[
                key.build_ast(context)
                for key, _
                in self.items
            ],
            values=[
                value.build_ast(
                    context
                )
                for _, value
                in self.items
            ],
        )