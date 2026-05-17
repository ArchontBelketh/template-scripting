from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
)


class CodePreview(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Generated Python")

        self.editor = QPlainTextEdit()

        self.editor.setPlainText(
            "# Generated code will appear here"
        )

        layout.addWidget(title)
        layout.addWidget(self.editor)