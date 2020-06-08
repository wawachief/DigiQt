# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Slot


class StatusBar(QLabel):

    def __init__(self, window_width):
        """
        Custom widget for the execution frame's status bar

        :param window_width: application window width, to use as width for this label as well
        :type window_width: int
        """
        QLabel.__init__(self)

        self.setFixedSize(window_width, 26)
        self.setStyleSheet("padding-left: 1em; background-color: #585858; color: cyan;")

    @Slot(str)
    def display(self, text):
        """
        Displays the given text

        :param text: text to display
        :type text: str
        """
        self.setText(text)

    def clear(self):
        """
        Clears the content
        """
        self.setText("")
