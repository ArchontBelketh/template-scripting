from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class RandomValueNode(ExpressionNode):
    NODE_TYPE = "random_value"

    DISPLAY_NAME = "Random Value"

    def render(
        self,
        indent=0,
        context=None,
    ):
        return "random.random()"