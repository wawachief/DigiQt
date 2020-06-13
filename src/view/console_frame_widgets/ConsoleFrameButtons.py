# Author: Thomas Lécluse
# Licence GPL-3

#
# Widgets of monitor frame
#

from PySide2.QtWidgets import QPushButton, QFileDialog
import src.assets_manager as assets_mgr


class ToDigiruleButton(QPushButton):
    def __init__(self, config):
        """
        Button handling the ToDigirule operation
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("to_digirule"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("To Digirule")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(self.to_digirule)

    def to_digirule(self):
        pass


class FromDigiruleButton(QPushButton):
    def __init__(self, config):
        """
        Button handling the FromDigirule operation
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("from_digirule"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("From Digirule")
        self.setStyleSheet('border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(self.from_digirule)

    def from_digirule(self):
        pass


class ClearButton(QPushButton):
    def __init__(self, config):
        """
        Button handling the clear operation on the serial out field
        """
        QPushButton.__init__(self)

        self.config = config

        self.setIcon(assets_mgr.get_icon("clear"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Clear Serial out")
        self.set_style()

        self.clicked.connect(self.on_clear)

    def set_style(self, is_clicked=False):
        """
        Sets a different style whereas this button is clicked or not
        """
        if is_clicked:
            color = self.config.get('colors', 'toolbar_clicked_icon_btn_bg')
        else:
            color = self.config.get('colors', 'toolbar_icon_btn_bg')

        self.setStyleSheet(f"border: none; margin-left: 10px; background-color: {color};")

    def mousePressEvent(self, e):
        """
        Overrides to call the style update
        """
        self.set_style(True)

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """
        Overrides to call the style update
        """
        self.set_style(False)

        super().mouseReleaseEvent(e)

    def on_clear(self):
        pass
