# Author: Olivier Lécluse
# License GPL-3
# Using Simple PyQT serial terminal v0.09 from iosoft.blog
#
# Serial Terminal frame
#

from PySide2.QtWidgets import QVBoxLayout, QWidget, QTextEdit
from PySide2.QtCore import Qt, Signal, Slot, SIGNAL, QThread, QObject, QSize
from PySide2.QtGui import QFont, QTextCursor
from configparser import ConfigParser

from src.view.style import style
from src.assets_manager import get_font

import queue as Queue
import sys, time, serial
from time import sleep

WIN_WIDTH, WIN_HEIGHT = 684, 400    # Window size
SER_TIMEOUT = 0.1                   # Timeout for serial Rx
RETURN_CHAR = "\n"                 # Char to be sent when Enter key pressed
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

        self.setFixedSize(QSize(WIN_WIDTH, WIN_HEIGHT))

        self.setWindowTitle("DigiQt - Serial terminal")

        self.textbox = MyTextBox()              # Create custom text box
        font = QFont()
        font.setFamily("Courier New")           # Monospaced font
        font.setPointSize(10)
        self.textbox.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        self.setLayout(layout)
        self.text_update.connect(self.append_text)      # Connect text update to handler
        sys.stdout = self                               # Redirect sys.stdout to self

        self.serth = None
        
         
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
            head,sep,s = s.partition("\n")      # Split line at LF
            cur.insertText(head)                # Insert text at cursor
            if sep:                             # New line if LF
                cur.insertBlock()
        self.textbox.setTextCursor(cur)         # Update visible cursor
 
    def keypress_handler(self, event):          # Handle keypress from text box
        k = event.key()
        s = RETURN_CHAR if k==Qt.Key_Return else event.text()
        if len(s)>0 and s[0]==PASTE_CHAR:       # Detect ctrl-V paste
            cb = QApplication.clipboard() 
            self.serth.ser_out(cb.text())       # Send paste string to serial driver
        else:
            self.serth.ser_out(s)               # ..or send keystroke
     
    # --- Close handler ---
    def closeEvent(self, event):                # Window closing
        self.serth.running = False              # Wait until serial thread terminates
        sleep(0.1)
        print("Bye")
        self.on_close()


# Thread to handle incoming &amp; outgoing serial data
class SerialThread(QThread):
    def __init__(self, config): # Initialise with serial port details
        QThread.__init__(self)

        self.config = config
        self.dr_model = self.config.get("digirule", "dr_model")
        self.baudrate    = self.config.getint(self.dr_model, "baudrate")                 # Default baud rate
        self.portname    = self.config.get("serial", "port")                # Default port name
        
        self.txq = Queue.Queue()
        self.running = True
 
    def ser_out(self, s):                   # Write outgoing data to serial port if open
        if s != '\x0a':
            self.txq.put(s)                     # ..using a queue to sync with reader thread
         
    def ser_in(self, s):                    # Write incoming serial data to screen
        self.display(s)

    def bytes_str(self, d):
            return d if type(d) is str else "".join([chr(b) for b in d])

    def display(self, s):
        def textdump(data):
        # Return a string with high-bit chars replaced by hex values
            return "".join(["[%02X]" % ord(b) if b>'\x7e' else b for b in data])
        sys.stdout.write(textdump(str(s)))

    def run(self):                          # Run serial reader thread
        print(f"Opening {self.portname} at {self.baudrate} baud")
        try:
            self.ser = serial.Serial(self.portname, self.baudrate, timeout=SER_TIMEOUT)
            time.sleep(SER_TIMEOUT*1.2)
            self.ser.flushInput()
        except:
            self.ser = None
        if not self.ser:
            print("Can't open port")
            self.running = False
        while self.running:
            s = self.ser.read(self.ser.in_waiting or 1)
            if s:                                       # Get data from serial port
                self.ser_in(self.bytes_str(s))               # ..and convert to string
            if not self.txq.empty():
                txd = str(self.txq.get())               # If Tx data in queue, write to serial port
                self.ser.write(txd.encode('latin-1'))
        if self.ser:                                    # Close serial port when thread finished
            self.ser.close()
            self.ser = None
 