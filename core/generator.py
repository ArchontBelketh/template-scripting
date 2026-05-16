from core.context import RenderContext


class PythonGenerator:
    def generate(self, root_node):
        context = RenderContext()

        return root_node.render(
            indent=0,
            context=context,
        )