from dataclasses import dataclass, field


@dataclass
class RenderContext:
    inside_function: bool = False
    inside_loop: bool = False
    inside_class: bool = False
    inside_async: bool = False

    imports: set[str] = field(default_factory=set)

    scope_stack: list[str] = field(default_factory=list)

    def child(self, **kwargs):
        data = {
            "inside_function": self.inside_function,
            "inside_loop": self.inside_loop,
            "inside_class": self.inside_class,
            "inside_async": self.inside_async,
            "imports": self.imports,
            "scope_stack": self.scope_stack.copy(),
        }

        data.update(kwargs)

        return RenderContext(**data)