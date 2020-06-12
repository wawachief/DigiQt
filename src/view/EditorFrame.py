# Author: Thomas Lécluse
# Licence GPL-3

#
# Edition frame
#

from PySide2.QtWidgets import QToolBar, QGridLayout, QWidget
from PySide2.QtCore import Qt, QSize

from src.view.editor_frame_widgets.EditorFrameButtons import OpenFileButton, AssembleButton, SaveAsFileButton

from src.view.editor_frame_widgets.CodeEditor import CodeEditor
from src.view.style import style


class EditorFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        Editor frame. Contains a toolbar and an editor widget

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.__init_title()
        self.setMinimumSize(QSize(630, 500))

        self.config = config

        self.editor = CodeEditor(config)
        self.editor.setMinimumSize(QSize(600, 430))

        self.open_file_btn = OpenFileButton(config)
        self.open_file_btn.set_content = self.editor.setPlainText  # Reroute text set method directly to the text editor widget
        self.open_file_btn.set_new_file_name = self.__init_title

        self.save_as_btn = SaveAsFileButton(config)
        self.save_as_btn.get_content_to_save = self.retrieve_text  # Bind the text retrieve method in order to get the text to save
        self.save_as_btn.set_new_file_name = self.__init_title

        self.assemble_btn = AssembleButton(config)

        self._init_tool_bar()
        self._set_layout()
        self._connect_all()
        self._set_stylesheet()

    def __init_title(self, file_name=""):
        """
        Sets the currently edited file in this frame's title
        """
        if file_name:
            self.setWindowTitle("DigiQt - Editing '" + file_name + "'")
        else:
            # In the case no file name is specified, we have an empty editor, we display default text
            self.setWindowTitle("DigiQt - Assemble Editor")

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.toolbar.addWidget(self.open_file_btn)
        self.toolbar.addWidget(self.save_as_btn)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.assemble_btn)

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QGridLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.toolbar, 0, 0)

        box.addWidget(self.editor, 1, 0)

        self.setLayout(box)

    def _connect_all(self):
        """
        Connects all the buttons to methods
        """

    def _set_stylesheet(self):
        self.toolbar.setStyleSheet(style.get_stylesheet("qtoolbar"))
        self.editor.setStyleSheet("background-color: " + self.config.get('colors', 'editor_bg') +
                                  "; color: " + self.config.get('colors', 'asm_text_default') + ";")

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
        """
        self.on_close()

    def on_close(self):
        """
        Reroot this method in the Main Frame in order to Updates the execution frame's open editor icon and tooltip
        :return:
        """
        pass
