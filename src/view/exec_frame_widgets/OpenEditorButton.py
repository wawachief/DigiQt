# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QPushButton

import src.assets_manager as assets_mgr


class OpenEditorButton(QPushButton):
    def __init__(self, editor_frame):
        """
        Button handling the open/close operation of the editor frame

        :param editor_frame: The editor frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_editor"))
        self.setToolTip("Open Editor")
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setStyleSheet('border: none; padding-left: 10px; background-color: #333333;')

        self.editor_frame = editor_frame

        self.clicked.connect(lambda: self.show_editor_frame(not self.editor_frame.isVisible()))

    def show_editor_frame(self, do_display):
        """
        Hides or shows the editor frame

        :param do_display: True will display the editor frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setIcon(assets_mgr.get_icon("close_editor"))
            self.setToolTip("Close Editor")

            self.editor_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("open_editor"))
            self.setToolTip("Open Editor")

            self.editor_frame.hide()
