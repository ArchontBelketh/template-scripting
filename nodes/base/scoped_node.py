from core.context import RenderContext


class ScopedNode:
    def create_child_context(
        self,
        context: RenderContext,
        **kwargs,
    ):
        return context.child(**kwargs)