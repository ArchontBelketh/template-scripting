from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class PassNode(StatementNode):
    NODE_TYPE = "pass"
    DISPLAY_NAME = "Pass"

    def render(self, indent=0, context=None):
        ind = "    " * indent

        code = f"{ind}pass\n"

        return code + self.render_next(
            indent,
            context,
        )