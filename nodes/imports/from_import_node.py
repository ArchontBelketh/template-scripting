from registry.node_registry import register_node

from core.base_node import BaseNode


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

    def render(self, indent=0, context=None):
        names_code = ", ".join(self.names)

        code = (
            f"from {self.module} "
            f"import {names_code}"
        )

        if context:
            context.imports.add(code)

        return ""