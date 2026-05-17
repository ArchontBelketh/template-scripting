from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor, QBrush, QPen, QPolygonF
from PySide6.QtCore import QRectF, QPointF, Qt

from ui.styling.colors import (
    EXECUTION_COLOR,
    FLOAT_COLOR,
    BOOL_COLOR,
    STRING_COLOR,
    OBJECT_COLOR,
)

from ui.styling.metrics import PIN_RADIUS


PIN_COLORS = {
    "execution": EXECUTION_COLOR,
    "float": FLOAT_COLOR,
    "bool": BOOL_COLOR,
    "string": STRING_COLOR,
    "object": OBJECT_COLOR,
}


class PinItem(QGraphicsItem):
    def __init__(
        self,
        name,
        pin_type,
        is_input,
        parent=None,
    ):
        super().__init__(parent)

        self.name = name
        self.pin_type = pin_type
        self.is_input = is_input

        self.radius = PIN_RADIUS

        self.runtime_pin = None

        self.connections = []

        self.setAcceptHoverEvents(True)

        self.setFlag(
            QGraphicsItem.ItemSendsScenePositionChanges
        )

    def boundingRect(self):
        return QRectF(
            -10,
            -10,
            20,
            20,
        )

    def get_color(self):
        return QColor(
            PIN_COLORS.get(
                self.pin_type,
                OBJECT_COLOR,
            )
        )

    def paint(self, painter, option, widget):
        color = self.get_color()

        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color))

        if self.pin_type == "execution":
            polygon = QPolygonF(
                [
                    QPointF(-6, -6),
                    QPointF(6, 0),
                    QPointF(-6, 6),
                ]
            )

            painter.drawPolygon(polygon)
        else:
            painter.drawEllipse(
                -self.radius,
                -self.radius,
                self.radius * 2,
                self.radius * 2,
            )

    def itemChange(self, change, value):
        if (
            change
            == QGraphicsItem.ItemScenePositionHasChanged
        ):
            for connection in self.connections:
                connection.update_path()

        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        scene = self.scene()

        if hasattr(scene, "begin_connection_drag"):
            scene.begin_connection_drag(self)

        event.accept()