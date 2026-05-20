import ast

from registry.node_registry import (
    register_node,
)

from core.context import (
    RenderContext,
)

from core.base_node import (
    BaseNode,
)


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

        self.body_nodes = (
            body_nodes or []
        )

        self.bases = bases or []

        self.decorators = (
            decorators or []
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

        ind = "    " * indent

        child_context = context.child(
            inside_class=True,
        )

        code = ""

        for decorator in self.decorators:
            code += (
                f"{ind}@"
                f"{decorator.render(context=context)}\n"
            )

        bases_code = ""

        if self.bases:
            bases_code = (
                "("
                + ", ".join(
                    self.bases
                )
                + ")"
            )

        code += (
            f"{ind}class "
            f"{self.name}"
            f"{bases_code}:\n"
        )

        if not self.body_nodes:
            code += (
                "    "
                * (indent + 1)
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

        if not body:
            body = [ast.Pass()]

        return ast.ClassDef(
            name=self.name,
            bases=[
                ast.Name(
                    id=base,
                    ctx=ast.Load(),
                )
                for base
                in self.bases
            ],
            keywords=[],
            body=body,
            decorator_list=[
                decorator.build_ast(
                    context
                )
                for decorator
                in self.decorators
            ],
        )