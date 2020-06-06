from PySide2.QtWidgets import (QToolBar, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Qt


import src.assets_manager as assets_mgr

APP_VERSION = "BETA-0.1"  # Application version


class ExecutionFrame(QWidget):

    # --- Init methods ---

    def __init__(self):
        """
        Main application frame. Contains the MenuBar, main toolbar, DR canvas and status bar.
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - Emulator for Digirule - " + str(APP_VERSION))

        self.is_editor_opened = False

        self._initToolBar()
        self._setLayout()
        self._connectAll()

    def _initToolBar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.open_editor_btn = QPushButton()
        self.open_editor_btn.setIcon(assets_mgr.get_icon("open_editor"))
        self.open_editor_btn.setToolTip("Open Editor")
        self.open_editor_btn.setIconSize(assets_mgr.ICON_SIZE)
        self.open_editor_btn.setStyleSheet('border: none; padding-left: 10px;')

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
        """
        Handles the click on the open editor button
        """
        if not self.is_editor_opened:  # opening editor frame
            print("Opening editor...")

            self.open_editor_btn.setIcon(assets_mgr.get_icon("close_editor"))
            self.open_editor_btn.setToolTip("Close Editor")

        else:  # closing editor frame
            print("Closing editor...")

            self.open_editor_btn.setIcon(assets_mgr.get_icon("open_editor"))
            self.open_editor_btn.setToolTip("Open Editor")

        self.is_editor_opened = not self.is_editor_opened
