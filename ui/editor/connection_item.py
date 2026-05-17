from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPen, QColor
from PySide6.QtCore import QPointF

from ui.styling.colors import CONNECTION_COLOR


class ConnectionItem(QGraphicsPathItem):
    def __init__(
        self,
        start_pin,
        end_pin,
        parent=None,
    ):
        super().__init__(parent)

        self.start_pin = start_pin
        self.end_pin = end_pin

        self.setZValue(-1)

        self.update_path()

    def update_path(self):
        start = self.start_pin.scenePos()
        end = self.end_pin.scenePos()

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

        pen = QPen(QColor(CONNECTION_COLOR), 4)
        pen.setCapStyle(pen.RoundCap)

        self.setPen(pen)