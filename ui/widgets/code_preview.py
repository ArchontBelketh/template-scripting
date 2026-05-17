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

        self.editor.setReadOnly(True)

        layout.addWidget(title)
        layout.addWidget(self.editor)

    def set_code(self, code):
        self.editor.setPlainText(code)