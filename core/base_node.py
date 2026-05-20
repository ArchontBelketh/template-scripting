from __future__ import annotations

from abc import ABC, abstractmethod


class BaseNode(ABC):
    NODE_TYPE = "base"
    CATEGORY = "base"
    DISPLAY_NAME = "Base Node"

    @abstractmethod
    def render(
        self,
        indent=0,
        context=None,
    ) -> str:
        pass

    @abstractmethod
    def build_ast(
        self,
        context=None,
    ):
        pass