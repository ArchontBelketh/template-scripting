# Архитектура визуальной системы кодогенерации Python

## Структура проекта

```text
project/
│
├── core/
│   ├── base_node.py
│   ├── context.py
│   ├── generator.py
│   ├── exceptions.py
│   └── types.py
│
├── registry/
│   ├── node_registry.py
│   └── node_factory.py
│
├── nodes/
│   ├── base/
│   │   ├── expression_node.py
│   │   ├── statement_node.py
│   │   ├── flow_node.py
│   │   ├── scoped_node.py
│   │   └── executable_node.py
│   │
│   ├── expressions/
│   │   ├── literal_node.py
│   │   ├── variable_node.py
│   │   ├── binary_op_node.py
│   │   ├── unary_op_node.py
│   │   ├── call_node.py
│   │   ├── attribute_node.py
│   │   ├── subscript_node.py
│   │   ├── lambda_node.py
│   │   ├── compare_node.py
│   │   ├── ternary_node.py
│   │   └── await_node.py
│   │
│   ├── statements/
│   │   ├── assign_node.py
│   │   ├── augmented_assign_node.py
│   │   ├── expression_statement_node.py
│   │   ├── return_node.py
│   │   ├── raise_node.py
│   │   ├── break_node.py
│   │   ├── continue_node.py
│   │   ├── pass_node.py
│   │   ├── global_node.py
│   │   └── nonlocal_node.py
│   │
│   ├── flow/
│   │   ├── if_node.py
│   │   ├── while_node.py
│   │   ├── for_node.py
│   │   ├── try_except_node.py
│   │   ├── with_node.py
│   │   └── match_node.py
│   │
│   ├── structures/
│   │   ├── function_node.py
│   │   ├── class_node.py
│   │   ├── module_node.py
│   │   └── decorator_node.py
│   │
│   ├── imports/
│   │   ├── import_node.py
│   │   └── from_import_node.py
│   │
│   └── collections/
│       ├── list_node.py
│       ├── tuple_node.py
│       ├── dict_node.py
│       ├── set_node.py
│       └── comprehension_node.py
│
├── graph/
│   ├── graph.py
│   ├── graph_node.py
│   ├── pin.py
│   ├── connection.py
│   ├── execution_pin.py
│   └── data_pin.py
│
├── serializer/
│   ├── graph_serializer.py
│   ├── graph_deserializer.py
│   └── schemas.py
│
├── compiler/
│   ├── graph_compiler.py
│   ├── dependency_resolver.py
│   └── validation.py
│
├── ui/
│   ├── node_metadata.py
│   ├── node_categories.py
│   └── colors.py
│
├── examples/
│   ├── hello_world.py
│   ├── loops.py
│   └── async_example.py
│
└── main.py
```

---

# Главная идея архитектуры

## НОДЫ САМИ ГЕНЕРИРУЮТ КОД

НЕТ:

- giant switch/case
- central compiler logic
- AST walker
- type dispatch generator

ДА:

```python
node.render(context)
```

Каждый узел знает:

- как рендерить себя
- как рендерить детей
- как продолжать execution flow

Весь генератор:

```python
root.render(context)
```

---

# core/base_node.py

```python
from __future__ import annotations

from abc import ABC, abstractmethod


class BaseNode(ABC):
    NODE_TYPE = "base"
    CATEGORY = "base"
    DISPLAY_NAME = "Base Node"

    @abstractmethod
    def render(self, indent=0, context=None) -> str:
        pass
```

---

# core/context.py

```python
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
```

---

# nodes/base/expression_node.py

```python
from core.base_node import BaseNode


class ExpressionNode(BaseNode):
    CATEGORY = "expression"
```

---

# nodes/base/statement_node.py

```python
from __future__ import annotations

from core.base_node import BaseNode


class StatementNode(BaseNode):
    CATEGORY = "statement"

    def __init__(self, next_node=None):
        self.next_node = next_node

    def render_next(self, indent, context):
        if not self.next_node:
            return ""

        return self.next_node.render(indent, context)
```

---

# nodes/base/flow_node.py

```python
from nodes.base.statement_node import StatementNode


class FlowNode(StatementNode):
    CATEGORY = "flow"
```

---

# nodes/base/scoped_node.py

```python
from core.context import RenderContext


class ScopedNode:
    def create_child_context(self, context: RenderContext):
        return context.child()
```

---

# registry/node_registry.py

```python
NODE_REGISTRY = {}


def register_node(node_class):
    NODE_REGISTRY[node_class.NODE_TYPE] = node_class

    return node_class
```

---

# registry/node_factory.py

```python
from registry.node_registry import NODE_REGISTRY


class NodeFactory:
    @staticmethod
    def create(node_type: str, **kwargs):
        cls = NODE_REGISTRY[node_type]

        return cls(**kwargs)
```

---

# graph/pin.py

```python
class Pin:
    def __init__(
        self,
        name,
        pin_type,
        is_input,
    ):
        self.name = name
        self.pin_type = pin_type
        self.is_input = is_input
```

---

# graph/execution_pin.py

```python
from graph.pin import Pin


class ExecutionPin(Pin):
    def __init__(self, name, is_input):
        super().__init__(
            name=name,
            pin_type="execution",
            is_input=is_input,
        )
```

---

# graph/data_pin.py

```python
from graph.pin import Pin


class DataPin(Pin):
    def __init__(
        self,
        name,
        data_type,
        is_input,
    ):
        super().__init__(
            name=name,
            pin_type=data_type,
            is_input=is_input,
        )
```

---

# graph/connection.py

```python
class Connection:
    def __init__(
        self,
        output_pin,
        input_pin,
    ):
        self.output_pin = output_pin
        self.input_pin = input_pin
```

---

# graph/graph_node.py

```python
class GraphNode:
    def __init__(self, runtime_node):
        self.runtime_node = runtime_node

        self.input_pins = []
        self.output_pins = []
```

---

# graph/graph.py

```python
class Graph:
    def __init__(self):
        self.nodes = []
        self.connections = []
```

---

# Пример полноценной ноды

# nodes/flow/while_node.py

```python
from registry.node_registry import register_node

from nodes.base.flow_node import FlowNode


@register_node
class WhileNode(FlowNode):
    NODE_TYPE = "while"
    DISPLAY_NAME = "While"

    def __init__(
        self,
        condition,
        body_node=None,
        else_node=None,
        next_node=None,
    ):
        super().__init__(next_node)

        self.condition = condition
        self.body_node = body_node
        self.else_node = else_node

    def render(self, indent=0, context=None):
        ind = "    " * indent

        condition_code = self.condition.render(
            context=context,
        )

        loop_context = context.child(
            inside_loop=True,
        )

        if self.body_node:
            body_code = self.body_node.render(
                indent + 1,
                loop_context,
            )
        else:
            body_code = (
                "    " * (indent + 1)
                + "pass\n"
            )

        code = (
            f"{ind}while {condition_code}:\n"
            f"{body_code}"
        )

        if self.else_node:
            else_code = self.else_node.render(
                indent + 1,
                context,
            )

            code += (
                f"{ind}else:\n"
                f"{else_code}"
            )

        code += self.render_next(
            indent,
            context,
        )

        return code
```

---

# Как это будет выглядеть в UI

## Expression Nodes

Только data pins:

```text
[a + b]
● int  ● int
```

---

## Statement Nodes

Execution + data:

```text
exec ▶ [Assign] ▶ exec
        value ●
```

---

## Flow Nodes

Несколько execution outputs:

```text
           ▶ true
exec ▶ [If]
           ▶ false
```

---

# Как создаются новые ноды

## Минимум действий

1. Создать файл
2. Унаследоваться
3. Реализовать render()
4. Добавить pins

ВСЕ.

---

# Пример новой ноды

```python
@register_node
class PrintNode(StatementNode):
    NODE_TYPE = "print"

    def __init__(
        self,
        value,
        next_node=None,
    ):
        super().__init__(next_node)

        self.value = value

    def render(self, indent=0, context=None):
        ind = "    " * indent

        code = (
            f"{ind}print({self.value.render(context=context)})\n"
        )

        return code + self.render_next(
            indent,
            context,
        )
```

---

# Что эта архитектура уже поддерживает

## Без изменений ядра

Можно добавить:

- async/await
- decorators
- generators
- yield
- pattern matching
- dataclass
- comprehensions
- context managers
- type annotations
- imports
- lambdas
- walrus operator
- f-strings
- any future Python syntax

Просто новой нодой.

---

# Почему это лучше AST-based генератора

## AST-based

Проблемы:

- central logic explosion
- giant compiler
- сложно расширять
- type dispatch hell
- сложно дебажить
- сложно сериализовать

---

## Node-template architecture

Плюсы:

- локальная логика
- легко расширять
- easy serialization
- easy UI mapping
- easy graph editing
- easy save/load
- easy custom nodes
- easy plugins
- easy modding

---

# Следующий этап после каркаса

После этого:

## 1. Serializer

Graph -> JSON

## 2. Deserializer

JSON -> Graph

## 3. UI Editor

Drag/drop nodes

## 4. Auto layout

Автоматическое расположение нод

## 5. Type system

Подсветка несовместимых pin connections

## 6. Live preview

Мгновенная генерация Python-кода

## 7. Plugin API

Внешние пакеты смогут добавлять новые ноды

---

# Финальная мысль

Это уже не "генератор Python".

Это:

- визуальный язык программирования
- blueprint system
- node compiler
- programmable graph runtime
- foundation для собственного visual scripting engine

Причем архитектура уже готова для:

- Unreal-like blueprints
- behavior trees
- AI graphs
- shader graphs
- automation graphs
- dialogue graphs
- gameplay scripting
- no-code systems
