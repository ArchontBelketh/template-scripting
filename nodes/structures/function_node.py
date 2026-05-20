import ast

from registry.node_registry import (
    register_node,
)

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

    def render(
        self,
        indent=0,
        context=None,
    ):
        ind = "    " * indent

        context = (
            context
            or RenderContext()
        )

        child_context = context.child(
            inside_function=True,
            inside_async=self.is_async,
        )

        decorators_code = ""

        for decorator in self.decorators:
            decorators_code += (
                f"{ind}@"
                f"{decorator.render(context=context)}\n"
            )

        params_code = ", ".join(
            self.params
        )

        prefix = (
            "async "
            if self.is_async
            else ""
        )

        if self.body_node:
            body_code = (
                self.body_node.render(
                    indent + 1,
                    child_context,
                )
            )
        else:
            body_code = (
                "    "
                * (indent + 1)
                + "pass\n"
            )

        return (
            f"{decorators_code}"
            f"{ind}{prefix}"
            f"def {self.name}"
            f"({params_code}):\n"
            f"{body_code}"
        )

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

        args = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg=name)
                for name in self.params
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        )

        function_class = (
            ast.AsyncFunctionDef
            if self.is_async
            else ast.FunctionDef
        )

        return function_class(
            name=self.name,
            args=args,
            body=body,
            decorator_list=[
                decorator.build_ast(
                    context
                )
                for decorator
                in self.decorators
            ],
        )