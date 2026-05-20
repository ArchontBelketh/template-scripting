from core.context import RenderContext

from compiler.ast_generator import (
    ASTGenerator,
)


class PythonGenerator:
    def __init__(
        self,
        use_ast=True,
    ):
        self.use_ast = use_ast

    def generate(self, root_node):
        if self.use_ast:
            generator = ASTGenerator()

            return generator.generate(
                root_node
            )

        context = RenderContext()

        return root_node.render(
            indent=0,
            context=context,
        )