from registry.node_registry import register_node

from core.base_node import BaseNode


@register_node
class ImportNode(BaseNode):
    NODE_TYPE = "import"
    DISPLAY_NAME = "Import"

    def __init__(
        self,
        module,
        alias=None,
    ):
        self.module = module
        self.alias = alias

    def render(self, indent=0, context=None):
        if self.alias:
            code = (
                f"import {self.module} "
                f"as {self.alias}"
            )
        else:
            code = f"import {self.module}"

        if context:
            context.imports.add(code)

        return ""