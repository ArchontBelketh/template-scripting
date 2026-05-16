from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class ReturnNode(StatementNode):
    NODE_TYPE = "return"
    DISPLAY_NAME = "Return"

    def __init__(
        self,
        value=None,
    ):
        super().__init__(None)

        self.value = value

    def render(self, indent=0, context=None):
        ind = "    " * indent

        if self.value:
            value_code = self.value.render(
                context=context,
            )

            return f"{ind}return {value_code}\n"

        return f"{ind}return\n"