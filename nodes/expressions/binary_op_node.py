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