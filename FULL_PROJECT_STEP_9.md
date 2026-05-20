# Документация проекта: template-scripting

**Корневая директория:** `C:\portfolio\template-scripting`

## Структура проекта

```
template-scripting/
├── compiler/
│   └── graph_compiler.py
├── core/
│   ├── base_node.py
│   ├── context.py
│   ├── exceptions.py
│   ├── generator.py
│   ├── type_inference.py
│   ├── type_system.py
│   ├── type_validation.py
│   └── types.py
├── examples/
├── graph/
│   ├── auto_layout.py
│   ├── connection.py
│   ├── data_pin.py
│   ├── execution_pin.py
│   ├── graph.py
│   ├── graph_node.py
│   ├── pin.py
│   ├── tracer.py
│   ├── type_propagator.py
│   └── validator.py
├── nodes/
│   ├── base/
│   │   ├── executable_node.py
│   │   ├── expression_node.py
│   │   ├── flow_node.py
│   │   ├── scoped_node.py
│   │   └── statement_node.py
│   ├── collections/
│   ├── expressions/
│   │   ├── attribute_node.py
│   │   ├── await_node.py
│   │   ├── binary_op_node.py
│   │   ├── call_node.py
│   │   ├── dict_node.py
│   │   ├── list_comprehension_node.py
│   │   ├── list_node.py
│   │   ├── literal_node.py
│   │   └── variable_node.py
│   ├── flow/
│   │   ├── if_node.py
│   │   └── while_node.py
│   ├── imports/
│   │   ├── from_import_node.py
│   │   └── import_node.py
│   ├── statements/
│   │   ├── assign_node.py
│   │   ├── expression_statement_node.py
│   │   ├── import_statement_node.py
│   │   ├── pass_node.py
│   │   └── return_node.py
│   └── structures/
│       ├── class_node.py
│       ├── function_node.py
│       └── module_node.py
├── plugins/
│   └── example_plugin.py
├── registry/
│   ├── node_factory.py
│   ├── node_registry.py
│   └── plugin_manager.py
├── serializer/
│   ├── graph_loader.py
│   └── graph_serializer.py
├── ui/
│   ├── app/
│   │   ├── app.py
│   │   └── main_window.py
│   ├── editor/
│   │   ├── clipboard.py
│   │   ├── commands.py
│   │   ├── connection_item.py
│   │   ├── graph_scene.py
│   │   ├── graph_view.py
│   │   ├── history.py
│   │   ├── node_item.py
│   │   ├── node_search_popup.py
│   │   ├── pin_item.py
│   │   └── reroute_node_item.py
│   ├── runtime/
│   │   └── runtime_graph.py
│   ├── styling/
│   │   ├── colors.py
│   │   ├── metrics.py
│   │   └── type_colors.py
│   ├── widgets/
│   │   ├── code_preview.py
│   │   ├── inspector_panel.py
│   │   ├── node_palette.py
│   │   └── type_hint_widget.py
│   └── node_metadata.py
├── .gitattributes
├── .gitignore
├── main.py
├── README.md
├── Roadmap_to_step12.txt
├── Roadmap_to_step5.txt
└── Warnings.txt
```

## Исходный код Python

### `compiler/graph_compiler.py`

```python
from core.generator import PythonGenerator

from graph.validator import GraphValidator
from graph.tracer import ExecutionTracer

from nodes.structures.module_node import ModuleNode
from nodes.structures.function_node import FunctionNode

from nodes.statements.expression_statement_node import (
    ExpressionStatementNode,
)

from nodes.statements.assign_node import AssignNode
from nodes.statements.return_node import ReturnNode

from nodes.flow.if_node import IfNode
from nodes.flow.while_node import WhileNode

from nodes.expressions.call_node import CallNode
from nodes.expressions.literal_node import LiteralNode
from nodes.expressions.variable_node import VariableNode
from nodes.expressions.binary_op_node import BinaryOpNode


class GraphCompiler:
    def __init__(self, graph):
        self.graph = graph

        self.validator = GraphValidator(
            graph
        )

        self.tracer = ExecutionTracer()

        self.expression_cache = {}

        self.node_compilers = {
            "print": self.compile_print_node,
            "branch": self.compile_branch_node,
            "while": self.compile_while_node,
            "assign": self.compile_assign_node,
            "return": self.compile_return_node,
        }

    def compile(self):
        self.graph.propagate_types()
        errors = self.validator.validate()

        if errors:
            return "\n".join(
                f"# ERROR: {error}"
                for error in errors
            )

        start_node = self.graph.find_node_by_type(
            "start"
        )

        if not start_node:
            return "# ERROR: Start node not found"

        execution_root = self.resolve_execution_tree(
            start_node
        )

        main_function = FunctionNode(
            name="main",
            body_node=execution_root,
        )

        module = ModuleNode(
            body_nodes=[
                main_function,
            ]
        )

        generator = PythonGenerator()

        return generator.generate(module)

    def resolve_execution_tree(
        self,
        start_node,
    ):
        visited = set()

        return self.walk_execution(
            start_node,
            visited,
        )

    def walk_execution(
        self,
        node,
        visited,
    ):
        if not node:
            return None

        if node.node_id in visited:
            return None

        visited.add(node.node_id)

        self.tracer.trace_node(node)

        compiled = self.compile_node(node)

        if compiled is None:
            next_node = self.get_execution_target(
                node,
                "next",
            )

            return self.walk_execution(
                next_node,
                visited,
            )

        if isinstance(compiled, IfNode):
            true_target = self.get_execution_target(
                node,
                "true",
            )

            false_target = self.get_execution_target(
                node,
                "false",
            )

            compiled.true_node = self.walk_execution(
                true_target,
                visited.copy(),
            )

            compiled.false_node = self.walk_execution(
                false_target,
                visited.copy(),
            )

            return compiled

        if isinstance(compiled, WhileNode):
            loop_target = self.get_execution_target(
                node,
                "loop",
            )

            next_target = self.get_execution_target(
                node,
                "next",
            )

            compiled.body_node = self.walk_execution(
                loop_target,
                visited.copy(),
            )

            compiled.next_node = self.walk_execution(
                next_target,
                visited.copy(),
            )

            return compiled

        next_node = self.get_execution_target(
            node,
            "next",
        )

        compiled.next_node = self.walk_execution(
            next_node,
            visited,
        )

        return compiled

    def compile_node(self, graph_node):
        if graph_node.node_type == "start":
            return None

        compiler = self.node_compilers.get(
            graph_node.node_type
        )

        if not compiler:
            return None

        return compiler(graph_node)

    def compile_print_node(self, graph_node):
        value = self.resolve_input_expression(
            graph_node,
            "value",
        )

        if not value:
            value = LiteralNode(
                graph_node.properties.get(
                    "value",
                    "Hello World",
                )
            )

        call = CallNode(
            func=VariableNode("print"),
            args=[value],
        )

        return ExpressionStatementNode(
            expression=call,
        )

    def compile_assign_node(self, graph_node):
        variable_name = graph_node.properties.get(
            "variable",
            "value",
        )

        value = self.resolve_input_expression(
            graph_node,
            "value",
        )

        if not value:
            value = LiteralNode(0)

        return AssignNode(
            target=VariableNode(variable_name),
            value=value,
        )

    def compile_return_node(self, graph_node):
        value = self.resolve_input_expression(
            graph_node,
            "value",
        )

        return ReturnNode(value)

    def compile_branch_node(self, graph_node):
        condition = self.resolve_input_expression(
            graph_node,
            "condition",
        )

        if not condition:
            condition = LiteralNode(True)

        return IfNode(condition)

    def compile_while_node(self, graph_node):
        condition = self.resolve_input_expression(
            graph_node,
            "condition",
        )

        if not condition:
            condition = LiteralNode(True)

        return WhileNode(condition)

    def resolve_input_expression(
        self,
        node,
        pin_name,
    ):
        pin = self.find_input_pin(
            node,
            pin_name,
        )

        if not pin:
            return None

        if not pin.connections:
            return None

        connection = pin.connections[0]

        source_node = (
            connection.output_pin.owner
        )

        return self.compile_expression_node(
            source_node
        )

    def compile_expression_node(
        self,
        node,
    ):
        if node.node_id in self.expression_cache:
            return self.expression_cache[
                node.node_id
            ]

        expression = None

        if node.node_type == "literal":
            expression = LiteralNode(
                node.properties.get("value")
            )

        elif node.node_type == "variable":
            expression = VariableNode(
                node.properties.get(
                    "name",
                    "value",
                )
            )

        elif node.node_type == "add":
            left = self.resolve_input_expression(
                node,
                "left",
            )

            right = self.resolve_input_expression(
                node,
                "right",
            )

            expression = BinaryOpNode(
                left,
                "+",
                right,
            )

        elif node.node_type == "subtract":
            left = self.resolve_input_expression(
                node,
                "left",
            )

            right = self.resolve_input_expression(
                node,
                "right",
            )

            expression = BinaryOpNode(
                left,
                "-",
                right,
            )

        elif node.node_type == "greater":
            left = self.resolve_input_expression(
                node,
                "left",
            )

            right = self.resolve_input_expression(
                node,
                "right",
            )

            expression = BinaryOpNode(
                left,
                ">",
                right,
            )

        self.expression_cache[
            node.node_id
        ] = expression

        return expression

    def find_input_pin(
        self,
        node,
        pin_name,
    ):
        for pin in node.input_pins:
            if pin.name == pin_name:
                return pin

        return None

    def get_execution_target(
        self,
        node,
        pin_name,
    ):
        for pin in node.output_pins:
            if pin.name != pin_name:
                continue

            if not pin.connections:
                return None

            return pin.connections[0].input_pin.owner

        return None
```

### `core/base_node.py`

```python
import uuid
from typing import Optional, Dict
from graph.graph_node import GraphNode
from graph.data_pin import DataPin
from core.context import RenderContext


class BaseNode(GraphNode):
    def __init__(self, node_id: Optional[str] = None, node_type: str = "base", title: str = "Base", properties: Optional[dict] = None):
        # Если node_id не передан (как при ручной сборке дерева), создаем уникальный
        uid = node_id if node_id is not None else f"{node_type}_{uuid.uuid4().hex[:8]}"
        super().__init__(uid, node_type, title)
        
        self.properties: Dict[str, str] = properties if properties is not None else {}

    def render(self, context: RenderContext) -> str:
        raise NotImplementedError("Каждая нода должна реализовывать метод render()")

    def infer_output_types(self):
        pass

    def get_input_value(self, pin_name: str, context: RenderContext) -> str:
        pin = self.inputs.get(pin_name)
        if not pin or not isinstance(pin, DataPin):
            return ""

        if pin.is_connected():
            source_pin = pin.connections[0].source_pin
            return source_pin.node.render_expression(source_pin.name, context)
        
        return self.properties.get(pin_name, pin.default_value)

    def render_expression(self, pin_name: str, context: RenderContext) -> str:
        return ""
```

### `core/context.py`

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

### `core/exceptions.py`

```python
class NodeValidationError(Exception):
    pass


class RenderError(Exception):
    pass

class GraphValidationError(Exception):
    pass


class ConnectionValidationError(Exception):
    pass
```

### `core/generator.py`

```python
from core.context import RenderContext


class PythonGenerator:
    def generate(self, root_node):
        context = RenderContext()

        return root_node.render(
            indent=0,
            context=context,
        )
```

### `core/type_inference.py`

```python
import ast
from core.type_system import (
    TypeInfo,
    INT_TYPE,
    FLOAT_TYPE,
    STRING_TYPE,
    BOOL_TYPE,
    ANY_TYPE,
    LIST_TYPE,
    DICT_TYPE,
    UNION_TYPE,
)


class TypeInferenceEngine:
    @staticmethod
    def infer_from_value(value: str) -> TypeInfo:
        """Определяет TypeInfo на основе строкового представления значения литерала."""
        if not value or value.strip() == "":
            return ANY_TYPE

        try:
            parsed = ast.parse(value, mode="eval")
            return TypeInferenceEngine.infer_from_ast_node(parsed.body)
        except Exception:
            # Если это не валидный литерал Python, считаем это строкой или произвольным кодом
            return STRING_TYPE

    @staticmethod
    def infer_from_ast_node(node: ast.AST) -> TypeInfo:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                return BOOL_TYPE
            if isinstance(node.value, int):
                return INT_TYPE
            if isinstance(node.value, float):
                return FLOAT_TYPE
            if isinstance(node.value, str):
                return STRING_TYPE
            if node.value is None:
                return ANY_TYPE

        elif isinstance(node, ast.List):
            if not node.elts:
                return LIST_TYPE(ANY_TYPE)
            element_types = [TypeInferenceEngine.infer_from_ast_node(el) for el in node.elts]
            return LIST_TYPE(UNION_TYPE(element_types))

        elif isinstance(node, ast.Dict):
            if not node.keys:
                return DICT_TYPE(ANY_TYPE, ANY_TYPE)
            key_types = [TypeInferenceEngine.infer_from_ast_node(k) for k in node.keys if k is not None]
            val_types = [TypeInferenceEngine.infer_from_ast_node(v) for v in node.values]
            return DICT_TYPE(UNION_TYPE(key_types), UNION_TYPE(val_types))

        return ANY_TYPE
```

### `core/type_system.py`

```python
from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class TypeInfo:
    name: str  # "int", "float", "str", "bool", "list", "dict", "union", "any", "exec"
    generic_args: List["TypeInfo"] = field(default_factory=list)
    is_optional: bool = False

    def matches(self, other: "TypeInfo") -> bool:
        # 'any' совпадает с абсолютно любым типом
        if self.name == "any" or other.name == "any":
            return True

        # Если один из типов Union, проверяем вхождение
        if self.name == "union":
            return any(arg.matches(other) for arg in self.generic_args)
        if other.name == "union":
            return any(self.matches(arg) for arg in other.generic_args)

        # Проверка опциональности (nullable)
        if self.is_optional != other.is_optional and not (self.is_optional or other.is_optional):
            return False

        # Базовая проверка имени типа
        if self.name != other.name:
            # Поддержка безопасного неявного приведения (Type Casting): int -> float
            if self.name == "int" and other.name == "float":
                return True
            return False

        # Рекурсивная проверка Generics (например, list[int] vs list[str])
        if self.generic_args and other.generic_args:
            if len(self.generic_args) != len(other.generic_args):
                return False
            return all(g1.matches(g2) for g1, g2 in zip(self.generic_args, other.generic_args))

        return True

    def __str__(self) -> str:
        opt_str = "?" if self.is_optional else ""
        if self.name == "union":
            return f"({' | '.join(str(arg) for arg in self.generic_args)}){opt_str}"
        if self.generic_args:
            args_str = ", ".join(str(arg) for arg in self.generic_args)
            return f"{self.name}[{args_str}]{opt_str}"
        return f"{self.name}{opt_str}"


# Предопределенные константы базовых типов данных
ANY_TYPE = TypeInfo(name="any")
EXEC_TYPE = TypeInfo(name="exec")
INT_TYPE = TypeInfo(name="int")
FLOAT_TYPE = TypeInfo(name="float")
STRING_TYPE = TypeInfo(name="str")
BOOL_TYPE = TypeInfo(name="bool")


def LIST_TYPE(element_type: TypeInfo) -> TypeInfo:
    return TypeInfo(name="list", generic_args=[element_type])


def DICT_TYPE(key_type: TypeInfo, value_type: TypeInfo) -> TypeInfo:
    return TypeInfo(name="dict", generic_args=[key_type, value_type])


def UNION_TYPE(types: List[TypeInfo]) -> TypeInfo:
    # Плоское развертывание вложенных Union
    flat_types: Set[TypeInfo] = set()
    for t in types:
        if t.name == "union":
            flat_types.update(t.generic_args)
        else:
            flat_types.add(t)
    if len(flat_types) == 1:
        return list(flat_types)[0]
    return TypeInfo(name="union", generic_args=sorted(list(flat_types), key=lambda x: x.name))


def OPTIONAL_TYPE(base_type: TypeInfo) -> TypeInfo:
    return TypeInfo(name=base_type.name, generic_args=base_type.generic_args, is_optional=True)
```

### `core/type_validation.py`

```python
from core.type_system import TypeInfo


class TypeValidationEngine:
    @staticmethod
    def validate_connection(source_type: TypeInfo, target_type: TypeInfo) -> bool:
        """Проверяет допустимость связи между выходным и входным пинами."""
        if source_type.name == "exec" or target_type.name == "exec":
            return source_type.name == target_type.name
        return source_type.matches(target_type)
```

### `core/types.py`

```python
from core.type_system import TypeInfo, ANY_TYPE


def normalize_type(type_obj: TypeInfo) -> TypeInfo:
    """Приводит тип к каноничному виду."""
    if not isinstance(type_obj, TypeInfo):
        return ANY_TYPE
    return type_obj


def is_type_compatible(source: TypeInfo, target: TypeInfo) -> bool:
    """Проверяет, можно ли передать данные из source в target."""
    if source is None or target is None:
        return False
    return source.matches(target)


def auto_cast_expression(source_expr: str, source_type: TypeInfo, target_type: TypeInfo) -> str:
    """Генерирует код явного приведения типов, если это необходимо."""
    if source_type.name == "int" and target_type.name == "float":
        return source_expr  # Неявное аппроксимирование в Python разрешено
    if source_type.name != target_type.name:
        if target_type.name == "str":
            return f"str({source_expr})"
        if target_type.name == "int" and source_type.name == "float":
            return f"int({source_expr})"
        if target_type.name == "float" and source_type.name == "str":
            return f"float({source_expr})"
    return source_expr
```

### `graph/auto_layout.py`

```python
class GraphAutoLayout:
    def __init__(self, graph):
        self.graph = graph

    def apply(self):
        x = 0
        y = 0

        spacing_x = 450

        for node in self.graph.nodes:
            node.position = (
                x,
                y,
            )

            x += spacing_x
```

### `graph/connection.py`

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graph.pin import Pin


class Connection:
    def __init__(self, source_pin: "Pin", target_pin: "Pin"):
        self.source_pin: "Pin" = source_pin
        self.target_pin: "Pin" = target_pin

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return self.source_pin == other.source_pin and self.target_pin == other.target_pin
```

### `graph/data_pin.py`

```python
from graph.pin import Pin
from core.type_system import TypeInfo, ANY_TYPE


class DataPin(Pin):
    def __init__(self, name: str, direction: str, pin_type: TypeInfo = ANY_TYPE, default_value: str = ""):
        super().__init__(name, direction, pin_type)
        self.default_value: str = default_value
```

### `graph/execution_pin.py`

```python
from graph.pin import Pin
from core.type_system import EXEC_TYPE


class ExecutionPin(Pin):
    def __init__(self, name: str, direction: str):
        super().__init__(name, direction, EXEC_TYPE)
```

### `graph/graph.py`

```python
from typing import Dict
from graph.graph_node import GraphNode
from graph.connection import Connection
from graph.type_propagator import GraphTypePropagator


class Graph:
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.connections: list[Connection] = []

    def add_node(self, node: GraphNode):
        self.nodes[node.id] = node

    def remove_node(self, node_id: str):
        if node_id in self.nodes:
            # Удаляем связи ноды перед удалением самой ноды
            node = self.nodes[node_id]
            for pin in list(node.inputs.values()) + list(node.outputs.values()):
                for conn in list(pin.connections):
                    self.remove_connection(conn)
            del self.nodes[node_id]

    def add_connection(self, source_node_id: str, source_pin_name: str, target_node_id: str, target_pin_name: str):
        source_node = self.nodes.get(source_node_id)
        target_node = self.nodes.get(target_node_id)

        if source_node and target_node:
            source_pin = source_node.outputs.get(source_pin_name)
            target_pin = target_node.inputs.get(target_pin_name)

            if source_pin and target_pin:
                connection = Connection(source_pin, target_pin)
                source_pin.connections.append(connection)
                target_pin.connections.append(connection)
                self.connections.append(connection)
                self.propagate_types()

    def remove_connection(self, connection: Connection):
        if connection in self.connections:
            connection.source_pin.connections.remove(connection)
            connection.target_pin.connections.remove(connection)
            self.connections.remove(connection)
            self.propagate_types()

    def propagate_types(self):
        """Запускает процесс обновления типов данных на пинах по всему графу."""
        propagator = GraphTypePropagator(self)
        propagator.propagate()
```

### `graph/graph_node.py`

```python
class GraphNode:
    def __init__(
        self,
        node_id,
        node_type,
        title,
        position=(0, 0),
        properties=None,
    ):
        self.node_id = node_id

        self.node_type = node_type
        self.title = title

        self.position = position

        self.properties = properties or {}

        self.input_pins = []
        self.output_pins = []

    def add_input_pin(self, pin):
        pin.owner = self
        self.input_pins.append(pin)

    def add_output_pin(self, pin):
        pin.owner = self
        self.output_pins.append(pin)

    def get_input_pin(self, name):
        for pin in self.input_pins:
            if pin.name == name:
                return pin

        return None

    def get_output_pin(self, name):
        for pin in self.output_pins:
            if pin.name == name:
                return pin

        return None
```

### `graph/pin.py`

```python
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from graph.connection import Connection
    from core.type_system import TypeInfo


class Pin:
    def __init__(self, name: str, direction: str, pin_type: "TypeInfo"):
        self.name: str = name
        self.direction: str = direction  # "input" или "output"
        self.pin_type: "TypeInfo" = pin_type
        self.inferred_type: Optional["TypeInfo"] = None
        self.node = None  # Заполняется при добавлении в ноду
        self.connections: List["Connection"] = []

    @property
    def effective_type(self) -> "TypeInfo":
        """Возвращает выведенный тип, если он есть, иначе базовый объявленный."""
        if self.direction == "input" and self.connections:
            # Входной пин наследует тип от присоединенного выхода
            source_pin = self.connections[0].source_pin
            return source_pin.effective_type
        return self.inferred_type if self.inferred_type else self.pin_type

    def is_connected(self) -> bool:
        return len(self.connections) > 0
```

### `graph/tracer.py`

```python
class ExecutionTracer:
    def __init__(self):
        self.execution_log = []

    def clear(self):
        self.execution_log.clear()

    def trace_node(self, node):
        self.execution_log.append(
            {
                "node_id": node.node_id,
                "node_type": node.node_type,
                "title": node.title,
            }
        )

    def get_log(self):
        return self.execution_log.copy()
```

### `graph/type_propagator.py`

```python
class GraphTypePropagator:
    def __init__(self, graph):
        self.graph = graph

    def propagate(self):
        """Проводит распространение типов по графу до стабилизации изменений."""
        iterations = 0
        max_iterations = 20
        changed = True

        while changed and iterations < max_iterations:
            changed = False
            iterations += 1

            for node in self.graph.nodes.values():
                # Каждая нода сама вычисляет свои выходные типы на основе входных данных
                if hasattr(node, "infer_output_types"):
                    old_types = {p.name: p.inferred_type for p in node.outputs.values()}
                    node.infer_output_types()
                    new_types = {p.name: p.inferred_type for p in node.outputs.values()}

                    if old_types != new_types:
                        changed = True
```

### `graph/validator.py`

```python
from typing import List, Set
from graph.graph import Graph
from core.type_validation import TypeValidationEngine


class GraphValidator:
    @staticmethod
    def validate(graph: Graph) -> List[str]:
        errors: List[str] = []
        
        # 1. Проверка типов подключений данных
        for conn in graph.connections:
            src_type = conn.source_pin.effective_type
            tgt_type = conn.target_pin.effective_type
            
            if not TypeValidationEngine.validate_connection(src_type, tgt_type):
                errors.append(
                    f"Несовместимые типы: нельзя подключить пин '{conn.source_pin.node.title}.{conn.source_pin.name}' "
                    f"({src_type}) к пину '{conn.target_pin.node.title}.{conn.target_pin.name}' ({tgt_type})."
                )

        # 2. Поиск циклов в графе исполнения (DFS)
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()

        def dfs_check_cycles(node_id: str) -> bool:
            visited.add(node_id)
            recursion_stack.add(node_id)

            node = graph.nodes.get(node_id)
            if node:
                for out_pin in node.outputs.values():
                    if out_pin.pin_type.name == "exec":
                        for conn in out_pin.connections:
                            neighbor_id = conn.target_pin.node.id
                            if neighbor_id not in visited:
                                if dfs_check_cycles(neighbor_id):
                                    return True
                            elif neighbor_id in recursion_stack:
                                return True

            recursion_stack.remove(node_id)
            return False

        for node_id in graph.nodes:
            if node_id not in visited:
                if dfs_check_cycles(node_id):
                    errors.append("В графе исполнения обнаружен цикл!")
                    break

        return errors
```

### `main.py`

```python
import sys
from ui.app.app import run_app
from core.generator import PythonGenerator

from nodes.structures.module_node import ModuleNode
from nodes.structures.class_node import ClassNode
from nodes.structures.function_node import FunctionNode
from nodes.imports.import_node import ImportNode
from nodes.statements.expression_statement_node import ExpressionStatementNode
from nodes.statements.return_node import ReturnNode

from nodes.expressions.variable_node import VariableNode
from nodes.expressions.literal_node import LiteralNode
from nodes.expressions.call_node import CallNode
from nodes.expressions.attribute_node import AttributeNode
from nodes.expressions.await_node import AwaitNode
from nodes.expressions.list_comprehension_node import ListComprehensionNode
from nodes.expressions.binary_op_node import BinaryOpNode
from nodes.expressions.list_node import ListNode


# 1. Сборка нод импорта и асинхронного вызова
import_asyncio = ImportNode("asyncio")

sleep_call = AwaitNode(
    CallNode(
        func=AttributeNode(
            VariableNode("asyncio"),
            "sleep",
        ),
        args=[
            LiteralNode(1),
        ],
    )
)

print_statement = ExpressionStatementNode(
    expression=CallNode(
        func=VariableNode("print"),
        args=[
            LiteralNode("async works"),
        ],
    ),
)

sleep_statement = ExpressionStatementNode(
    expression=sleep_call,
    next_node=print_statement,
)

async_function = FunctionNode(
    name="load_data",
    body_node=sleep_statement,
    is_async=True,
)

# 2. Построение List Comprehension с явным использованием именованных аргументов
comprehension = ListComprehensionNode(
    expression=BinaryOpNode(
        left=VariableNode("x"),
        op="*",
        right=LiteralNode(2),
    ),
    variable_name="x",
    iterable=ListNode(
        elements=[
            LiteralNode(1),
            LiteralNode(2),
            LiteralNode(3),
        ]
    ),
)

return_statement = ReturnNode(
    comprehension,
)

method = FunctionNode(
    name="build",
    params=["self"],
    body_node=return_statement,
)

example_class = ClassNode(
    name="DataBuilder",
    body_nodes=[
        method,
    ],
)

module = ModuleNode(
    body_nodes=[
        import_asyncio,
        async_function,
        example_class,
    ]
)

# 3. Генерация кода в консоль
generator = PythonGenerator()

print("--- СГЕНЕРИРОВАННЫЙ PYTHON КОД ---")
print(generator.generate(module))
print("----------------------------------")


# 4. Безопасный запуск UI-приложения
if __name__ == "__main__":
    # Патчим MainWindow.create_demo_graph перед запуском, чтобы защититься от KeyError: 'start'
    # если в метаданных проекта отсутствует конфигурация для демонстрационных нод.
    from ui.app.main_window import MainWindow
    original_create_demo = MainWindow.create_demo_graph
    
    def safe_create_demo_graph(self):
        try:
            original_create_demo(self)
        except KeyError as e:
            print(f"[UI Warning] Не удалось загрузить демо-граф: отсутствует нода типа {e}. Открываем чистый холст.")
            if hasattr(self, "graph"):
                self.graph.clear()

    MainWindow.create_demo_graph = safe_create_demo_graph

    # Запускаем приложение PySide6
    run_app()
```

### `nodes/base/executable_node.py`

```python
class ExecutableNode:
    pass
```

### `nodes/base/expression_node.py`

```python
from core.base_node import BaseNode


class ExpressionNode(BaseNode):
    CATEGORY = "expression"
```

### `nodes/base/flow_node.py`

```python
from nodes.base.statement_node import StatementNode


class FlowNode(StatementNode):
    CATEGORY = "flow"
```

### `nodes/base/scoped_node.py`

```python
from core.context import RenderContext


class ScopedNode:
    def create_child_context(
        self,
        context: RenderContext,
        **kwargs,
    ):
        return context.child(**kwargs)
```

### `nodes/base/statement_node.py`

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

        return self.next_node.render(
            indent,
            context,
        )
```

### `nodes/expressions/attribute_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class AttributeNode(ExpressionNode):
    NODE_TYPE = "attribute"
    DISPLAY_NAME = "Attribute"

    def __init__(
        self,
        value,
        attribute,
    ):
        self.value = value
        self.attribute = attribute

    def render(self, indent=0, context=None):
        value_code = self.value.render(
            context=context,
        )

        return f"{value_code}.{self.attribute}"
```

### `nodes/expressions/await_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class AwaitNode(ExpressionNode):
    NODE_TYPE = "await"
    DISPLAY_NAME = "Await"

    def __init__(self, expression):
        self.expression = expression

    def render(self, indent=0, context=None):
        expression_code = self.expression.render(
            context=context,
        )

        return f"await {expression_code}"
```

### `nodes/expressions/binary_op_node.py`

```python
from nodes.base.expression_node import ExpressionNode
from graph.data_pin import DataPin
from core.context import RenderContext
from core.type_system import ANY_TYPE, INT_TYPE, FLOAT_TYPE, STRING_TYPE, UNION_TYPE


class BinaryOpNode(ExpressionNode):
    def __init__(self, left=None, op: str = "+", right=None, node_id: str = None, properties: dict = None):
        props = properties if properties is not None else {}
        props["op"] = op
            
        super().__init__(node_id=node_id, node_type="binary_op", title=f"Binary Operation ({op})", properties=props)
        
        self.left = left
        self.op = op
        self.right = right
        
        self.add_input_pin(DataPin("a", "input", ANY_TYPE, "0"))
        self.add_input_pin(DataPin("b", "input", ANY_TYPE, "0"))
        self.add_output_pin(DataPin("output", "output", ANY_TYPE))

    def infer_output_types(self):
        if self.left and hasattr(self.left, "infer_output_types"):
            self.left.infer_output_types()
            type_a = self.left.outputs["output"].effective_type if "output" in self.left.outputs else ANY_TYPE
        else:
            type_a = self.inputs["a"].effective_type

        if self.right and hasattr(self.right, "infer_output_types"):
            self.right.infer_output_types()
            type_b = self.right.outputs["output"].effective_type if "output" in self.right.outputs else ANY_TYPE
        else:
            type_b = self.inputs["b"].effective_type

        current_op = self.properties.get("op", self.op)

        if current_op in ["+", "-", "*", "/"]:
            if type_a.name == "float" or type_b.name == "float":
                self.outputs["output"].inferred_type = FLOAT_TYPE
            elif type_a.name == "int" and type_b.name == "int":
                self.outputs["output"].inferred_type = FLOAT_TYPE if current_op == "/" else INT_TYPE
            elif current_op == "+" and (type_a.name == "str" or type_b.name == "str"):
                self.outputs["output"].inferred_type = STRING_TYPE
            else:
                self.outputs["output"].inferred_type = UNION_TYPE([type_a, type_b])
        else:
            self.outputs["output"].inferred_type = ANY_TYPE

    def render_expression(self, pin_name: str, context: RenderContext) -> str:
        # Важно: если поднода — это выражение, вызываем render_expression, иначе обычный render
        if self.left:
            expr_a = self.left.render_expression("output", context) if hasattr(self.left, "render_expression") else self.left.render(context)
        else:
            expr_a = self.get_input_value("a", context)

        if self.right:
            expr_b = self.right.render_expression("output", context) if hasattr(self.right, "render_expression") else self.right.render(context)
        else:
            expr_b = self.get_input_value("b", context)
        
        current_op = self.properties.get("op", self.op)
        return f"({expr_a} {current_op} {expr_b})"

    def render(self, context: RenderContext) -> str:
        return self.render_expression("output", context)
```

### `nodes/expressions/call_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class CallNode(ExpressionNode):
    NODE_TYPE = "call"
    DISPLAY_NAME = "Call"

    def __init__(
        self,
        func,
        args=None,
        kwargs=None,
    ):
        self.func = func

        self.args = args or []
        self.kwargs = kwargs or {}

    def render(self, indent=0, context=None):
        func_code = self.func.render(
            context=context,
        )

        positional = [
            arg.render(context=context)
            for arg in self.args
        ]

        keyword = [
            (
                f"{key}="
                f"{value.render(context=context)}"
            )
            for key, value in self.kwargs.items()
        ]

        args_code = ", ".join(
            positional + keyword
        )

        return f"{func_code}({args_code})"
```

### `nodes/expressions/dict_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class DictNode(ExpressionNode):
    NODE_TYPE = "dict"
    DISPLAY_NAME = "Dict"

    def __init__(self, items=None):
        self.items = items or []

    def render(self, indent=0, context=None):
        parts = []

        for key, value in self.items:
            key_code = key.render(
                context=context,
            )

            value_code = value.render(
                context=context,
            )

            parts.append(
                f"{key_code}: {value_code}"
            )

        return "{%s}" % ", ".join(parts)
```

### `nodes/expressions/list_comprehension_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class ListComprehensionNode(ExpressionNode):
    NODE_TYPE = "list_comprehension"
    DISPLAY_NAME = "List Comprehension"

    def __init__(
        self,
        expression,
        variable_name,
        iterable,
        condition=None,
    ):
        self.expression = expression
        self.variable_name = variable_name
        self.iterable = iterable
        self.condition = condition

    def render(self, indent=0, context=None):
        expression_code = self.expression.render(
            context=context,
        )

        iterable_code = self.iterable.render(
            context=context,
        )

        code = (
            f"[{expression_code} "
            f"for {self.variable_name} "
            f"in {iterable_code}"
        )

        if self.condition:
            condition_code = self.condition.render(
                context=context,
            )

            code += f" if {condition_code}"

        code += "]"

        return code
```

### `nodes/expressions/list_node.py`

```python
from nodes.base.expression_node import ExpressionNode
from graph.data_pin import DataPin
from core.context import RenderContext
from core.type_system import ANY_TYPE, LIST_TYPE, UNION_TYPE


class ListNode(ExpressionNode):
    def __init__(self, elements=None, node_id: str = None, properties: dict = None):
        props = properties if properties is not None else {}
        super().__init__(node_id=node_id, node_type="create_list", title="Create List", properties=props)
        
        self.elements = elements if elements is not None else []
        
        self.add_input_pin(DataPin("item0", "input", ANY_TYPE, "None"))
        self.add_input_pin(DataPin("item1", "input", ANY_TYPE, "None"))
        self.add_input_pin(DataPin("item2", "input", ANY_TYPE, "None"))
        self.add_output_pin(DataPin("list", "output", LIST_TYPE(ANY_TYPE)))

    def infer_output_types(self):
        types = []
        if self.elements:
            for el in self.elements:
                if hasattr(el, "infer_output_types"):
                    el.infer_output_types()
                if hasattr(el, "outputs") and "output" in el.outputs:
                    types.append(el.outputs["output"].effective_type)
                elif hasattr(el, "outputs") and "list" in el.outputs:
                    types.append(el.outputs["list"].effective_type)
                else:
                    types.append(ANY_TYPE)
        else:
            types = [
                self.inputs["item0"].effective_type,
                self.inputs["item1"].effective_type,
                self.inputs["item2"].effective_type
            ]
            
        element_type = UNION_TYPE(types)
        self.outputs["list"].inferred_type = LIST_TYPE(element_type)

    def render_expression(self, pin_name: str, context: RenderContext) -> str:
        if self.elements:
            rendered_elms = []
            for el in self.elements:
                if hasattr(el, "render_expression"):
                    # Пробуем получить значение через пины/выражения, иначе рендерим напрямую
                    val = el.render_expression("output", context)
                    if not val:
                        val = el.render_expression("list", context)
                    rendered_elms.append(val if val else el.render(context))
                else:
                    rendered_elms.append(el.render(context))
            return f"[{', '.join(rendered_elms)}]"
        else:
            val0 = self.get_input_value("item0", context)
            val1 = self.get_input_value("item1", context)
            val2 = self.get_input_value("item2", context)
            return f"[{val0}, {val1}, {val2}]"

    def render(self, context: RenderContext) -> str:
        return self.render_expression("list", context)
```

### `nodes/expressions/literal_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class LiteralNode(ExpressionNode):
    NODE_TYPE = "literal"
    DISPLAY_NAME = "Literal"

    def __init__(self, value):
        self.value = value

    def render(self, indent=0, context=None):
        return repr(self.value)
```

### `nodes/expressions/variable_node.py`

```python
from registry.node_registry import register_node

from nodes.base.expression_node import ExpressionNode


@register_node
class VariableNode(ExpressionNode):
    NODE_TYPE = "variable"
    DISPLAY_NAME = "Variable"

    def __init__(self, name):
        self.name = name

    def render(self, indent=0, context=None):
        return self.name
```

### `nodes/flow/if_node.py`

```python
from registry.node_registry import register_node

from nodes.base.flow_node import FlowNode


@register_node
class IfNode(FlowNode):
    NODE_TYPE = "if"
    DISPLAY_NAME = "If"

    def __init__(
        self,
        condition,
        true_node=None,
        false_node=None,
        next_node=None,
    ):
        super().__init__(next_node)

        self.condition = condition
        self.true_node = true_node
        self.false_node = false_node

    def render(self, indent=0, context=None):
        ind = "    " * indent

        condition_code = self.condition.render(
            context=context,
        )

        if self.true_node:
            true_code = self.true_node.render(
                indent + 1,
                context,
            )
        else:
            true_code = (
                "    " * (indent + 1)
                + "pass\n"
            )

        code = (
            f"{ind}if {condition_code}:\n"
            f"{true_code}"
        )

        if self.false_node:
            false_code = self.false_node.render(
                indent + 1,
                context,
            )

            code += (
                f"{ind}else:\n"
                f"{false_code}"
            )

        code += self.render_next(
            indent,
            context,
        )

        return code
```

### `nodes/flow/while_node.py`

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

### `nodes/imports/from_import_node.py`

```python
from registry.node_registry import register_node

from core.base_node import BaseNode


@register_node
class FromImportNode(BaseNode):
    NODE_TYPE = "from_import"
    DISPLAY_NAME = "From Import"

    def __init__(
        self,
        module,
        names,
    ):
        self.module = module
        self.names = names

    def render(self, indent=0, context=None):
        names_code = ", ".join(self.names)

        code = (
            f"from {self.module} "
            f"import {names_code}"
        )

        if context:
            context.imports.add(code)

        return ""
```

### `nodes/imports/import_node.py`

```python
from registry.node_registry import register_node

from core.base_node import BaseNode


@register_node
class ImportNode(BaseNode):
    NODE_TYPE = "import"
    DISPLAY_NAME = "Import"

    def __init__(
        self,
        module,
        alias=None,
    ):
        self.module = module
        self.alias = alias

    def render(self, indent=0, context=None):
        if self.alias:
            code = (
                f"import {self.module} "
                f"as {self.alias}"
            )
        else:
            code = f"import {self.module}"

        if context:
            context.imports.add(code)

        return ""
```

### `nodes/statements/assign_node.py`

```python
from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class AssignNode(StatementNode):
    NODE_TYPE = "assign"
    DISPLAY_NAME = "Assign"

    def __init__(
        self,
        target,
        value,
        next_node=None,
    ):
        super().__init__(next_node)

        self.target = target
        self.value = value

    def render(self, indent=0, context=None):
        ind = "    " * indent

        target_code = self.target.render(
            context=context,
        )

        value_code = self.value.render(
            context=context,
        )

        code = (
            f"{ind}{target_code} = {value_code}\n"
        )

        return code + self.render_next(
            indent,
            context,
        )
```

### `nodes/statements/expression_statement_node.py`

```python
from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class ExpressionStatementNode(StatementNode):
    NODE_TYPE = "expression_statement"
    DISPLAY_NAME = "Expression Statement"

    def __init__(
        self,
        expression,
        next_node=None,
    ):
        super().__init__(next_node)

        self.expression = expression

    def render(self, indent=0, context=None):
        ind = "    " * indent

        expression_code = self.expression.render(
            context=context,
        )

        code = f"{ind}{expression_code}\n"

        return code + self.render_next(
            indent,
            context,
        )
```

### `nodes/statements/import_statement_node.py`

```python
from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class ImportStatementNode(StatementNode):
    NODE_TYPE = "import_statement"
    DISPLAY_NAME = "Import Statement"

    def __init__(
        self,
        import_node,
        next_node=None,
    ):
        super().__init__(next_node)

        self.import_node = import_node

    def render(self, indent=0, context=None):
        self.import_node.render(
            context=context,
        )

        return self.render_next(
            indent,
            context,
        )
```

### `nodes/statements/pass_node.py`

```python
from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class PassNode(StatementNode):
    NODE_TYPE = "pass"
    DISPLAY_NAME = "Pass"

    def render(self, indent=0, context=None):
        ind = "    " * indent

        code = f"{ind}pass\n"

        return code + self.render_next(
            indent,
            context,
        )
```

### `nodes/statements/return_node.py`

```python
from registry.node_registry import register_node

from nodes.base.statement_node import StatementNode


@register_node
class ReturnNode(StatementNode):
    NODE_TYPE = "return"
    DISPLAY_NAME = "Return"

    def __init__(
        self,
        value=None,
    ):
        super().__init__(None)

        self.value = value

    def render(self, indent=0, context=None):
        ind = "    " * indent

        if self.value:
            value_code = self.value.render(
                context=context,
            )

            return f"{ind}return {value_code}\n"

        return f"{ind}return\n"
```

### `nodes/structures/class_node.py`

```python
from registry.node_registry import register_node

from core.context import RenderContext
from core.base_node import BaseNode


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

        self.body_nodes = body_nodes or []

        self.bases = bases or []
        self.decorators = decorators or []

    def render(self, indent=0, context=None):
        context = context or RenderContext()

        ind = "    " * indent

        child_context = context.child(
            inside_class=True,
        )

        code = ""

        for decorator in self.decorators:
            code += (
                f"{ind}@{decorator.render(context=context)}\n"
            )

        bases_code = ""

        if self.bases:
            bases_code = (
                "("
                + ", ".join(self.bases)
                + ")"
            )

        code += (
            f"{ind}class {self.name}"
            f"{bases_code}:\n"
        )

        if not self.body_nodes:
            code += (
                "    " * (indent + 1)
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
```

### `nodes/structures/function_node.py`

```python
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
```

### `nodes/structures/module_node.py`

```python
from registry.node_registry import register_node

from core.context import RenderContext
from core.base_node import BaseNode


@register_node
class ModuleNode(BaseNode):
    NODE_TYPE = "module"
    DISPLAY_NAME = "Module"

    def __init__(self, body_nodes=None):
        self.body_nodes = body_nodes or []

    def render(self, indent=0, context=None):
        context = context or RenderContext()

        code_blocks = []

        for node in self.body_nodes:
            rendered = node.render(
                indent=0,
                context=context,
            )

            if rendered.strip():
                code_blocks.append(rendered)

        imports_code = ""

        if context.imports:
            imports_code = (
                "\n".join(sorted(context.imports))
                + "\n\n"
            )

        return (
            imports_code
            + "\n\n".join(code_blocks)
        )
```

### `plugins/example_plugin.py`

```python
from registry.node_registry import (
    register_node,
)

from nodes.base.expression_node import (
    ExpressionNode,
)


@register_node
class RandomValueNode(ExpressionNode):
    NODE_TYPE = "random_value"

    DISPLAY_NAME = "Random Value"

    def render(
        self,
        indent=0,
        context=None,
    ):
        return "random.random()"
```

### `registry/node_factory.py`

```python
from registry.node_registry import NODE_REGISTRY


class NodeFactory:
    @staticmethod
    def create(node_type: str, **kwargs):
        if node_type not in NODE_REGISTRY:
            raise ValueError(
                f"Unknown node type: {node_type}"
            )

        cls = NODE_REGISTRY[node_type]

        return cls(**kwargs)
```

### `registry/node_registry.py`

```python
NODE_REGISTRY = {}


def register_node(node_class):
    NODE_REGISTRY[node_class.NODE_TYPE] = node_class

    return node_class
```

### `registry/plugin_manager.py`

```python
import importlib.util
from pathlib import Path


class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(
        self,
        plugins_directory="plugins",
    ):
        path = Path(plugins_directory)

        if not path.exists():
            return

        for file in path.glob("*.py"):
            self.load_plugin(file)

    def load_plugin(self, file_path):
        module_name = file_path.stem

        spec = importlib.util.spec_from_file_location(
            module_name,
            file_path,
        )

        if not spec:
            return

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        self.plugins.append(module)
```

### `serializer/graph_loader.py`

```python
class GraphLoader:
    @staticmethod
    def load(main_window, data):
        main_window.clear_graph()

        created_nodes = {}

        for node_data in data["nodes"]:
            node = main_window.create_node(
                node_type=node_data["node_type"],
                x=node_data["x"],
                y=node_data["y"],
                properties=node_data.get(
                    "properties",
                    {},
                ),
            )

            created_nodes[
                node_data["id"]
            ] = node

        for connection_data in data["connections"]:
            from_node = created_nodes[
                connection_data["from_node"]
            ]

            to_node = created_nodes[
                connection_data["to_node"]
            ]

            output_pin = None
            input_pin = None

            for pin in from_node.outputs:
                if (
                    pin.name
                    == connection_data["from_pin"]
                ):
                    output_pin = pin
                    break

            for pin in to_node.inputs:
                if (
                    pin.name
                    == connection_data["to_pin"]
                ):
                    input_pin = pin
                    break

            if output_pin and input_pin:
                main_window.create_connection_between_pins(
                    output_pin,
                    input_pin,
                )

        main_window.compile_graph()
```

### `serializer/graph_serializer.py`

```python
import json


class GraphSerializer:
    @staticmethod
    def serialize(scene):
        nodes_data = []
        connections_data = []

        node_id_map = {}

        for index, item in enumerate(scene.items()):
            if not hasattr(item, "node_type"):
                continue

            node_id = str(index)

            node_id_map[item] = node_id

            nodes_data.append(
                {
                    "id": node_id,
                    "node_type": item.node_type,
                    "x": item.pos().x(),
                    "y": item.pos().y(),
                    "properties": item.properties,
                }
            )

        added_connections = set()

        for item in scene.items():
            if not hasattr(item, "connections"):
                continue

            for connection in item.connections:
                if connection in added_connections:
                    continue

                added_connections.add(connection)

                start_node = connection.start_pin.parentItem()
                end_node = connection.end_pin.parentItem()

                connections_data.append(
                    {
                        "from_node": node_id_map[start_node],
                        "from_pin": connection.start_pin.name,
                        "to_node": node_id_map[end_node],
                        "to_pin": connection.end_pin.name,
                    }
                )

        return {
            "nodes": nodes_data,
            "connections": connections_data,
        }

    @staticmethod
    def save_to_file(scene, path):
        data = GraphSerializer.serialize(scene)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
            )

    @staticmethod
    def load_from_file(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
```

### `ui/app/app.py`

```python
import sys

from PySide6.QtWidgets import QApplication

from ui.app.main_window import MainWindow


GLOBAL_STYLE = """
QMainWindow {
    background-color: #1e1f22;
}

QDockWidget {
    color: #e5e7eb;
    font-size: 12px;
}

QWidget {
    background-color: #25262b;
    color: #e5e7eb;
}

QListWidget {
    border: none;
    background-color: #1f2023;
}

QPlainTextEdit {
    background-color: #111214;
    border: 1px solid #3b3d44;
    font-family: Consolas;
    font-size: 14px;
}
"""


def run_app():
    app = QApplication(sys.argv)

    app.setStyleSheet(GLOBAL_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
```

### `ui/app/main_window.py`

```python
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QFileDialog,
    QMessageBox,
)

from PySide6.QtGui import QAction

from PySide6.QtCore import Qt

from ui.editor.graph_scene import GraphScene
from ui.editor.graph_view import GraphView
from ui.editor.node_item import NodeItem
from ui.editor.connection_item import ConnectionItem

from ui.widgets.node_palette import NodePalette
from ui.widgets.inspector_panel import InspectorPanel
from ui.widgets.code_preview import CodePreview

from ui.node_metadata import NODE_METADATA

from ui.runtime.runtime_graph import RuntimeGraph

from compiler.graph_compiler import GraphCompiler

from serializer.graph_serializer import (
    GraphSerializer,
)

from serializer.graph_loader import GraphLoader

from registry.plugin_manager import (
    PluginManager,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Python Blueprint System"
        )

        self.resize(1800, 1000)

        self.scene = GraphScene()
        self.scene.main_window = self

        self.view = GraphView(self.scene)

        self.runtime_graph = RuntimeGraph()

        self.setCentralWidget(self.view)

        self.setup_menu()
        self.setup_docks()

        self.plugin_manager = PluginManager()

        self.plugin_manager.load_plugins()

        self.create_demo_graph()

        self.compile_graph()

    def setup_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        new_action = QAction(
            "New Project",
            self,
        )

        save_action = QAction(
            "Save Project",
            self,
        )

        load_action = QAction(
            "Load Project",
            self,
        )

        undo_action = QAction(
            "Undo",
            self,
        )

        redo_action = QAction(
            "Redo",
            self,
        )

        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Y")

        undo_action.triggered.connect(
            self.scene.history.undo
        )

        redo_action.triggered.connect(
            self.scene.history.redo
        )

        file_menu.addSeparator()

        file_menu.addAction(undo_action)
        file_menu.addAction(redo_action)

        new_action.triggered.connect(
            self.new_project
        )

        save_action.triggered.connect(
            self.save_project
        )

        load_action.triggered.connect(
            self.load_project
        )

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

    def setup_docks(self):
        self.palette = NodePalette()

        self.palette.list_widget.itemDoubleClicked.connect(
            self.create_node_from_palette
        )

        palette_dock = QDockWidget("Palette")
        palette_dock.setWidget(self.palette)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            palette_dock,
        )

        self.inspector = InspectorPanel()

        inspector_dock = QDockWidget("Inspector")
        inspector_dock.setWidget(self.inspector)

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            inspector_dock,
        )

        self.preview = CodePreview()

        preview_dock = QDockWidget("Code Preview")
        preview_dock.setWidget(self.preview)

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            preview_dock,
        )

    def create_node_from_palette(self):
        node_type = (
            self.palette.get_selected_node_type()
        )

        if not node_type:
            return

        center = self.view.mapToScene(
            self.view.viewport().rect().center()
        )

        self.create_node(
            node_type,
            center.x(),
            center.y(),
        )

    def create_node(
        self,
        node_type,
        x,
        y,
        properties=None,
    ):
        metadata = NODE_METADATA[node_type]

        node = NodeItem(
            node_type,
            metadata["title"],
            metadata["inputs"],
            metadata["outputs"],
        )

        node.properties = properties or {}

        node.setPos(x, y)

        self.scene.addItem(node)

        self.runtime_graph.create_node_from_item(node)

        runtime_node = node.runtime_node

        for index, pin in enumerate(node.inputs):
            pin.runtime_pin = runtime_node.input_pins[index]

        for index, pin in enumerate(node.outputs):
            pin.runtime_pin = runtime_node.output_pins[index]

        return node

    def create_connection_between_pins(
        self,
        pin_a,
        pin_b,
    ):
        if pin_a.is_input:
            input_pin = pin_a
            output_pin = pin_b
        else:
            input_pin = pin_b
            output_pin = pin_a

        connection = ConnectionItem(
            output_pin,
            input_pin,
        )

        output_pin.connections.append(connection)
        input_pin.connections.append(connection)

        self.scene.addItem(connection)

        self.runtime_graph.create_connection(
            output_pin,
            input_pin,
        )

        self.compile_graph()

    def clear_graph(self):
        self.scene.clear()

        self.runtime_graph = RuntimeGraph()

    def new_project(self):
        self.clear_graph()

        self.compile_graph()

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "Template Graph (*.tgraph)",
        )

        if not path:
            return

        GraphSerializer.save_to_file(
            self.scene,
            path,
        )

        QMessageBox.information(
            self,
            "Saved",
            "Project saved successfully",
        )

    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Project",
            "",
            "Template Graph (*.tgraph)",
        )

        if not path:
            return

        data = GraphSerializer.load_from_file(
            path
        )

        GraphLoader.load(
            self,
            data,
        )

    def create_demo_graph(self):
        start_node = self.create_node(
            "start",
            0,
            0,
        )

        print_node = self.create_node(
            "print",
            450,
            100,
            {
                "value": "Hello Runtime Graph",
            },
        )

        self.create_connection_between_pins(
            start_node.outputs[0],
            print_node.inputs[0],
        )

    def compile_graph(self):
        compiler = GraphCompiler(
            self.runtime_graph.graph,
        )

        code = compiler.compile()

        self.preview.set_code(code)

    def auto_layout_graph(self):
        self.runtime_graph.auto_layout()

        for item in self.scene.items():
            if not hasattr(item, "runtime_node"):
                continue

            x, y = item.runtime_node.position

            item.setPos(x, y)
```

### `ui/editor/clipboard.py`

```python
import copy


class GraphClipboard:
    def __init__(self):
        self.data = None

    def copy(self, nodes):
        serialized = []

        for node in nodes:
            serialized.append(
                {
                    "node_type": node.node_type,
                    "x": node.pos().x(),
                    "y": node.pos().y(),
                    "properties": copy.deepcopy(
                        node.properties
                    ),
                }
            )

        self.data = serialized

    def paste(self, main_window, offset=40):
        if not self.data:
            return

        created = []

        for node_data in self.data:
            node = main_window.create_node(
                node_data["node_type"],
                node_data["x"] + offset,
                node_data["y"] + offset,
                node_data["properties"],
            )

            created.append(node)

        return created
```

### `ui/editor/commands.py`

```python
class Command:
    def undo(self):
        raise NotImplementedError

    def redo(self):
        raise NotImplementedError


class MoveNodesCommand(Command):
    def __init__(self, nodes, old_positions, new_positions):
        self.nodes = nodes

        self.old_positions = old_positions
        self.new_positions = new_positions

    def undo(self):
        for node in self.nodes:
            pos = self.old_positions[node]

            node.setPos(pos)

    def redo(self):
        for node in self.nodes:
            pos = self.new_positions[node]

            node.setPos(pos)


class CreateNodeCommand(Command):
    def __init__(self, scene, node):
        self.scene = scene
        self.node = node

    def undo(self):
        self.scene.remove_node(self.node)

    def redo(self):
        self.scene.addItem(self.node)


class DeleteNodesCommand(Command):
    def __init__(self, scene, nodes):
        self.scene = scene
        self.nodes = nodes

    def undo(self):
        for node in self.nodes:
            self.scene.addItem(node)

    def redo(self):
        for node in self.nodes:
            self.scene.remove_node(node)
```

### `ui/editor/connection_item.py`

```python
from PySide6.QtWidgets import QGraphicsPathItem

from PySide6.QtGui import (
    QPainterPath,
    QPen,
    QColor,
)

from PySide6.QtCore import (
    QPointF,
    Qt,
)

from ui.styling.colors import CONNECTION_COLOR


class ConnectionItem(QGraphicsPathItem):
    def __init__(
        self,
        start_pin,
        end_pin=None,
        parent=None,
    ):
        super().__init__(parent)

        self.start_pin = start_pin
        self.end_pin = end_pin

        self.temp_end_pos = QPointF()

        self.setZValue(-1)

        self.update_path()

    def set_end_pos(self, pos):
        self.temp_end_pos = pos
        self.update_path()

    def update_path(self):
        start = self.start_pin.scenePos()

        if self.end_pin:
            end = self.end_pin.scenePos()
        else:
            end = self.temp_end_pos

        path = QPainterPath()

        path.moveTo(start)

        dx = abs(end.x() - start.x()) * 0.5

        ctrl1 = QPointF(
            start.x() + dx,
            start.y(),
        )

        ctrl2 = QPointF(
            end.x() - dx,
            end.y(),
        )

        path.cubicTo(
            ctrl1,
            ctrl2,
            end,
        )

        self.setPath(path)

        pen = QPen(
            QColor(CONNECTION_COLOR),
            4,
        )

        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        if self.end_pin:
            from core.type_validation import (
                TypeValidationEngine,
            )

            validator = TypeValidationEngine()

            source = (
                self.start_pin.runtime_pin
                .effective_type
            )

            target = (
                self.end_pin.runtime_pin
                .effective_type
            )

            if validator.can_auto_cast(
                source,
                target,
            ):
                pen.setStyle(Qt.DashLine)

        self.setPen(pen)

    def remove_from_pins(self):
        if not self.end_pin:
            return

        if self in self.start_pin.connections:
            self.start_pin.connections.remove(self)

        if self in self.end_pin.connections:
            self.end_pin.connections.remove(self)

    def destroy(self):
        self.remove_from_pins()

        scene = self.scene()

        if scene:
            scene.removeItem(self)

    def cleanup(self):
        self.hide()

        scene = self.scene()

        if scene:
            scene.removeItem(self)
```

### `ui/editor/graph_scene.py`

```python
from PySide6.QtWidgets import (
    QGraphicsScene,
    QMenu,
)

from PySide6.QtGui import (
    QColor,
    QPen,
    QAction,
)

from PySide6.QtCore import Qt

from ui.styling.colors import (
    BACKGROUND_COLOR,
    GRID_COLOR,
)

from ui.styling.metrics import GRID_SIZE

from ui.editor.connection_item import (
    ConnectionItem,
)

from ui.editor.history import HistoryManager

from ui.editor.clipboard import (
    GraphClipboard,
)

from ui.editor.node_search_popup import (
    NodeSearchPopup,
)


class GraphScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.setSceneRect(
            -10000,
            -10000,
            20000,
            20000,
        )

        self.drag_connection = None
        self.drag_start_pin = None

        self.main_window = None

        self.history = HistoryManager()

        self.clipboard = GraphClipboard()

    def begin_connection_drag(self, pin):
        self.drag_start_pin = pin

        self.drag_connection = ConnectionItem(
            pin,
            None,
        )

        self.addItem(self.drag_connection)

    def mouseMoveEvent(self, event):
        if self.drag_connection:
            self.drag_connection.set_end_pos(
                event.scenePos()
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drag_connection:
            items = self.items(event.scenePos())

            target_pin = None

            for item in items:
                if hasattr(item, "pin_type"):
                    target_pin = item
                    break

            if self.is_valid_connection(
                self.drag_start_pin,
                target_pin,
            ):
                self.main_window.create_connection_between_pins(
                    self.drag_start_pin,
                    target_pin,
                )

            self.removeItem(
                self.drag_connection
            )

            self.drag_connection = None
            self.drag_start_pin = None

        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()

        create_action = QAction(
            "Create Node",
            menu,
        )

        duplicate_action = QAction(
            "Duplicate",
            menu,
        )

        delete_action = QAction(
            "Delete",
            menu,
        )

        menu.addAction(create_action)
        menu.addAction(duplicate_action)
        menu.addAction(delete_action)

        create_action.triggered.connect(
            lambda: self.open_search_popup(
                event.scenePos()
            )
        )

        duplicate_action.triggered.connect(
            self.duplicate_selection
        )

        delete_action.triggered.connect(
            self.delete_selection
        )

        menu.exec(event.screenPos())

    def open_search_popup(self, pos):
        popup = NodeSearchPopup()

        if popup.exec():
            if popup.selected_node:
                self.main_window.create_node(
                    popup.selected_node,
                    pos.x(),
                    pos.y(),
                )

    def duplicate_selection(self):
        nodes = [
            item
            for item in self.selectedItems()
            if hasattr(item, "node_type")
        ]

        self.clipboard.copy(nodes)

        self.clipboard.paste(
            self.main_window
        )

    def delete_selection(self):
        for item in self.selectedItems():
            self.remove_node(item)

    def is_valid_connection(
        self,
        start_pin,
        end_pin,
    ):
        if not end_pin:
            return False

        if start_pin == end_pin:
            return False

        if start_pin.is_input == end_pin.is_input:
            return False

        from core.types import (
            is_type_compatible,
        )

        if start_pin.is_input:
            source = end_pin
            target = start_pin
        else:
            source = start_pin
            target = end_pin

        return is_type_compatible(
            source.pin_type,
            target.pin_type,
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selection()

        if (
            event.modifiers()
            & Qt.ControlModifier
        ):
            if event.key() == Qt.Key_C:
                self.copy_selection()

            elif event.key() == Qt.Key_V:
                self.paste_selection()

            elif event.key() == Qt.Key_Z:
                self.history.undo()

            elif event.key() == Qt.Key_Y:
                self.history.redo()

            elif event.key() == Qt.Key_D:
                self.duplicate_selection()

        if event.key() == Qt.Key_Tab:
            view = self.views()[0]

            center = view.mapToScene(
                view.viewport().rect().center()
            )

            self.open_search_popup(center)

        super().keyPressEvent(event)

    def copy_selection(self):
        nodes = [
            item
            for item in self.selectedItems()
            if hasattr(item, "node_type")
        ]

        self.clipboard.copy(nodes)

    def paste_selection(self):
        self.clipboard.paste(
            self.main_window
        )

    def remove_node(self, node):
        if not hasattr(node, "inputs"):
            return

        all_pins = (
            node.inputs + node.outputs
        )

        runtime_node = node.runtime_node

        for pin in all_pins:
            for connection in pin.connections.copy():
                connection.remove_from_pins()

                if (
                    connection
                    in self.main_window.runtime_graph.graph.connections
                ):
                    self.main_window.runtime_graph.graph.connections.remove(
                        connection
                    )

                self.removeItem(connection)

        if (
            runtime_node
            in self.main_window.runtime_graph.graph.nodes
        ):
            self.main_window.runtime_graph.graph.nodes.remove(
                runtime_node
            )

        self.removeItem(node)

        self.main_window.compile_graph()

    def drawBackground(
        self,
        painter,
        rect,
    ):
        painter.fillRect(
            rect,
            QColor(BACKGROUND_COLOR),
        )

        pen = QPen(QColor(GRID_COLOR))
        pen.setWidth(1)

        painter.setPen(pen)

        left = int(rect.left()) - (
            int(rect.left()) % GRID_SIZE
        )

        top = int(rect.top()) - (
            int(rect.top()) % GRID_SIZE
        )

        x = left

        while x < rect.right():
            painter.drawLine(
                x,
                rect.top(),
                x,
                rect.bottom(),
            )

            x += GRID_SIZE

        y = top

        while y < rect.bottom():
            painter.drawLine(
                rect.left(),
                y,
                rect.right(),
                y,
            )

            y += GRID_SIZE
```

### `ui/editor/graph_view.py`

```python
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt


class GraphView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

        self.zoom = 1.0

        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        self.setViewportUpdateMode(
            QGraphicsView.SmartViewportUpdate
        )

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setDragMode(
            QGraphicsView.RubberBandDrag
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setStyleSheet(
            "border: none;"
        )

        self.panning = False
        self.last_pos = None

    def wheelEvent(self, event):
        factor = 1.15

        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
            self.zoom *= factor
        else:
            self.scale(1 / factor, 1 / factor)
            self.zoom /= factor

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = True
            self.last_pos = event.pos()

            self.setCursor(Qt.ClosedHandCursor)

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            delta = event.pos() - self.last_pos
            self.last_pos = event.pos()

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)

            event.accept()
            return

        super().mouseReleaseEvent(event)
```

### `ui/editor/history.py`

```python
class HistoryManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def push(self, command):
        self.undo_stack.append(command)

        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return

        command = self.undo_stack.pop()

        command.undo()

        self.redo_stack.append(command)

    def redo(self):
        if not self.redo_stack:
            return

        command = self.redo_stack.pop()

        command.redo()

        self.undo_stack.append(command)
```

### `ui/editor/node_item.py`

```python
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import (
    QColor,
    QBrush,
    QPen,
    QLinearGradient,
    QPainterPath,
    QFont,
)

from PySide6.QtCore import QRectF, Qt

from ui.editor.pin_item import PinItem

from ui.styling.colors import (
    NODE_BODY_COLOR,
    NODE_HEADER_START,
    NODE_HEADER_END,
    NODE_BORDER_COLOR,
    NODE_SELECTED_BORDER,
    TEXT_COLOR,
)

from ui.styling.metrics import (
    NODE_WIDTH,
    NODE_HEADER_HEIGHT,
    NODE_RADIUS,
    PIN_SPACING,
)


class NodeItem(QGraphicsItem):
    def __init__(
        self,
        node_type,
        title,
        inputs,
        outputs,
    ):
        super().__init__()

        self.node_type = node_type

        self.title = title

        self.inputs = []
        self.outputs = []

        self.properties = {}

        self.runtime_node = None

        self.width = NODE_WIDTH

        pin_count = max(
            len(inputs),
            len(outputs),
        )

        self.height = (
            NODE_HEADER_HEIGHT
            + 24
            + pin_count * PIN_SPACING
        )

        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.create_pins(inputs, outputs)

        self.setup_shadow()

    def setup_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))

        self.setGraphicsEffect(shadow)

    def create_pins(self, inputs, outputs):
        start_y = NODE_HEADER_HEIGHT + 24

        for index, pin_data in enumerate(inputs):
            pin = PinItem(
                pin_data["name"],
                pin_data["type"],
                True,
                self,
            )

            pin.setPos(
                0,
                start_y + index * PIN_SPACING,
            )

            self.inputs.append(pin)

        for index, pin_data in enumerate(outputs):
            pin = PinItem(
                pin_data["name"],
                pin_data["type"],
                False,
                self,
            )

            pin.setPos(
                self.width,
                start_y + index * PIN_SPACING,
            )

            self.outputs.append(pin)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height,
        )

    def paint(self, painter, option, widget):
        rect = self.boundingRect()

        path = QPainterPath()
        path.addRoundedRect(
            rect,
            NODE_RADIUS,
            NODE_RADIUS,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(NODE_BODY_COLOR))
        painter.drawPath(path)

        header_rect = QRectF(
            0,
            0,
            self.width,
            NODE_HEADER_HEIGHT,
        )

        gradient = QLinearGradient(
            0,
            0,
            0,
            NODE_HEADER_HEIGHT,
        )

        gradient.setColorAt(
            0,
            QColor(NODE_HEADER_START),
        )

        gradient.setColorAt(
            1,
            QColor(NODE_HEADER_END),
        )

        header_path = QPainterPath()

        header_path.addRoundedRect(
            header_rect,
            NODE_RADIUS,
            NODE_RADIUS,
        )

        painter.setBrush(QBrush(gradient))
        painter.drawPath(header_path)

        border_color = (
            NODE_SELECTED_BORDER
            if self.isSelected()
            else NODE_BORDER_COLOR
        )

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(border_color), 2))

        painter.drawPath(path)

        painter.setPen(QColor(TEXT_COLOR))

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            QRectF(
                16,
                0,
                self.width - 32,
                NODE_HEADER_HEIGHT,
            ),
            Qt.AlignVCenter,
            self.title,
        )

        if self.outputs:
            output_pin = self.outputs[0]

            if hasattr(output_pin, "runtime_pin"):
                type_text = (
                    output_pin.runtime_pin.type_name
                )

                painter.setPen(
                    QColor("#9ca3af")
                )

                small_font = QFont()

                small_font.setPointSize(8)

                painter.setFont(small_font)

                painter.drawText(
                    12,
                    NODE_HEADER_HEIGHT - 10,
                    type_text,
                )

                painter.setFont(font)

        self.draw_pin_labels(painter)

        self.draw_pin_labels(painter)

    def draw_pin_labels(self, painter):
        font = QFont()
        font.setPointSize(9)

        painter.setFont(font)
        painter.setPen(QColor(TEXT_COLOR))

        for pin in self.inputs:
            painter.drawText(
                16,
                pin.y() + 5,
                pin.name,
            )

        for pin in self.outputs:
            text_width = painter.fontMetrics().horizontalAdvance(
                pin.name
            )

            painter.drawText(
                self.width - text_width - 16,
                pin.y() + 5,
                pin.name,
            )
            
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        grid_size = 32

        x = round(self.x() / grid_size) * grid_size
        y = round(self.y() / grid_size) * grid_size

        self.setPos(x, y)

        scene = self.scene()

        if (
            scene
            and scene.main_window
        ):
            scene.main_window.compile_graph()

            scene.main_window.inspector.set_node(
                self
            )
```

### `ui/editor/node_search_popup.py`

```python
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
)

from ui.node_metadata import NODE_METADATA


class NodeSearchPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Node")

        self.resize(350, 500)

        self.selected_node = None

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search node..."
        )

        self.list_widget = QListWidget()

        layout.addWidget(self.search)
        layout.addWidget(self.list_widget)

        self.populate()

        self.search.textChanged.connect(
            self.filter_nodes
        )

        self.list_widget.itemDoubleClicked.connect(
            self.accept_selection
        )

    def populate(self):
        self.list_widget.clear()

        for node_type, metadata in NODE_METADATA.items():
            self.list_widget.addItem(
                f"{metadata['title']} ({node_type})"
            )

    def filter_nodes(self, text):
        self.list_widget.clear()

        text = text.lower()

        for node_type, metadata in NODE_METADATA.items():
            title = metadata["title"]

            combined = (
                title + " " + node_type
            ).lower()

            if text in combined:
                self.list_widget.addItem(
                    f"{title} ({node_type})"
                )

    def accept_selection(self):
        text = self.list_widget.currentItem().text()

        node_type = (
            text.split("(")[-1]
            .replace(")", "")
        )

        self.selected_node = node_type

        self.accept()
```

### `ui/editor/pin_item.py`

```python
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor, QBrush, QPen, QPolygonF
from PySide6.QtCore import QRectF, QPointF

from ui.styling.colors import (
    EXECUTION_COLOR,
    FLOAT_COLOR,
    BOOL_COLOR,
    STRING_COLOR,
    OBJECT_COLOR,
)

from ui.styling.metrics import PIN_RADIUS

from ui.styling.type_colors import (
    TYPE_COLORS,
)


PIN_COLORS = {
    "execution": EXECUTION_COLOR,
    "float": FLOAT_COLOR,
    "bool": BOOL_COLOR,
    "string": STRING_COLOR,
    "object": OBJECT_COLOR,
}


class PinItem(QGraphicsItem):
    def __init__(
        self,
        name,
        pin_type,
        is_input,
        parent=None,
    ):
        super().__init__(parent)

        self.name = name
        self.pin_type = pin_type
        self.is_input = is_input

        self.radius = PIN_RADIUS

        self.runtime_pin = None

        self.connections = []

        self.setAcceptHoverEvents(True)

        self.setFlag(
            QGraphicsItem.ItemSendsScenePositionChanges
        )

    def boundingRect(self):
        return QRectF(
            -10,
            -10,
            20,
            20,
        )

    def get_color(self):
        return QColor(
            self.get_type_color()
        )

    def paint(self, painter, option, widget):
        color = self.get_color()

        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color))

        if self.pin_type == "execution":
            polygon = QPolygonF(
                [
                    QPointF(-6, -6),
                    QPointF(6, 0),
                    QPointF(-6, 6),
                ]
            )

            painter.drawPolygon(polygon)
        else:
            painter.drawEllipse(
                -self.radius,
                -self.radius,
                self.radius * 2,
                self.radius * 2,
            )

    def itemChange(self, change, value):
        if (
            change
            == QGraphicsItem.ItemScenePositionHasChanged
        ):
            for connection in self.connections:
                connection.update_path()

        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        scene = self.scene()

        if hasattr(scene, "begin_connection_drag"):
            scene.begin_connection_drag(self)

        event.accept()

    def get_type_color(self):
        type_name = (
            self.runtime_pin.effective_type.name
        )

        return TYPE_COLORS.get(
            type_name,
            "#9ca3af",
        )
```

### `ui/editor/reroute_node_item.py`

```python
from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QColor, QBrush, QPen

from ui.styling.colors import (
    CONNECTION_COLOR,
)


class RerouteNodeItem(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__(-8, -8, 16, 16)

        self.setBrush(
            QBrush(QColor(CONNECTION_COLOR))
        )

        self.setPen(
            QPen(QColor("#ffffff"), 2)
        )

        self.setFlags(
            self.ItemIsMovable
            | self.ItemIsSelectable
        )
```

### `ui/node_metadata.py`

```python
from core.type_system import (
    ANY_TYPE,
    EXEC_TYPE,
    FLOAT_TYPE,
    STRING_TYPE,
    BOOL_TYPE,
    LIST_TYPE,
    DICT_TYPE,
    OPTIONAL_TYPE,
)

NODE_METADATA = {
    "entry": {
        "title": "Start",
        "inputs": [],
        "outputs": [("next", EXEC_TYPE)]
    },
    "print": {
        "title": "Print",
        "inputs": [("exec_in", EXEC_TYPE), ("value", ANY_TYPE)],
        "outputs": [("exec_out", EXEC_TYPE)]
    },
    "if": {
        "title": "If Branch",
        "inputs": [("exec_in", EXEC_TYPE), ("condition", BOOL_TYPE)],
        "outputs": [("true", EXEC_TYPE), ("false", EXEC_TYPE)]
    },
    "binary_op": {
        "title": "Binary Op",
        "inputs": [("a", FLOAT_TYPE), ("b", FLOAT_TYPE)],
        "outputs": [("output", FLOAT_TYPE)]
    },
    "string_concat": {
        "title": "Concat Strings",
        "inputs": [("a", STRING_TYPE), ("b", STRING_TYPE)],
        "outputs": [("output", STRING_TYPE)]
    },
    "while": {
        "title": "While Loop",
        "inputs": [("exec_in", EXEC_TYPE), ("condition", BOOL_TYPE)],
        "outputs": [("body", EXEC_TYPE), ("completed", EXEC_TYPE)]
    },
    "create_list": {
        "title": "Create List",
        "inputs": [("item0", ANY_TYPE), ("item1", ANY_TYPE)],
        "outputs": [("list", LIST_TYPE(ANY_TYPE))]
    },
    "create_dict": {
        "title": "Create Dict",
        "inputs": [("key", STRING_TYPE), ("value", ANY_TYPE)],
        "outputs": [("dict", DICT_TYPE(STRING_TYPE, ANY_TYPE))]
    },
    "optional_handler": {
        "title": "Optional Handler",
        "inputs": [("data", OPTIONAL_TYPE(STRING_TYPE))],
        "outputs": [("result", STRING_TYPE)]
    }
}
```

### `ui/runtime/runtime_graph.py`

```python
from graph.graph import Graph
from graph.graph_node import GraphNode
from graph.connection import Connection
from graph.auto_layout import GraphAutoLayout

from graph.execution_pin import ExecutionPin
from graph.data_pin import DataPin

from ui.node_metadata import NODE_METADATA


class RuntimeGraph:
    def __init__(self):
        self.graph = Graph()

    def create_node_from_item(self, node_item):
        metadata = NODE_METADATA[node_item.node_type]

        graph_node = GraphNode(
            node_id=id(node_item),
            node_type=node_item.node_type,
            title=metadata["title"],
            position=(
                node_item.pos().x(),
                node_item.pos().y(),
            ),
            properties=node_item.properties.copy(),
        )

        for pin_data in metadata["inputs"]:
            pin = self.create_pin(pin_data, True)
            graph_node.add_input_pin(pin)

        for pin_data in metadata["outputs"]:
            pin = self.create_pin(pin_data, False)
            graph_node.add_output_pin(pin)

        node_item.runtime_node = graph_node

        self.graph.add_node(graph_node)

    def create_pin(self, pin_data, is_input):
        pin_type = pin_data["type"]

        if pin_type == "execution":
            return ExecutionPin(
                pin_data["name"],
                is_input,
            )

        return DataPin(
            pin_data["name"],
            pin_type,
            is_input,
        )

    def create_connection(
        self,
        output_pin_item,
        input_pin_item,
    ):
        output_runtime_pin = output_pin_item.runtime_pin
        input_runtime_pin = input_pin_item.runtime_pin

        connection = Connection(
            output_runtime_pin,
            input_runtime_pin,
        )

        self.graph.add_connection(connection)

        self.graph.propagate_types()

        self.scene().update()

    def get_input_value(
        self,
        node,
        pin_name,
    ):
        pin = node.get_input_pin(pin_name)

        if not pin:
            return None

        if not pin.connections:
            return None

        return pin.connections[0]

    def clear(self):
        self.graph.nodes.clear()
        self.graph.connections.clear()

    def auto_layout(self):
        layout = GraphAutoLayout(
            self.graph
        )

        layout.apply()
```

### `ui/styling/colors.py`

```python
BACKGROUND_COLOR = "#1e1f22"
GRID_COLOR = "#2b2d31"
NODE_BODY_COLOR = "#25262b"
NODE_HEADER_START = "#3a3d46"
NODE_HEADER_END = "#2f3138"
NODE_BORDER_COLOR = "#4b5263"
NODE_SELECTED_BORDER = "#00d0ff"

TEXT_COLOR = "#e5e7eb"
SUBTEXT_COLOR = "#9ca3af"

EXECUTION_COLOR = "#ffffff"
FLOAT_COLOR = "#00d0ff"
BOOL_COLOR = "#ffcc00"
STRING_COLOR = "#c084fc"
OBJECT_COLOR = "#4ade80"

CONNECTION_COLOR = "#00d0ff"
```

### `ui/styling/metrics.py`

```python
NODE_WIDTH = 260
NODE_HEADER_HEIGHT = 42
NODE_RADIUS = 14
PIN_RADIUS = 6
GRID_SIZE = 32
NODE_PADDING = 12
PIN_SPACING = 28
```

### `ui/styling/type_colors.py`

```python
TYPE_COLORS = {
    "int": "#60a5fa",
    "float": "#c084fc",
    "str": "#34d399",
    "bool": "#fbbf24",
    "list": "#fb7185",
    "dict": "#f97316",
    "execution": "#ffffff",
    "any": "#9ca3af",
}
```

### `ui/widgets/code_preview.py`

```python
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
)


class CodePreview(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Generated Python")

        self.editor = QPlainTextEdit()

        self.editor.setReadOnly(True)

        layout.addWidget(title)
        layout.addWidget(self.editor)

    def set_code(self, code):
        self.editor.setPlainText(code)
```

### `ui/widgets/inspector_panel.py`

```python
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)

from PySide6.QtCore import Qt


class InspectorPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.current_node = None

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Inspector")

        self.layout.addWidget(self.title)

        self.layout.setAlignment(
            Qt.AlignTop
        )

    def set_node(self, node):
        self.current_node = node

        while self.layout.count() > 1:
            item = self.layout.takeAt(1)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not node:
            return

        defaults = self.build_default_properties(
            node
        )

        for key, value in defaults.items():
            if key not in node.properties:
                node.properties[key] = value

        for key, value in node.properties.items():
            label = QLabel(key)

            field = QLineEdit(str(value))

            field.textChanged.connect(
                lambda text, k=key: self.update_property(
                    k,
                    text,
                )
            )

            self.layout.addWidget(label)
            self.layout.addWidget(field)

    def build_default_properties(self, node):
        defaults = {}

        if node.node_type == "literal":
            defaults["value"] = "123"

        elif node.node_type == "variable":
            defaults["name"] = "my_var"

        elif node.node_type == "assign":
            defaults["variable"] = "my_var"

        elif node.node_type == "print":
            defaults["value"] = "Hello World"

        return defaults

    def update_property(self, key, value):
        if not self.current_node:
            return

        self.current_node.properties[key] = value

        window = self.window()

        if hasattr(window, "compile_graph"):
            window.compile_graph()
```

### `ui/widgets/node_palette.py`

```python
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
)

from ui.node_metadata import NODE_METADATA


class NodePalette(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Node Palette")

        self.list_widget = QListWidget()

        self.node_types = []

        for node_type, metadata in NODE_METADATA.items():
            self.list_widget.addItem(
                metadata["title"]
            )

            self.node_types.append(node_type)

        layout.addWidget(title)
        layout.addWidget(self.list_widget)

    def get_selected_node_type(self):
        row = self.list_widget.currentRow()

        if row < 0:
            return None

        return self.node_types[row]
```

### `ui/widgets/type_hint_widget.py`

```python
from PySide6.QtWidgets import QLabel


class TypeHintWidget(QLabel):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            """
            QLabel {
                background: #111827;
                color: #e5e7eb;
                border: 1px solid #374151;
                padding: 4px 8px;
                border-radius: 6px;
            }
            """
        )
```

