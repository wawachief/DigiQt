from PySide2.QtWidgets import (QToolBar, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Qt, QSize

import src.assets_manager as assets_mgr


class EditorFrame(QWidget):

    # --- Init methods ---

    def __init__(self, parent_frame):
        """
        Editor frame. Contains a toolbar and an editor widget

        :param parent_frame: Main application frame (the execution frame)
        :type parent_frame: ExecutionFrame
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - Assemble Editor")
        self.setMinimumSize(QSize(630, 500))

        self.exec_frame = parent_frame

        self._initToolBar()
        self._setLayout()
        self._connectAll()

    def _initToolBar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

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

    # --- Buttons callbacks methods ---

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click.

        Updates the execution frame's open editor icon and tooltip
        """
        self.exec_frame.showEditorFrame(False)
