from __future__ import annotations

from core.base_node import BaseNode


class StatementNode(BaseNode):
    CATEGORY = "statement"

    def __init__(self, next_node=None):
        self.next_node = next_node

    def render_next(self, indent, context):
        if not self.next_node:
            return ""

        return self.next_node.render(
            indent,
            context,
        )