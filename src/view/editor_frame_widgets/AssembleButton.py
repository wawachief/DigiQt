# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of editor frame
#

from PySide2.QtWidgets import QPushButton, QFileDialog
import src.assets_manager as assets_mgr


class AssembleButton(QPushButton):
    def __init__(self):
        """
        Button handling the assemble operation
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("assemble"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Assemble")
        self.setStyleSheet('border: none; padding-left: 10px; background-color: #333333;')

        self.clicked.connect(self.on_assemble)

    def on_assemble(self):
        """
        Method to reroute in the Editor in order to process the assemble operation event
        """
        print("assemble")
        pass
