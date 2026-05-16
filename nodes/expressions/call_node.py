from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class CallNode(ExpressionNode):
    NODE_TYPE = "call"
    DISPLAY_NAME = "Call"

    def __init__(
        self,
        func,
        args=None,
    ):
        self.func = func
        self.args = args or []

    def render(self, indent=0, context=None):
        func_code = self.func.render(
            context=context,
        )

        args_code = ", ".join(
            arg.render(context=context)
            for arg in self.args
        )

        return f"{func_code}({args_code})"