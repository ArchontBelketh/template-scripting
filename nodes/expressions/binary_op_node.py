from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class BinaryOpNode(ExpressionNode):
    NODE_TYPE = "binary_op"
    DISPLAY_NAME = "Binary Operation"

    def __init__(
        self,
        left,
        operator,
        right,
    ):
        self.left = left
        self.operator = operator
        self.right = right

    def render(self, indent=0, context=None):
        left_code = self.left.render(
            context=context,
        )

        right_code = self.right.render(
            context=context,
        )

        return f"({left_code} {self.operator} {right_code})"