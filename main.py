from core.generator import PythonGenerator

from nodes.structures.module_node import ModuleNode
from nodes.structures.function_node import FunctionNode

from nodes.statements.expression_statement_node import (
    ExpressionStatementNode,
)

from nodes.expressions.variable_node import VariableNode
from nodes.expressions.literal_node import LiteralNode
from nodes.expressions.call_node import CallNode


print_call = CallNode(
    func=VariableNode("print"),
    args=[
        LiteralNode("Hello World"),
    ],
)

print_statement = ExpressionStatementNode(
    expression=print_call,
)

main_function = FunctionNode(
    name="main",
    body_node=print_statement,
)

module = ModuleNode(
    body_nodes=[
        main_function,
    ]
)

generator = PythonGenerator()

code = generator.generate(module)

print(code)