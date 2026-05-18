from PySide6.QtWidgets import QGraphicsPathItem

from PySide6.QtGui import (
    QPainterPath,
    QPen,
    QColor,
)

from PySide6.QtCore import (
    QPointF,
    Qt,
)

from ui.styling.colors import CONNECTION_COLOR


class ConnectionItem(QGraphicsPathItem):
    def __init__(
        self,
        start_pin,
        end_pin=None,
        parent=None,
    ):
        super().__init__(parent)

        self.start_pin = start_pin
        self.end_pin = end_pin

        self.temp_end_pos = QPointF()

        self.setZValue(-1)

        self.update_path()

    def set_end_pos(self, pos):
        self.temp_end_pos = pos
        self.update_path()

    def update_path(self):
        start = self.start_pin.scenePos()

        if self.end_pin:
            end = self.end_pin.scenePos()
        else:
            end = self.temp_end_pos

        path = QPainterPath()

        path.moveTo(start)

        dx = abs(end.x() - start.x()) * 0.5

        ctrl1 = QPointF(
            start.x() + dx,
            start.y(),
        )

        ctrl2 = QPointF(
            end.x() - dx,
            end.y(),
        )

        path.cubicTo(
            ctrl1,
            ctrl2,
            end,
        )

        self.setPath(path)

        pen = QPen(
            QColor(CONNECTION_COLOR),
            4,
        )

        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        self.setPen(pen)

    def remove_from_pins(self):
        if not self.end_pin:
            return

        if self in self.start_pin.connections:
            self.start_pin.connections.remove(self)

        if self in self.end_pin.connections:
            self.end_pin.connections.remove(self)

    def destroy(self):
        self.remove_from_pins()

        scene = self.scene()

        if scene:
            scene.removeItem(self)

    def cleanup(self):
        self.hide()

        scene = self.scene()

        if scene:
            scene.removeItem(self)