# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QComboBox
from PySide2.QtCore import QSize
from src.view.style import style


class DigiruleModelDropdown(QComboBox):
    def __init__(self, callback_function, init_model):
        """
        Customed dropdown button for the Digirule model selection
        """
        QComboBox.__init__(self)

        self.addItems(("2A", "2B", "2U"))
        self.setCurrentText(init_model)  # Switch to initial selection

        self.setStyleSheet(style.get_stylesheet("qcombobox"))

        self.activated.connect(callback_function)

        self.setFixedSize(QSize(70, 30))

    def get_digirule_model(self):
        """
        Gets the current model selection
        """
        return self.currentText()
