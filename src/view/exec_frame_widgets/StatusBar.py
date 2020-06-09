# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QLabel, QFrame, QProgressBar, QVBoxLayout
from PySide2.QtCore import Slot, Signal

from threading import Thread
from time import sleep


class StatusBar(QFrame):

    sig_progress_bar = Signal(int)  # progress value update
    sig_persistent_message = Signal(str)  # new statusbar persistent message signal
    sig_temp_message = Signal(str)  # new statusbar temporary message signal

    def __init__(self, width, height):
        """
        Custom widget for the execution frame's status bar

        :param width: to use as width for this label
        :type width: int
        :param height: to use as height for this label
        :type height: int
        """
        QFrame.__init__(self)

        self.setFixedSize(width, height)

        self.label = QLabel()
        self.progressbar = QProgressBar()

        self.label.setFixedSize(width, height - 5)
        self.progressbar.setFixedSize(width, 5)
        self.progressbar.setRange(0, 100)
        self.progressbar.setValue(100)
        self.progressbar.setTextVisible(False)
        self._set_style_sheet()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label)
        layout.addWidget(self.progressbar)

        self.setLayout(layout)

        self.sig_progress_bar.connect(self.__set_progress_val)
        self.sig_persistent_message.connect(self.__set_status_message)
        self.sig_temp_message.connect(self.__display_for_4_sec)

        self.last_thread = 0

    @Slot(str)
    def __display_for_4_sec(self, text):
        """
        Displays the given text for 10 seconds

        :param text: text to display
        :type text: str
        """
        self.last_thread += 1
        Thread(target=self.__clear_after, args=(4, text, self.last_thread)).start()

    @Slot(int)
    def __set_progress_val(self, val):
        """
        Sets the current val (between 0 and 100) into the progress bar
        :type val: int
        """
        self.progressbar.setValue(val)

    @Slot(int)
    def __set_status_message(self, message):
        """
        Displays a message that does not disappear
        """
        self.label.setText(message)

    def __clear_after(self, time, text, thread_index):
        """
        Performs an automatic clear of this status bar after the given time

        :param time: seconds
        :type time: int
        :param text: message to display
        :param thread_index: id of the thread that is running this
        """
        self.sig_persistent_message.emit(text)

        self.sig_progress_bar.emit(100)

        for i in range(100):
            # Stop condition
            if thread_index != self.last_thread:
                return

            self.sig_progress_bar.emit(100 - i)

            sleep(time / 100)

        self.sig_progress_bar.emit(0)
        self.sig_persistent_message.emit("")
        self.sig_progress_bar.emit(100)

        self.last_thread = 0  # Once we've reached the end, we may reset that value

    def _set_style_sheet(self):
        """
        Sets the default style sheet
        """
        self.label.setStyleSheet("padding-left: 1em; background-color: #585858; color: cyan;")
        self.progressbar.setStyleSheet("QProgressBar::chunk {background-color: #585858}")
