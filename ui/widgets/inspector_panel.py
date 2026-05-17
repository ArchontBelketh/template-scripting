from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)

from PySide6.QtCore import Qt


class InspectorPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.current_node = None

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Inspector")

        self.layout.addWidget(self.title)

        self.layout.setAlignment(
            Qt.AlignTop
        )

    def set_node(self, node):
        self.current_node = node

        while self.layout.count() > 1:
            item = self.layout.takeAt(1)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not node:
            return

        for key, value in node.properties.items():
            label = QLabel(key)

            field = QLineEdit(str(value))

            field.textChanged.connect(
                lambda text, k=key: self.update_property(
                    k,
                    text,
                )
            )

            self.layout.addWidget(label)
            self.layout.addWidget(field)

    def update_property(self, key, value):
        if not self.current_node:
            return

        self.current_node.properties[key] = value

        window = self.window()

        if hasattr(window, "compile_graph"):
            window.compile_graph()