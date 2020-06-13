# Author: Thomas Lécluse
# Licence GPL-3

#
# Serial console frame
#

from PySide2.QtWidgets import QToolBar, QGridLayout, QWidget, QLabel, QPlainTextEdit, QSizePolicy
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QKeySequence, QFont, QTextCursor

from src.view.style import style


class SerialConsoleFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        Serial Console frame

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.setFixedSize(QSize(600, 170))

        self.config = config
        self.setWindowTitle("DigiQt - Serial console")

        self.serial_out = QPlainTextEdit()
        self.serial_out.setReadOnly(True)
        self.serial_out.setFixedSize(QSize(600, 100))

        self.serial_in = QLabel()
        self.serial_in.setAlignment(Qt.AlignCenter)
        self.serial_in.setFixedSize(QSize(50, 30))

        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.serial_in.setFont(font)

        self._init_tool_bar()
        self._set_layout()
        self._set_stylesheet()

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        # Empty space to align the about button to the right
        spacer = QWidget()
        spacer.setStyleSheet("background-color: transparent;")
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        self.toolbar.addWidget(self.serial_in)

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QGridLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.toolbar, 0, 0)

        box.addWidget(self.serial_out, 1, 0)

        self.setLayout(box)

    def _set_stylesheet(self):
        self.toolbar.setStyleSheet(style.get_stylesheet("qtoolbar"))
        self.setStyleSheet(style.get_stylesheet("common"))
        self.serial_in.setStyleSheet("background-color: #565656; color: cyan; margin-right: 20px")
        self.serial_out.setStyleSheet("background-color: #505050; color: white; padding-left: 10px;")

    def keyPressEvent(self, event):
        self.set_serial_in(QKeySequence(event.key()).toString())  # TODO signal keyseq to controller for process
        self.append_serial_out(QKeySequence(event.key()).toString())

    def set_serial_in(self, val):
        """
        Sets the serial in value
        """
        self.serial_in.setText(val)

    def append_serial_out(self, text):
        """
        Appends the given text inside the serial out area
        """
        # First, we place the cursor at the end (this will also clear the selection before inserting new text)
        cursor = self.serial_out.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.serial_out.setTextCursor(cursor)

        self.serial_out.insertPlainText(text)

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click.
        """
        self.on_close()

    def on_close(self):
        """
        Reroute this method in the Main Frame in order to Updates the execution frame's open editor icon and tooltip
        """
        pass
