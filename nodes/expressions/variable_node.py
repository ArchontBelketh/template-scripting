from nodes.base.expression_node import ExpressionNode
from graph.data_pin import DataPin
from core.context import RenderContext
from core.type_system import ANY_TYPE


class VariableNode(ExpressionNode):
    def __init__(self, node_id: str = None, properties: dict = None):
        # ИСПРАВЛЕНО: если вызвано как VariableNode("x") из скрипта,
        # перенаправляем строку в имя переменной, генерируя ID автоматически
        if node_id is not None and properties is None:
            properties = {"name": str(node_id)}
            node_id = None

        super().__init__(node_id, "variable", "Variable", properties)
        self.add_output_pin(DataPin("value", "output", ANY_TYPE))
        
        if "name" not in self.properties:
            self.properties["name"] = "my_var"

    def render(self, context: RenderContext) -> str:
        return self.properties.get("name", "my_var")