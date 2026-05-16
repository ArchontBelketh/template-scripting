from registry.node_registry import register_node

from nodes.base.flow_node import FlowNode


@register_node
class IfNode(FlowNode):
    NODE_TYPE = "if"
    DISPLAY_NAME = "If"

    def __init__(
        self,
        condition,
        true_node=None,
        false_node=None,
        next_node=None,
    ):
        super().__init__(next_node)

        self.condition = condition
        self.true_node = true_node
        self.false_node = false_node

    def render(self, indent=0, context=None):
        ind = "    " * indent

        condition_code = self.condition.render(
            context=context,
        )

        if self.true_node:
            true_code = self.true_node.render(
                indent + 1,
                context,
            )
        else:
            true_code = (
                "    " * (indent + 1)
                + "pass\n"
            )

        code = (
            f"{ind}if {condition_code}:\n"
            f"{true_code}"
        )

        if self.false_node:
            false_code = self.false_node.render(
                indent + 1,
                context,
            )

            code += (
                f"{ind}else:\n"
                f"{false_code}"
            )

        code += self.render_next(
            indent,
            context,
        )

        return code