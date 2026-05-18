from core.generator import PythonGenerator

from graph.validator import GraphValidator
from graph.tracer import ExecutionTracer

from nodes.structures.module_node import ModuleNode
from nodes.structures.function_node import FunctionNode

from nodes.statements.expression_statement_node import (
    ExpressionStatementNode,
)

from nodes.expressions.call_node import CallNode
from nodes.expressions.literal_node import LiteralNode
from nodes.expressions.variable_node import VariableNode


class GraphCompiler:
    def __init__(self, graph):
        self.graph = graph

        self.validator = GraphValidator(
            graph
        )

        self.tracer = ExecutionTracer()

    def compile(self):
        errors = self.validator.validate()

        if errors:
            return "\n".join(
                f"# ERROR: {error}"
                for error in errors
            )

        statements = []

        execution_nodes = (
            self.resolve_execution_chain()
        )

        for node in execution_nodes:
            self.tracer.trace_node(node)

            compiled = self.compile_node(node)

            if compiled:
                statements.append(compiled)

        chained = self.chain_statements(
            statements
        )

        main_function = FunctionNode(
            name="main",
            body_node=chained,
        )

        module = ModuleNode(
            body_nodes=[
                main_function,
            ]
        )

        generator = PythonGenerator()

        return generator.generate(module)

    def resolve_execution_chain(self):
        start_node = self.graph.find_node_by_type(
            "start"
        )

        if not start_node:
            return []

        result = []

        current = start_node

        visited = set()

        while current:
            if current.node_id in visited:
                break

            visited.add(current.node_id)

            result.append(current)

            current = self.find_next_execution_node(
                current
            )

        return result

    def find_next_execution_node(
        self,
        node,
    ):
        for pin in node.output_pins:
            if pin.type_name != "execution":
                continue

            if not pin.connections:
                continue

            connection = pin.connections[0]

            return connection.input_pin.owner

        return None

    def compile_node(self, graph_node):
        if graph_node.node_type == "start":
            return None

        if graph_node.node_type == "print":
            value = graph_node.properties.get(
                "value",
                "Hello World",
            )

            call = CallNode(
                func=VariableNode("print"),
                args=[
                    LiteralNode(value),
                ],
            )

            return ExpressionStatementNode(
                expression=call,
            )

        return None

    def chain_statements(
        self,
        statements,
    ):
        if not statements:
            return None

        for index in range(
            len(statements) - 1
        ):
            statements[index].next_node = (
                statements[index + 1]
            )

        return statements[0]