from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QColor, QBrush, QPen

from ui.styling.colors import (
    CONNECTION_COLOR,
)


class RerouteNodeItem(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__(-8, -8, 16, 16)

        self.setBrush(
            QBrush(QColor(CONNECTION_COLOR))
        )

        self.setPen(
            QPen(QColor("#ffffff"), 2)
        )

        self.setFlags(
            self.ItemIsMovable
            | self.ItemIsSelectable
        )