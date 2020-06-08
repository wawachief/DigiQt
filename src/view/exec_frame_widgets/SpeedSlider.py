# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QSlider
from PySide2.QtCore import Qt


class SpeedSlider(QSlider):

    def __init__(self, sig_status, width, height):
        """
        Custom slider for the execution's speed selection

        :param sig_status: signal that is connected to the statusbar
        :type sig_status: Signal
        :param width:
        :param height:
        """
        QSlider.__init__(self, Qt.Horizontal)

        self.sig_status = sig_status

        self.setMinimum(0)
        self.setMaximum(255)

        self.setFixedSize(width, height)
        self.setToolTip("Execution speed")

        self.setStyleSheet("border-left: 2px solid #333333; background-color: #585858;")

        self.valueChanged.connect(self.value_changed)

    def value_changed(self):
        """
        Trigerred upon value change event
        """

        self.sig_status.emit("Speed value set to " + str(self.value()))

        # TODO: call the update speed method using 'self.value()' to retrieve current value
