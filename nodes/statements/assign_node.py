from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class AssignNode(StatementNode):
    NODE_TYPE = "assign"
    DISPLAY_NAME = "Assign"

    def __init__(
        self,
        target,
        value,
        next_node=None,
    ):
        super().__init__(next_node)

        self.target = target
        self.value = value

    def render(self, indent=0, context=None):
        ind = "    " * indent

        target_code = self.target.render(
            context=context,
        )

        value_code = self.value.render(
            context=context,
        )

        code = (
            f"{ind}{target_code} = {value_code}\n"
        )

        return code + self.render_next(
            indent,
            context,
        )