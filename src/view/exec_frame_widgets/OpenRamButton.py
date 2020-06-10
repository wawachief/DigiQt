# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QPushButton

import src.assets_manager as assets_mgr


class OpenRamButton(QPushButton):
    def __init__(self, ram_frame):
        """
        Button handling the open/close operation of the ram frame

        :param ram_frame: The ram frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_editor"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Show RAM")
        self.setStyleSheet('border: none; padding-left: 10px; background-color: #333333;')

        self.ram_frame = ram_frame

        self.clicked.connect(lambda: self.show_ram_frame(not self.ram_frame.isVisible()))

    def show_ram_frame(self, do_display):
        """
        Hides or shows the ram frame

        :param do_display: True will display the ram frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setIcon(assets_mgr.get_icon("close_editor"))
            self.setToolTip("Hide RAM")

            self.ram_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("open_editor"))
            self.setToolTip("Show RAM")

            self.ram_frame.hide()
