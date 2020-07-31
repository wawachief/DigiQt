# Author: Thomas Lécluse
# License GPL-3

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

        self.setIcon(assets_mgr.get_icon("show_editor"))
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
            self.setIcon(assets_mgr.get_icon("hide_editor"))
            self.setToolTip("Close Editor")

            self.editor_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("show_editor"))
            self.setToolTip("Open Editor")

            self.editor_frame.hide()


class OpenRamButton(QPushButton):
    def __init__(self, ram_frame, config):
        """
        Button handling the open/close operation of the ram frame

        :param ram_frame: The ram frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("show_debug"))
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
            self.setIcon(assets_mgr.get_icon("hide_debug"))
            self.setToolTip("Hide RAM")

            self.ram_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("show_debug"))
            self.setToolTip("Show RAM")

            self.ram_frame.hide()


class OpenUSBButton(QPushButton):
    def __init__(self, usb_frame, config):
        """
        Button handling the open/close operation of the usb control frame

        :param usb_frame: The usb frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("show_monitor"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Show USB controls")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.usb_frame = usb_frame

        self.clicked.connect(lambda: self.show_usb_frame(not self.usb_frame.isVisible()))

    def show_usb_frame(self, do_display):
        """
        Hides or shows the usb control frame

        :param do_display: True will display the usb frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setIcon(assets_mgr.get_icon("hide_monitor"))
            self.setToolTip("Hide USB controls")

            self.usb_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("show_monitor"))
            self.setToolTip("Show USB controls")

            self.usb_frame.hide()

        self.is_opened(do_display)

    def is_opened(self, b_visible):
        pass

class OpenTerminalButton(QPushButton):
    def __init__(self, terminal_frame, config):
        """
        Button handling the open/close operation of the serial terminal frame

        :param terminal_frame: The terminal frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("show_terminal"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Show Serial terminal")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')
        self.config = config

        self.terminal_frame = terminal_frame

        self.clicked.connect(lambda: self.show_terminal_frame(not self.terminal_frame.isVisible()))

    def show_terminal_frame(self, do_display):
        """
        Hides or shows the serial terminal frame

        :param do_display: True will display the terminal frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setIcon(assets_mgr.get_icon("hide_terminal"))
            self.setToolTip("Hide Serial terminal")
            self.terminal_frame.terminal.sig_terminal_open.emit(True)  # Ask Serial controler to Start serial thread
            self.terminal_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("show_terminal"))
            self.setToolTip("Show Serial terminal")
            self.terminal_frame.terminal.sig_terminal_open.emit(False) # Ask Serial controler to Stop serial thread
            self.terminal_frame.hide()

        self.is_opened(do_display)

    def is_opened(self, b_visible):
        pass


class OpenSymbolButton(QPushButton):
    def __init__(self, symbol_frame, config):
        """
        Button handling the open/close operation of the symbols frame

        :param symbol_frame: The symbol frame that this button shows/hides
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("show_symbols"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Show symbols list frame")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.symbol_frame = symbol_frame

        self.clicked.connect(lambda: self.show_symbol_frame(not self.symbol_frame.isVisible()))

    def show_symbol_frame(self, do_display):
        """
        Hides or shows the symbol frame

        :param do_display: True will display the symbol frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setIcon(assets_mgr.get_icon("hide_symbols"))
            self.setToolTip("Hide symbols list frame")

            self.symbol_frame.show()
        else:
            self.setIcon(assets_mgr.get_icon("show_symbols"))
            self.setToolTip("Show symbols list frame")

            self.symbol_frame.hide()


class AboutButton(QPushButton):
    def __init__(self, about_frame, config):
        """
        About
        """
        QPushButton.__init__(self)

        self.about_frame = about_frame

        self.setIcon(assets_mgr.get_icon("info"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("About us")
        self.setStyleSheet('border: none; padding-right: 10px; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(lambda: self.show_about_frame(not self.about_frame.isVisible()))

    def show_about_frame(self, do_display):
        """
        Hides or shows the symbol frame

        :param do_display: True will display the symbol frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.setToolTip("Hide symbols list frame")

            self.about_frame.show()
        else:
            self.setToolTip("Show symbols list frame")

            self.about_frame.hide()
