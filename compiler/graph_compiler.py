from core.generator import PythonGenerator
from core.exceptions import GraphCompilationError

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

        self.validator = GraphValidator()

        self.tracer = ExecutionTracer()

        self.expression_cache = {}

        self.node_compilers = {
            "print": self.compile_print_node,
            "branch": self.compile_branch_node,
            "while": self.compile_while_node,
            "assign": self.compile_assign_node,
            "return": self.compile_return_node,
        }

    def compile(self) -> str:
        self.graph.propagate_types()
        errors = self.validator.validate(self.graph)
        if errors:
            raise GraphCompilationError(f"Validation failed with {len(errors)} errors")

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