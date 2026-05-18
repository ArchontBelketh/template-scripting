from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt, QRectF

from ui.styling.colors import (
    BACKGROUND_COLOR,
    GRID_COLOR,
)

from ui.styling.metrics import GRID_SIZE

from ui.editor.connection_item import ConnectionItem
from ui.editor.pin_item import PinItem


class GraphScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.setSceneRect(
            -10000,
            -10000,
            20000,
            20000,
        )

        self.drag_connection = None
        self.drag_start_pin = None

        self.main_window = None

    def begin_connection_drag(self, pin):
        self.drag_start_pin = pin

        self.drag_connection = ConnectionItem(
            pin,
            None,
        )

        self.addItem(self.drag_connection)

    def mouseMoveEvent(self, event):
        if self.drag_connection:
            self.drag_connection.set_end_pos(
                event.scenePos()
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drag_connection:
            target_pin = self.find_pin_near_position(
                event.scenePos()
            )

            if self.is_valid_connection(
                self.drag_start_pin,
                target_pin,
            ):
                self.main_window.create_connection_between_pins(
                    self.drag_start_pin,
                    target_pin,
                )

            self.drag_connection.cleanup()

            self.drag_connection = None
            self.drag_start_pin = None

        super().mouseReleaseEvent(event)

    def find_pin_near_position(
        self,
        scene_pos,
        radius=24,
    ):
        rect = QRectF(
            scene_pos.x() - radius,
            scene_pos.y() - radius,
            radius * 2,
            radius * 2,
        )

        items = self.items(rect)

        nearest_pin = None
        nearest_distance = float("inf")

        for item in items:
            if not isinstance(item, PinItem):
                continue

            pin_pos = item.scenePos()

            dx = pin_pos.x() - scene_pos.x()
            dy = pin_pos.y() - scene_pos.y()

            distance = (dx * dx + dy * dy) ** 0.5

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_pin = item

        return nearest_pin

    def is_valid_connection(
        self,
        start_pin,
        end_pin,
    ):
        if not end_pin:
            return False

        if start_pin == end_pin:
            return False

        if start_pin.is_input == end_pin.is_input:
            return False

        from core.types import is_type_compatible

        if start_pin.is_input:
            source = end_pin
            target = start_pin
        else:
            source = start_pin
            target = end_pin

        if not is_type_compatible(
            source.pin_type,
            target.pin_type,
        ):
            return False

        return True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                self.remove_node(item)

        super().keyPressEvent(event)

    def remove_node(self, node):
        if not hasattr(node, "inputs"):
            return

        all_pins = node.inputs + node.outputs

        runtime_node = node.runtime_node

        for pin in all_pins:
            for connection in pin.connections.copy():
                connection.remove_from_pins()

                if (
                    connection
                    in self.main_window.runtime_graph.graph.connections
                ):
                    self.main_window.runtime_graph.graph.connections.remove(
                        connection
                    )

                self.removeItem(connection)

        if (
            runtime_node
            in self.main_window.runtime_graph.graph.nodes
        ):
            self.main_window.runtime_graph.graph.nodes.remove(
                runtime_node
            )

        self.removeItem(node)

        self.main_window.compile_graph()

    def drawBackground(self, painter, rect):
        painter.fillRect(
            rect,
            QColor(BACKGROUND_COLOR),
        )

        pen = QPen(QColor(GRID_COLOR))
        pen.setWidth(1)

        painter.setPen(pen)

        left = int(rect.left()) - (
            int(rect.left()) % GRID_SIZE
        )

        top = int(rect.top()) - (
            int(rect.top()) % GRID_SIZE
        )

        x = left

        while x < rect.right():
            painter.drawLine(
                x,
                rect.top(),
                x,
                rect.bottom(),
            )

            x += GRID_SIZE

        y = top

        while y < rect.bottom():
            painter.drawLine(
                rect.left(),
                y,
                rect.right(),
                y,
            )

            y += GRID_SIZE