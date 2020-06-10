# Author: Thomas Lécluse
# Licence GPL-3

#
# RAM frame
#

from PySide2.QtWidgets import QVBoxLayout, QWidget, QPlainTextEdit
from PySide2.QtCore import Qt, QSize

from src.view.style import style


class RAMFrame(QWidget):

    # --- Init methods ---

    def __init__(self):
        """
        Editor frame. Contains a toolbar and an editor widget
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - RAM")
        self.setMinimumSize(QSize(350, 650))

        self.editor = QPlainTextEdit()  # TODO temporary
        self.editor.setMinimumSize(QSize(350, 650))

        self._set_layout()
        self._set_stylesheet()

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.editor)
        box.setAlignment(self.editor, Qt.AlignTop)

        self.setLayout(box)

    def _connect_all(self):
        """
        Connects all the buttons to methods
        """

    def _set_stylesheet(self):
        self.editor.setStyleSheet("background-color: #505050; color: white")

        # Execution Frame
        self.setStyleSheet(style.get_stylesheet("common"))

    def set_ram_content(self, text):
        """
        Sets the content of the RAM text holder

        :param text: text to set
        """
        self.editor.setPlainText(text)

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click.
        """
        self.on_close()

    def on_close(self):
        """
        Reroot this method in the Main Frame in order to Updates the execution frame's open editor icon and tooltip
        :return:
        """
        pass
