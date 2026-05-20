from nodes.base.expression_node import ExpressionNode
from graph.data_pin import DataPin
from core.context import RenderContext
from core.type_system import ANY_TYPE


class LiteralNode(ExpressionNode):
    def __init__(self, node_id = None, properties: dict = None):
        # ИСПРАВЛЕНО: если вызвано как LiteralNode(val) из скрипта,
        # сохраняем значение в свойства, убирая конфликт с node_id
        if node_id is not None and properties is None:
            properties = {"value": str(node_id)}
            node_id = None

        super().__init__(node_id, "literal", "Literal", properties)
        self.add_output_pin(DataPin("value", "output", ANY_TYPE))
        
        if "value" not in self.properties:
            self.properties["value"] = "0"

    def render(self, context: RenderContext) -> str:
        val = self.properties.get("value", "0")
        if isinstance(val, str):
            if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                return val
            try:
                int(val)
                return val
            except ValueError:
                try:
                    float(val)
                    return val
                except ValueError:
                    return f"'{val}'"
        return str(val)