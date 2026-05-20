import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class CallNode(ExpressionNode):
    NODE_TYPE = "call"
    DISPLAY_NAME = "Call"

    def __init__(
        self,
        func,
        args=None,
        kwargs=None,
    ):
        self.func = func

        self.args = args or []
        self.kwargs = kwargs or {}

    def render(
        self,
        indent=0,
        context=None,
    ):
        func_code = self.func.render(
            context=context,
        )

        positional = [
            arg.render(context=context)
            for arg in self.args
        ]

        keyword = [
            (
                f"{key}="
                f"{value.render(context=context)}"
            )
            for key, value in self.kwargs.items()
        ]

        args_code = ", ".join(
            positional + keyword
        )

        return f"{func_code}({args_code})"

    def build_ast(
        self,
        context=None,
    ):
        return ast.Call(
            func=self.func.build_ast(
                context
            ),
            args=[
                arg.build_ast(context)
                for arg in self.args
            ],
            keywords=[
                ast.keyword(
                    arg=key,
                    value=value.build_ast(
                        context
                    ),
                )
                for key, value
                in self.kwargs.items()
            ],
        )