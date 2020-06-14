# Author: Thomas Lécluse
# License GPL-3

#
# Widget of serial monitor frame
#

from PySide2.QtWidgets import QComboBox
from PySide2.QtCore import QSize
from src.view.style import style


class UsbPortCombo(QComboBox):
    def __init__(self):
        """
        Customed dropdown button for the usb-port selection
        """
        QComboBox.__init__(self)

        self.setStyleSheet(style.get_stylesheet("qcombobox"))
        self.activated.connect(self.on_selection_changed)
        self.setFixedSize(QSize(200, 30))
        self.sig_port_change = None # pushed by serial controler

    def set_ports(self, ports, selection = None):
        """
        Sets all the given ports in this combo box
        """
        if selection:
            self.setCurrentText(selection)
        else:
            self.clear()
            self.addItems(ports)

    def on_selection_changed(self):
        """
        Callback for selection change
        """
        port = self.currentText()
        self.setToolTip(port)
        self.sig_port_change.emit(port)
