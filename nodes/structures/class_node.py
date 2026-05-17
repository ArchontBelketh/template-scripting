from registry.node_registry import register_node

from core.context import RenderContext
from core.base_node import BaseNode


@register_node
class ClassNode(BaseNode):
    NODE_TYPE = "class"
    DISPLAY_NAME = "Class"

    def __init__(
        self,
        name,
        body_nodes=None,
        bases=None,
        decorators=None,
    ):
        self.name = name

        self.body_nodes = body_nodes or []

        self.bases = bases or []
        self.decorators = decorators or []

    def render(self, indent=0, context=None):
        context = context or RenderContext()

        ind = "    " * indent

        child_context = context.child(
            inside_class=True,
        )

        code = ""

        for decorator in self.decorators:
            code += (
                f"{ind}@{decorator.render(context=context)}\n"
            )

        bases_code = ""

        if self.bases:
            bases_code = (
                "("
                + ", ".join(self.bases)
                + ")"
            )

        code += (
            f"{ind}class {self.name}"
            f"{bases_code}:\n"
        )

        if not self.body_nodes:
            code += (
                "    " * (indent + 1)
                + "pass\n"
            )

            return code

        blocks = []

        for node in self.body_nodes:
            blocks.append(
                node.render(
                    indent + 1,
                    child_context,
                )
            )

        code += "\n".join(blocks)

        return code