from PySide2.QtWidgets import (QToolBar, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Qt


import src.assets_manager as assets_mgr

APP_VERSION = "BETA-0.1"  # Application version

TOOLBAR_BTN_WIDTH = 50


class ExecutionFrame(QWidget):

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
        self.open_editor_btn.setIcon(assets_mgr.get_icon("open_editor"))
        self.open_editor_btn.setIconSize(assets_mgr.ICON_SIZE)
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
