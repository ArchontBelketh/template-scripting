from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt

from ui.styling.colors import (
    BACKGROUND_COLOR,
    GRID_COLOR,
)

from ui.styling.metrics import GRID_SIZE

from ui.editor.connection_item import ConnectionItem


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
            items = self.items(event.scenePos())

            target_pin = None

            for item in items:
                if hasattr(item, "pin_type"):
                    target_pin = item
                    break

            if self.is_valid_connection(
                self.drag_start_pin,
                target_pin,
            ):
                self.main_window.create_connection_between_pins(
                    self.drag_start_pin,
                    target_pin,
                )

            self.removeItem(self.drag_connection)

            self.drag_connection = None
            self.drag_start_pin = None

        super().mouseReleaseEvent(event)

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

        if start_pin.pin_type != end_pin.pin_type:
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

        for pin in all_pins:
            for connection in pin.connections.copy():
                connection.remove_from_pins()

                self.removeItem(connection)

        self.removeItem(node)

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