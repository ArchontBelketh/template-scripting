from ui.app.app import run_app
from core.generator import PythonGenerator

from nodes.structures.module_node import ModuleNode
from nodes.structures.class_node import ClassNode
from nodes.structures.function_node import FunctionNode

from nodes.imports.import_node import ImportNode

from nodes.statements.expression_statement_node import (
    ExpressionStatementNode,
)

from nodes.statements.return_node import ReturnNode

from nodes.expressions.variable_node import VariableNode
from nodes.expressions.literal_node import LiteralNode
from nodes.expressions.call_node import CallNode
from nodes.expressions.attribute_node import (
    AttributeNode,
)
from nodes.expressions.await_node import AwaitNode
from nodes.expressions.list_comprehension_node import (
    ListComprehensionNode,
)
from nodes.expressions.binary_op_node import (
    BinaryOpNode,
)
from nodes.expressions.list_node import ListNode


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

comprehension = ListComprehensionNode(
    expression=BinaryOpNode(
        VariableNode("x"),
        "*",
        LiteralNode(2),
    ),
    variable_name="x",
    iterable=ListNode(
        [
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

generator = PythonGenerator()

print(
    generator.generate(module)
)

if __name__ == "__main__":
    run_app()