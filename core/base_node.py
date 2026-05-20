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
        """Для выражений: рендерит код конкретного пина-выхода.
        Если специфичный метод не переопределен поднодой, сбрасываемся на стандартный render.
        """
        return self.render(context)