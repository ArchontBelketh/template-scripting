import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.statement_node import (
    StatementNode,
)


@register_node
class ExpressionStatementNode(
    StatementNode
):
    NODE_TYPE = "expression_statement"

    DISPLAY_NAME = (
        "Expression Statement"
    )

    def __init__(
        self,
        expression,
        next_node=None,
    ):
        super().__init__(next_node)

        self.expression = expression

    def render(
        self,
        indent=0,
        context=None,
    ):
        ind = "    " * indent

        expression_code = (
            self.expression.render(
                context=context,
            )
        )

        code = (
            f"{ind}{expression_code}\n"
        )

        return (
            code
            + self.render_next(
                indent,
                context,
            )
        )

    def build_ast(
        self,
        context=None,
    ):
        nodes = [
            ast.Expr(
                value=self.expression.build_ast(
                    context
                )
            )
        ]

        if self.next_node:
            next_ast = (
                self.next_node.build_ast(
                    context
                )
            )

            if isinstance(
                next_ast,
                list,
            ):
                nodes.extend(next_ast)
            else:
                nodes.append(next_ast)

        return nodes