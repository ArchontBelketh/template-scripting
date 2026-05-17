from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class InspectorPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Inspector")

        layout.addWidget(title)