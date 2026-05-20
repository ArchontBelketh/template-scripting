import ast

from registry.node_registry import (
    register_node,
)

from nodes.base.flow_node import (
    FlowNode,
)


@register_node
class WhileNode(FlowNode):
    NODE_TYPE = "while"
    DISPLAY_NAME = "While"

    def __init__(
        self,
        condition,
        body_node=None,
        else_node=None,
        next_node=None,
    ):
        super().__init__(next_node)

        self.condition = condition

        self.body_node = body_node
        self.else_node = else_node

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

        loop_context = context.child(
            inside_loop=True,
        )

        if self.body_node:
            body_code = (
                self.body_node.render(
                    indent + 1,
                    loop_context,
                )
            )
        else:
            body_code = (
                "    "
                * (indent + 1)
                + "pass\n"
            )

        code = (
            f"{ind}while "
            f"{condition_code}:\n"
            f"{body_code}"
        )

        if self.else_node:
            else_code = (
                self.else_node.render(
                    indent + 1,
                    context,
                )
            )

            code += (
                f"{ind}else:\n"
                f"{else_code}"
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
        if self.body_node:
            body = self.body_node.build_ast(
                context
            )

            if not isinstance(
                body,
                list,
            ):
                body = [body]
        else:
            body = [ast.Pass()]

        if self.else_node:
            orelse = (
                self.else_node.build_ast(
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
            ast.While(
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