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


class OpenRamButton(QPushButton):
    def __init__(self, ram_frame, config):
        """
        Button handling the open/close operation of the ram frame

        :param ram_frame: The ram frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_editor"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Show RAM")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

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


class OpenConsoleButton(QPushButton):
    def __init__(self, console_frame, config):
        """
        Button handling the open/close operation of the serial console frame

        :param console_frame: The console frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_editor"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Show Serial Console")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.console_frame = console_frame

        self.clicked.connect(lambda: self.show_console_frame(not self.console_frame.isVisible()))

    def show_console_frame(self, do_display):
        """
        Hides or shows the serial console frame

        :param do_display: True will display the console frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setIcon(assets_mgr.get_icon("close_editor"))
            self.setToolTip("Hide Serial Console")

            self.console_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("open_editor"))
            self.setToolTip("Show Serial Console")

            self.console_frame.hide()


class AboutButton(QPushButton):
    def __init__(self, config, sig_message):
        """
        About
        """
        QPushButton.__init__(self)

        self.sig_messsage = sig_message

        self.setIcon(assets_mgr.get_icon("info"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("About us")
        self.setStyleSheet('border: none; padding-right: 10px; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(self.on_about)

    def on_about(self):
        self.sig_messsage.emit("LÉCLUSE - DevCorp. ©")
