from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import (
    QColor,
    QBrush,
    QPen,
    QLinearGradient,
    QPainterPath,
    QFont,
)

from PySide6.QtCore import QRectF, Qt

from ui.editor.pin_item import PinItem

from ui.styling.colors import (
    NODE_BODY_COLOR,
    NODE_HEADER_START,
    NODE_HEADER_END,
    NODE_BORDER_COLOR,
    NODE_SELECTED_BORDER,
    TEXT_COLOR,
)

from ui.styling.metrics import (
    NODE_WIDTH,
    NODE_HEADER_HEIGHT,
    NODE_RADIUS,
    PIN_SPACING,
)


class NodeItem(QGraphicsItem):
    def __init__(
        self,
        node_type,
        title,
        inputs,
        outputs,
    ):
        super().__init__()

        self.node_type = node_type

        self.title = title

        self.inputs = []
        self.outputs = []

        self.properties = {}

        self.runtime_node = None

        self.width = NODE_WIDTH

        pin_count = max(
            len(inputs),
            len(outputs),
        )

        self.height = (
            NODE_HEADER_HEIGHT
            + 24
            + pin_count * PIN_SPACING
        )

        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.create_pins(inputs, outputs)

        self.setup_shadow()

    def setup_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))

        self.setGraphicsEffect(shadow)

    def create_pins(self, inputs, outputs):
        start_y = NODE_HEADER_HEIGHT + 24

        for index, pin_data in enumerate(inputs):
            pin = PinItem(
                pin_data["name"],
                pin_data["type"],
                True,
                self,
            )

            pin.setPos(
                0,
                start_y + index * PIN_SPACING,
            )

            self.inputs.append(pin)

        for index, pin_data in enumerate(outputs):
            pin = PinItem(
                pin_data["name"],
                pin_data["type"],
                False,
                self,
            )

            pin.setPos(
                self.width,
                start_y + index * PIN_SPACING,
            )

            self.outputs.append(pin)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height,
        )

    def paint(self, painter, option, widget):
        rect = self.boundingRect()

        path = QPainterPath()
        path.addRoundedRect(
            rect,
            NODE_RADIUS,
            NODE_RADIUS,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(NODE_BODY_COLOR))
        painter.drawPath(path)

        header_rect = QRectF(
            0,
            0,
            self.width,
            NODE_HEADER_HEIGHT,
        )

        gradient = QLinearGradient(
            0,
            0,
            0,
            NODE_HEADER_HEIGHT,
        )

        gradient.setColorAt(
            0,
            QColor(NODE_HEADER_START),
        )

        gradient.setColorAt(
            1,
            QColor(NODE_HEADER_END),
        )

        header_path = QPainterPath()

        header_path.addRoundedRect(
            header_rect,
            NODE_RADIUS,
            NODE_RADIUS,
        )

        painter.setBrush(QBrush(gradient))
        painter.drawPath(header_path)

        border_color = (
            NODE_SELECTED_BORDER
            if self.isSelected()
            else NODE_BORDER_COLOR
        )

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(border_color), 2))

        painter.drawPath(path)

        painter.setPen(QColor(TEXT_COLOR))

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            QRectF(
                16,
                0,
                self.width - 32,
                NODE_HEADER_HEIGHT,
            ),
            Qt.AlignVCenter,
            self.title,
        )

        self.draw_pin_labels(painter)

    def draw_pin_labels(self, painter):
        font = QFont()
        font.setPointSize(9)

        painter.setFont(font)
        painter.setPen(QColor(TEXT_COLOR))

        for pin in self.inputs:
            painter.drawText(
                16,
                pin.y() + 5,
                pin.name,
            )

        for pin in self.outputs:
            text_width = painter.fontMetrics().horizontalAdvance(
                pin.name
            )

            painter.drawText(
                self.width - text_width - 16,
                pin.y() + 5,
                pin.name,
            )