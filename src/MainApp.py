import sys
from PySide2.QtWidgets import (QApplication, QToolBar, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Qt


from src.assets_manager import get_icon, ICON_SIZE

APP_VERSION = "BETA-0.1"  # Application version

TOOLBAR_BTN_WIDTH = 50


class MyWidget(QWidget):

    # --- Init methods ---

    def __init__(self):
        """
        Main application frame. Contains the MenuBar, main toolbar, DR canvas and status bar.
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - Emulator for Digirule - " + str(APP_VERSION))

        self._initToolBar()
        self._setLayout()
        self._connectAll()

    def _initToolBar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()

        self.open_editor_btn = QPushButton()
        self.open_editor_btn.setIcon(get_icon("open_editor"))
        self.open_editor_btn.setIconSize(ICON_SIZE)
        self.open_editor_btn.setFixedWidth(TOOLBAR_BTN_WIDTH)

        self.toolbar.addWidget(self.open_editor_btn)
        self.toolbar.addSeparator()

    def _setLayout(self):
        """
        Creates this Widget's Layout
        """
        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(10)

        box.addWidget(self.toolbar)
        box.setAlignment(self.toolbar, Qt.AlignTop)

        self.setLayout(box)

    def _connectAll(self):
        """
        Connects all the buttons to methods
        """
        self.open_editor_btn.clicked.connect(self.onOpenEditorBtnClicked)

    # --- Buttons callbacks methods ---

    def onOpenEditorBtnClicked(self):
        print("Opening editor...")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 400)
    widget.show()

    sys.exit(app.exec_())
