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