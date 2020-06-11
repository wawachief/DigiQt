# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QSlider
from PySide2.QtCore import Qt


class SpeedSlider(QSlider):

    def __init__(self, width, height, config):
        """
        Custom slider for the execution's speed selection

        :param sig_status: signal that is connected to the statusbar
        :param width:
        :param height:
        :param config: configuration file
        """
        QSlider.__init__(self, Qt.Horizontal)

        self.config = config

        self.setMinimum(0)
        self.setMaximum(255)

        self.setFixedSize(width, height)
        self.setToolTip("Execution speed")

        self.setStyleSheet("border-left: 2px solid #333333; background-color: " + self.config.get('colors', 'slider_bg') + ";")

        self.valueChanged.connect(self.value_changed)

    def value_changed(self):
        """
        Trigerred upon value change event
        """
        pass