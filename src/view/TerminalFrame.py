# Author: Thomas Lécluse
# License GPL-3

#
# Serial console frame
#

from PySide2.QtWidgets import QToolBar, QGridLayout, QWidget, QLabel, QPlainTextEdit, QShortcut, QTabWidget
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QKeySequence, QFont, QTextCursor

from src.view.style import style
from src.view.SerialTerminalFrame import SerialTerminalFrame, WIN_HEIGHT, WIN_WIDTH
from src.view.console_frame_widgets.ConsoleFrameButtons import ClearButton
from src.assets_manager import get_font


class TerminalFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        Serial Console frame

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.config = config
        self.setWindowTitle("DigiQt - Terminal")

        self.sig_keyseq_pressed = None  # signal configured by serialControler
        self.sig_button_pressed = None  # signal configured by serialControler

        # Virtual Serial out
        self.serial_out = QPlainTextEdit()
        self.serial_out.setReadOnly(True)
        self.serial_out.setFixedSize(QSize(WIN_WIDTH, WIN_HEIGHT))

        doc = self.serial_out.document()
        f = doc.defaultFont()
        f.setFamily(get_font(config))
        doc.setDefaultFont(f)

        # Serial terminal (real)
        self.terminal = SerialTerminalFrame(self.config)

        # Tab
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.serial_out, "Virtual terminal")
        self.tab_widget.addTab(self.terminal, "Serial terminal")

        # Serial in
        self.serial_in = QLabel()
        self.serial_in.setAlignment(Qt.AlignCenter)
        self.serial_in.setFixedSize(QSize(44, 36))
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.serial_in.setFont(font)

        # Buttons
        self.clear_btn = ClearButton(config)
        self.clear_btn.on_clear = lambda: self.sig_button_pressed.emit(3)

        shortcut_space = QShortcut(QKeySequence(Qt.Key_Space), self)
        shortcut_space.activated.connect(lambda: self.__send_key(" "))

        self.tab_widget.currentChanged.connect(self.__on_tab_changed)

        self._init_tool_bar()
        self._set_layout()
        self._set_stylesheet()

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.toolbar.addWidget(self.clear_btn)
        self.toolbar.addWidget(self.serial_in)

    def __on_tab_changed(self):
        """
        Hides the serial in display when current widget is the real terminal
        """
        if self.tab_widget.currentWidget() == self.serial_out:
            self.serial_in.setStyleSheet(style.get_stylesheet("serial_in"))
        else:
            self.serial_in.setStyleSheet("background: #333333; color: #333333;")

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QGridLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.toolbar, 0, 0)

        box.addWidget(self.tab_widget, 1, 0)

        self.setLayout(box)

    def clear(self):
        """
        Clears the content of the current tab
        """
        if self.tab_widget.currentWidget() == self.serial_out:
            self.serial_out.setPlainText("")
            self.set_serial_in(" ")
        else:
            self.terminal.textbox.setPlainText("")
            self.terminal.textbox.setFocus()

    def _set_stylesheet(self):
        self.toolbar.setStyleSheet(style.get_stylesheet("qtoolbar"))
        self.setStyleSheet(style.get_stylesheet("common"))
        self.serial_in.setStyleSheet(style.get_stylesheet("serial_in"))
        self.serial_out.setStyleSheet("background-color: #505050; color: white; padding-left: 10px;")
        self.terminal.textbox.setStyleSheet("background-color: #111111; color: #44DD44;")
        self.tab_widget.setStyleSheet(style.get_stylesheet("tab"))

    def keyPressEvent(self, event):
        """
        Intercepts key press events
        """
        self.__send_key(event.text())

    def __send_key(self, key_typed):
        """
        Sends signal to serialControler
        :param key_type: key typed
        """
        if self.tab_widget.currentWidget() == self.serial_out:
            self.sig_keyseq_pressed.emit(key_typed)

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
        if text != chr(10):
            cursor = self.serial_out.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.serial_out.setTextCursor(cursor)
            self.serial_out.insertPlainText(text)
    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click.
        """
        self.terminal.sig_terminal_open.emit(False)  # ask Serial Controller to terminate the thread
        self.on_close()

    def on_close(self):
        """
        Reroute this method in the Main Frame in order to Updates the execution frame's open editor icon and tooltip
        """
        pass
