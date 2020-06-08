# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Slot


class StatusBar(QLabel):

    def __init__(self, width, height):
        """
        Custom widget for the execution frame's status bar

        :param width: to use as width for this label
        :type width: int
        :param height: to use as height for this label
        :type height: int
        """
        QLabel.__init__(self)

        self.setFixedSize(width, height)
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
