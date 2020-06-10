# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QLabel, QFrame, QProgressBar, QVBoxLayout
from PySide2.QtCore import Slot, Signal, QThread

from time import sleep

PROGRESS_BAR_MAX = 200


class StatusBar(QFrame):

    sig_progress_bar = Signal(int)  # progress value update
    sig_persistent_message = Signal(str)  # new statusbar persistent message signal
    sig_temp_message = Signal(str)  # new statusbar temporary message signal

    def __init__(self, width, height, config):
        """
        Custom widget for the execution frame's status bar

        :param width: to use as width for this label
        :type width: int
        :param height: to use as height for this label
        :type height: int
        :param config: configuration file
        """
        QFrame.__init__(self)

        self.setFixedSize(width, height)

        self.config = config

        self.label = QLabel()
        self.progressbar = QProgressBar()

        self.label.setFixedSize(width, height - 5)
        self.progressbar.setFixedSize(width, 5)
        self.progressbar.setRange(0, PROGRESS_BAR_MAX)
        self.progressbar.setValue(100)
        self.progressbar.setTextVisible(False)
        self._set_style_sheet()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label)
        layout.addWidget(self.progressbar)

        self.setLayout(layout)

        self.last_thread = 0

        self.sig_progress_bar.connect(self.__set_progress_val)
        self.sig_persistent_message.connect(self.__set_status_message)
        self.sig_temp_message.connect(self.__display_temporary_message)

    @Slot(str)
    def __display_temporary_message(self, text):
        """
        Displays the given text for a few seconds

        :param text: text to display
        :type text: str
        """
        self.last_thread += 1
        ProgressBarThread(self, self.sig_progress_bar, self.label, text, self.last_thread).start()

    def get_last_thread(self):
        """
        Method that retrieves the last thread, we should be the only one to run.
        """
        return self.last_thread

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
        self.last_thread = 0
        self.label.setText(message)

    def _set_style_sheet(self):
        """
        Sets the default style sheet
        """
        self.label.setStyleSheet("padding-left: 1em; background-color: " + self.config.get('colors', 'statusbar_bg') +
                                 "; color: " + self.config.get('colors', 'statusbar_text') + ";")
        self.progressbar.setStyleSheet("QProgressBar::chunk {background-color: "  + self.config.get('colors', 'progressbar_bg') + ";}")


class ProgressBarThread(QThread):

    def __init__(self, parent, sig_bar_update, label, text, thread_index):
        """
        Handles the process of the progress bar

        :param sig_bar_update: signal to emit to update the progress bar value
        :param label: label into which write the text
        :param thread_index: this thread's index
        :param parent: parent
        """
        QThread.__init__(self, parent)
        self.sig_bar_update = sig_bar_update
        self.label = label
        self.thread_index = thread_index

        self.parent = parent

        self.label.setText(text)

    def run(self):
        self.sig_bar_update.emit(PROGRESS_BAR_MAX)

        for i in range(PROGRESS_BAR_MAX):
            # Stop condition
            if self.thread_index != self.parent.get_last_thread():
                self.sig_bar_update.emit(PROGRESS_BAR_MAX)
                return

            self.sig_bar_update.emit(PROGRESS_BAR_MAX - i)

            sleep(0.01)

        self.sig_bar_update.emit(PROGRESS_BAR_MAX)
        self.label.setText("")
