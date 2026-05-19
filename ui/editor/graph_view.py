from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt


class GraphView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

        self.zoom = 1.0

        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        self.setViewportUpdateMode(
            QGraphicsView.SmartViewportUpdate
        )

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setDragMode(
            QGraphicsView.RubberBandDrag
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setStyleSheet(
            "border: none;"
        )

        self.panning = False
        self.last_pos = None

    def wheelEvent(self, event):
        factor = 1.15

        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
            self.zoom *= factor
        else:
            self.scale(1 / factor, 1 / factor)
            self.zoom /= factor

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = True
            self.last_pos = event.pos()

            self.setCursor(Qt.ClosedHandCursor)

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            delta = event.pos() - self.last_pos
            self.last_pos = event.pos()

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)

            event.accept()
            return

        super().mouseReleaseEvent(event)