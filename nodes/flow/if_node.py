import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.flow_node import (
    FlowNode,
)


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

    def render(
        self,
        indent=0,
        context=None,
    ):
        ind = "    " * indent

        condition_code = (
            self.condition.render(
                context=context,
            )
        )

        if self.true_node:
            true_code = (
                self.true_node.render(
                    indent + 1,
                    context,
                )
            )
        else:
            true_code = (
                "    "
                * (indent + 1)
                + "pass\n"
            )

        code = (
            f"{ind}if "
            f"{condition_code}:\n"
            f"{true_code}"
        )

        if self.false_node:
            false_code = (
                self.false_node.render(
                    indent + 1,
                    context,
                )
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

    def build_ast(
        self,
        context=None,
    ):
        if self.true_node:
            body = self.true_node.build_ast(
                context
            )

            if not isinstance(
                body,
                list,
            ):
                body = [body]
        else:
            body = [ast.Pass()]

        if self.false_node:
            orelse = (
                self.false_node.build_ast(
                    context
                )
            )

            if not isinstance(
                orelse,
                list,
            ):
                orelse = [orelse]
        else:
            orelse = []

        nodes = [
            ast.If(
                test=self.condition.build_ast(
                    context
                ),
                body=body,
                orelse=orelse,
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