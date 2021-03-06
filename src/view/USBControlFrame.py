# Author: Thomas Lécluse
# License GPL-3

#
# USB controlframe
#

from PySide2.QtWidgets import QToolBar, QGridLayout, QWidget, QLabel, QPlainTextEdit, QFileDialog
from PySide2.QtCore import QSize
from PySide2.QtGui import QTextCursor

from src.view.style import style
from src.view.console_frame_widgets.ConsoleFrameButtons import ToDigiruleButton, FromDigiruleButton, RefreshPortButton, FirmwareUpdate
from src.view.console_frame_widgets.USBPortDropdown import UsbPortCombo

class ConsoleOutput(QPlainTextEdit):
    def __init__(self, *args): 
        QPlainTextEdit.__init__(self, *args)
        self.setReadOnly(True)

    def write(self, text):
        cur = self.textCursor()
        cur.movePosition(QTextCursor.End) # Move cursor to end of text
        s = str(text)
        while s:
            head, sep, s = s.partition("\n")      # Split line at LF
            cur.insertText(head)                # Insert text at cursor                # Insert text at cursor
            if sep:                             # New line if LF
                cur.insertBlock()
        self.setTextCursor(cur)         # Update visible cursor

class USBFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        USB control frame

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.setFixedSize(QSize(600, 200))

        self.config = config
        self.setWindowTitle("DigiQt - USB Control")

        self.sig_button_pressed = None  # signal configured by serialControler
        self.sig_firmware_update = None # 

        # Firmware update output
        self.out = ConsoleOutput()
        # Buttons
        self.to_dr_btn = ToDigiruleButton(config)
        self.to_dr_btn.to_digirule = lambda: self.sig_button_pressed.emit(0)

        self.from_dr_btn = FromDigiruleButton(config)
        self.from_dr_btn.from_digirule = lambda: self.sig_button_pressed.emit(1)

        # Firmware
        self.firmware_btn = FirmwareUpdate(config)
        self.firmware_btn.firmware_update = self.firmware_update
        # Port selection
        self.lab_port = QLabel("Port:")
        self.usb_combo = UsbPortCombo()
        self.refresh_btn = RefreshPortButton(config)
        self.refresh_btn.on_refresh = lambda: self.sig_button_pressed.emit(2)

        self._init_tool_bar()
        self._set_layout()
        self._set_stylesheet()

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.toolbar.addWidget(self.to_dr_btn)
        self.toolbar.addWidget(self.from_dr_btn)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.firmware_btn)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.lab_port)
        self.toolbar.addWidget(self.usb_combo)
        self.toolbar.addWidget(self.refresh_btn)

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QGridLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.toolbar, 0, 0)
        box.addWidget(self.out, 1, 0)

        self.setLayout(box)

    def _set_stylesheet(self):
        self.toolbar.setStyleSheet(style.get_stylesheet("qtoolbar"))
        self.setStyleSheet(style.get_stylesheet("common"))
        self.lab_port.setStyleSheet("background-color: transparent; color: #75BA6D; font-weight: bold;")
        self.out.setStyleSheet("background-color: #505050; color: white;")

    def firmware_update(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Choose a digirule Firmware")
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("HEX files (*.hex)")
        if dlg.exec_():
            file_path = dlg.selectedFiles()[0]
            # Call the controller method for update
            self.sig_firmware_update.emit(file_path)

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
