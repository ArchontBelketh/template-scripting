from registry.node_registry import register_node

from core.context import RenderContext

from core.base_node import BaseNode


@register_node
class ModuleNode(BaseNode):
    NODE_TYPE = "module"
    DISPLAY_NAME = "Module"

    def __init__(self, body_nodes=None):
        self.body_nodes = body_nodes or []

    def render(self, indent=0, context=None):
        context = context or RenderContext()

        code_blocks = []

        for node in self.body_nodes:
            code_blocks.append(
                node.render(
                    indent=0,
                    context=context,
                )
            )

        imports_code = ""

        if context.imports:
            imports_code = (
                "\n".join(sorted(context.imports))
                + "\n\n"
            )

        return imports_code + "\n\n".join(code_blocks)