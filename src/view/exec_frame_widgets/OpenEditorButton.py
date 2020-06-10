# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QPushButton

import src.assets_manager as assets_mgr


class OpenEditorButton(QPushButton):
    def __init__(self, editor_frame, config):
        """
        Button handling the open/close operation of the editor frame

        :param editor_frame: The editor frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_editor"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Open Editor")
        self.setStyleSheet('border: none; padding-left: 10px; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

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
