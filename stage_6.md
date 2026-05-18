# Этап 6 — Real Data Flow System

Ниже — готовый код для реализации этапа 6.
Заменяй файлы полностью.

---

# compiler/graph_compiler.py

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

---

# graph/graph.py

```python
class Graph:
    def __init__(self):
        self.nodes = []
        self.connections = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_connection(self, connection):
        self.connections.append(connection)

    def find_node_by_type(self, node_type):
        for node in self.nodes:
            if node.node_type == node_type:
                return node

        return None

    def find_node_by_id(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node

        return None
```

---

# graph/graph_node.py

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

---

# ui/node_metadata.py

```python
NODE_METADATA = {
    "start": {
        "title": "Start",
        "category": "Flow",
        "color": "#ffffff",
        "inputs": [],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "print": {
        "title": "Print",
        "category": "Statement",
        "color": "#5eead4",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "value",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "literal": {
        "title": "Literal",
        "category": "Expression",
        "color": "#c084fc",
        "inputs": [],
        "outputs": [
            {
                "name": "value",
                "type": "any",
            },
        ],
    },

    "variable": {
        "title": "Variable",
        "category": "Expression",
        "color": "#4ade80",
        "inputs": [],
        "outputs": [
            {
                "name": "value",
                "type": "any",
            },
        ],
    },

    "add": {
        "title": "Add",
        "category": "Math",
        "color": "#00d0ff",
        "inputs": [
            {
                "name": "left",
                "type": "any",
            },
            {
                "name": "right",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "result",
                "type": "any",
            },
        ],
    },

    "subtract": {
        "title": "Subtract",
        "category": "Math",
        "color": "#00d0ff",
        "inputs": [
            {
                "name": "left",
                "type": "any",
            },
            {
                "name": "right",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "result",
                "type": "any",
            },
        ],
    },

    "greater": {
        "title": "Greater",
        "category": "Logic",
        "color": "#ffcc00",
        "inputs": [
            {
                "name": "left",
                "type": "any",
            },
            {
                "name": "right",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "result",
                "type": "bool",
            },
        ],
    },

    "branch": {
        "title": "Branch",
        "category": "Flow",
        "color": "#ffffff",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "condition",
                "type": "bool",
            },
        ],
        "outputs": [
            {
                "name": "true",
                "type": "execution",
            },
            {
                "name": "false",
                "type": "execution",
            },
        ],
    },

    "while": {
        "title": "While",
        "category": "Flow",
        "color": "#ffffff",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "condition",
                "type": "bool",
            },
        ],
        "outputs": [
            {
                "name": "loop",
                "type": "execution",
            },
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "assign": {
        "title": "Assign",
        "category": "Statement",
        "color": "#4ade80",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "value",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "return": {
        "title": "Return",
        "category": "Statement",
        "color": "#ffcc00",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "value",
                "type": "any",
            },
        ],
        "outputs": [],
    },
}
```

---

# ui/widgets/inspector_panel.py

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

---

# ui/runtime/runtime_graph.py

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

---

# Что появится после этапа 6

Система теперь умеет:

- настоящий dataflow
- expression graph compilation
- nested expressions
- branching execution
- while loops
- recursive graph traversal
- compiler registry
- expression caching
- runtime graph API
- execution scopes
- multiple execution outputs

Теперь архитектура уже близка к Unreal Blueprint foundation.

