import ast

from registry.node_registry import (
    register_node,
)

from core.context import RenderContext
from core.base_node import BaseNode


@register_node
class ModuleNode(BaseNode):
    NODE_TYPE = "module"
    DISPLAY_NAME = "Module"

    def __init__(
        self,
        body_nodes=None,
    ):
        self.body_nodes = (
            body_nodes or []
        )

    def render(
        self,
        indent=0,
        context=None,
    ):
        context = (
            context
            or RenderContext()
        )

        code_blocks = []

        for node in self.body_nodes:
            rendered = node.render(
                indent=0,
                context=context,
            )

            if rendered.strip():
                code_blocks.append(
                    rendered
                )

        imports_code = ""

        if context.imports:
            imports_code = (
                "\n".join(
                    sorted(
                        context.imports
                    )
                )
                + "\n\n"
            )

        return (
            imports_code
            + "\n\n".join(
                code_blocks
            )
        )

    def build_ast(
        self,
        context=None,
    ):
        body = []

        for node in self.body_nodes:
            built = node.build_ast(
                context
            )

            if isinstance(
                built,
                list,
            ):
                body.extend(built)
            else:
                body.append(built)

        return ast.Module(
            body=body,
            type_ignores=[],
        )