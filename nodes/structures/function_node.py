from registry.node_registry import register_node

from core.context import RenderContext

from core.base_node import BaseNode


@register_node
class FunctionNode(BaseNode):
    NODE_TYPE = "function"
    DISPLAY_NAME = "Function"

    def __init__(
        self,
        name,
        params=None,
        body_node=None,
        decorators=None,
        is_async=False,
    ):
        self.name = name
        self.params = params or []
        self.body_node = body_node
        self.decorators = decorators or []
        self.is_async = is_async

    def render(self, indent=0, context=None):
        ind = "    " * indent

        context = context or RenderContext()

        child_context = context.child(
            inside_function=True,
            inside_async=self.is_async,
        )

        decorators_code = ""

        for decorator in self.decorators:
            decorators_code += (
                f"{ind}@{decorator.render(context=context)}\n"
            )

        params_code = ", ".join(self.params)

        prefix = "async " if self.is_async else ""

        if self.body_node:
            body_code = self.body_node.render(
                indent + 1,
                child_context,
            )
        else:
            body_code = (
                "    " * (indent + 1)
                + "pass\n"
            )

        return (
            f"{decorators_code}"
            f"{ind}{prefix}def {self.name}({params_code}):\n"
            f"{body_code}"
        )