from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class ListComprehensionNode(ExpressionNode):
    NODE_TYPE = "list_comprehension"
    DISPLAY_NAME = "List Comprehension"

    def __init__(
        self,
        expression,
        variable_name,
        iterable,
        condition=None,
    ):
        self.expression = expression
        self.variable_name = variable_name
        self.iterable = iterable
        self.condition = condition

    def render(self, indent=0, context=None):
        expression_code = self.expression.render(
            context=context,
        )

        iterable_code = self.iterable.render(
            context=context,
        )

        code = (
            f"[{expression_code} "
            f"for {self.variable_name} "
            f"in {iterable_code}"
        )

        if self.condition:
            condition_code = self.condition.render(
                context=context,
            )

            code += f" if {condition_code}"

        code += "]"

        return code