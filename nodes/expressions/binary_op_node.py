import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


OPERATORS = {
    "+": ast.Add(),
    "-": ast.Sub(),
    "*": ast.Mult(),
    "/": ast.Div(),
    ">": ast.Gt(),
    "<": ast.Lt(),
    "==": ast.Eq(),
}


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

    def render(
        self,
        indent=0,
        context=None,
    ):
        left_code = self.left.render(
            context=context,
        )

        right_code = self.right.render(
            context=context,
        )

        return (
            f"({left_code} "
            f"{self.operator} "
            f"{right_code})"
        )

    def build_ast(
        self,
        context=None,
    ):
        left = self.left.build_ast(
            context
        )

        right = self.right.build_ast(
            context
        )

        operator = OPERATORS.get(
            self.operator
        )

        if isinstance(
            operator,
            (
                ast.Gt,
                ast.Lt,
                ast.Eq,
            ),
        ):
            return ast.Compare(
                left=left,
                ops=[operator],
                comparators=[right],
            )

        return ast.BinOp(
            left=left,
            op=operator,
            right=right,
        )