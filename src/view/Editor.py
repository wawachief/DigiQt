# Author: Thomas Lécluse
# Licence GPL-3

#
# Edition frame
#

from PySide2.QtWidgets import QToolBar, QVBoxLayout, QWidget, QPlainTextEdit
from PySide2.QtCore import Qt, QSize

from src.view.editor_frame_widgets.OpenFileButton import OpenFileButton
from src.view.editor_frame_widgets.AssembleButton import AssembleButton
from src.view.style import style


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

        self.editor = QPlainTextEdit()  # TODO temporary
        self.editor.setMinimumSize(QSize(600, 430))

        self.open_file_btn = OpenFileButton()
        self.open_file_btn.set_content = self.editor.setPlainText  # Reroute text set method directly to the text editor widget

        self.assemble_btn = AssembleButton()

        self._init_tool_bar()
        self._set_layout()
        self._connect_all()
        self._set_stylesheet()

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.toolbar.addWidget(self.open_file_btn)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.assemble_btn)

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.toolbar)
        box.setAlignment(self.toolbar, Qt.AlignTop)

        box.addWidget(self.editor)
        box.setAlignment(self.editor, Qt.AlignTop)

        self.setLayout(box)

    def _connect_all(self):
        """
        Connects all the buttons to methods
        """

    def _set_stylesheet(self):
        self.toolbar.setStyleSheet(style.get_stylesheet("qtoolbar"))
        self.editor.setStyleSheet("background-color: #505050; color: white")

        # Execution Frame
        self.setStyleSheet(style.get_stylesheet("common"))

    # --- Buttons callbacks methods ---

    def retrieve_text(self):
        """
        Gets the content of the code editor widget
        :return: the code
        """
        return self.editor.toPlainText()

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click.

        Updates the execution frame's open editor icon and tooltip
        """
        self.exec_frame.show_editor_frame(False)
