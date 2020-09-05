# Author: Olivier Lécluse
# License GPL-3
# Using Simple PyQT serial terminal v0.09 from iosoft.blog
#
# Serial Terminal frame
#

from PySide2.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QApplication
from PySide2.QtCore import Qt, Signal, Slot, QSize
from PySide2.QtGui import QFont, QTextCursor, QPainter, QPixmap

from src.assets_manager import get_font

import sys

WIN_WIDTH, WIN_HEIGHT = 760, 510    # Window size
RETURN_CHAR = "\x0D"                  # Char to be sent when Enter key pressed
PASTE_CHAR  = "\x16"                # Ctrl code for clipboard paste


# Custom text box, catching keystrokes
class MyTextBox(QTextEdit):
    def __init__(self, *args): 
        QTextEdit.__init__(self, *args)
         
    def keyPressEvent(self, event):     # Send keypress to parent's handler
        self.parent().keypress_handler(event)


# Main widget            
class SerialTerminalFrame(QWidget):
    text_update = Signal(str)

    # --- Init methods ---

    def __init__(self, config):
        """
        Serial Terminal frame

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.setMinimumSize(QSize(WIN_WIDTH, WIN_HEIGHT))
        self.setMaximumSize(QSize(int(WIN_WIDTH*1.3), int(WIN_HEIGHT*1.5)))

        self.setWindowTitle("DigiQt - Serial terminal")

        self.textbox = MyTextBox()              # Create custom text box
        font = QFont()
        font.setFamily(get_font(config))           # Monospaced font
        font.setPointSize(11)
        self.textbox.setFont(font)
        layout = QVBoxLayout()
        layout.setMargin(60)
        layout.addWidget(self.textbox)
        self.setLayout(layout)
        self.text_update.connect(self.append_text)      # Connect text update to handler
        
        self.serth = None                       # Terminal thread created by serial controler
        self.sig_terminal_open = None           # Signal pushed by serial controler

    def write(self, text):                      # Handle sys.stdout.write: update display
        self.text_update.emit(text)             # Send signal to synchronise call with main thread

    def flush(self):                            # Handle sys.stdout.flush: do nothing
        pass

    @Slot(str)
    def append_text(self, text):                # Text display update handler
        cur = self.textbox.textCursor()
        cur.movePosition(QTextCursor.End) # Move cursor to end of text
        s = str(text)
        while s:
            head, sep, s = s.partition("\n")      # Split line at LF
            cur.insertText(head)                # Insert text at cursor
        self.textbox.setTextCursor(cur)         # Update visible cursor
 
    def keypress_handler(self, event):          # Handle keypress from text box
        k = event.key()
        s = RETURN_CHAR if k == Qt.Key_Return else event.text()
        if len(s) > 0 and s[0] == PASTE_CHAR:       # Detect ctrl-V paste
            cb = QApplication.clipboard() 
            self.serth.ser_out(cb.text())       # Send paste string to serial driver
        else:
            self.serth.ser_out(s)               # ..or send keystroke

    def paintEvent(self, event):
        """
        Override to draw the terminal console frame background image
        """
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap("assets/retroterm.png").scaled(self.size()))

        super().paintEvent(event)
