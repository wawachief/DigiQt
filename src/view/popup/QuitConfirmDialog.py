from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PySide2.QtCore import Qt, QSize

from src.view.style import style


class DialogQuitConfirmation(QDialog):
    def __init__(self):
        """
        Displays a Dialog for the quit confirmation.
        """
        QDialog.__init__(self)

        self.setWindowTitle("Quit DigiQt?")
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setFixedSize(QSize(300, 130))

        self.ok_btn = QPushButton("Quit")
        self.ok_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        self.label = QLabel("Do you really want to quit DigiQt?")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.ok_btn, 1, 0)
        layout.addWidget(self.cancel_btn, 1, 1)

        self.setLayout(layout)
        self.setStyleSheet(style.get_stylesheet("dialog"))
