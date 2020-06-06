from PySide2.QtWidgets import (QToolBar, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Qt

import src.assets_manager as assets_mgr
from src.Editor import EditorFrame

APP_VERSION = "BETA-0.1"  # Application version


class ExecutionFrame(QWidget):

    # --- Init methods ---

    def __init__(self):
        """
        Main application frame. Contains the MenuBar, main toolbar, DR canvas and status bar.
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - Emulator for Digirule - " + str(APP_VERSION))

        self.editor_frame = EditorFrame(self)

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
        self.open_editor_btn.clicked.connect(lambda: self.showEditorFrame(not self.editor_frame.isVisible()))

    # --- Buttons callbacks methods ---

    def showEditorFrame(self, do_display):
        """
        Hides or shows the editor frame

        :param do_display: True will display the editor frame, False will hide it
        :type do_display: bool
        """
        if do_display:
            self.open_editor_btn.setIcon(assets_mgr.get_icon("close_editor"))
            self.open_editor_btn.setToolTip("Close Editor")

            self.editor_frame.show()
        else:
            self.open_editor_btn.setIcon(assets_mgr.get_icon("open_editor"))
            self.open_editor_btn.setToolTip("Open Editor")

            self.editor_frame.hide()

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click
        """
        print("bye")
        event.accept()
