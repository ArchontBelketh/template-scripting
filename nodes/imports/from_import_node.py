import ast

from registry.node_registry import (
    register_node,
)

from core.base_node import (
    BaseNode,
)


@register_node
class FromImportNode(BaseNode):
    NODE_TYPE = "from_import"
    DISPLAY_NAME = "From Import"

    def __init__(
        self,
        module,
        names,
    ):
        self.module = module
        self.names = names

    def render(
        self,
        indent=0,
        context=None,
    ):
        names_code = ", ".join(
            self.names
        )

        code = (
            f"from {self.module} "
            f"import {names_code}"
        )

        if context:
            context.imports.add(code)

        return ""

    def build_ast(
        self,
        context=None,
    ):
        return ast.ImportFrom(
            module=self.module,
            names=[
                ast.alias(
                    name=name,
                    asname=None,
                )
                for name
                in self.names
            ],
            level=0,
        )