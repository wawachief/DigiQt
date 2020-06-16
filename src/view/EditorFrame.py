# Author: Thomas Lécluse
# License GPL-3

#
# Edition frame
#

from PySide2.QtWidgets import QToolBar, QGridLayout, QWidget, QSizePolicy, QLineEdit
from PySide2.QtCore import QSize

from src.view.editor_frame_widgets.EditorFrameButtons import OpenFileButton, AssembleButton, SaveAsFileButton, SaveFileButton

from src.view.editor_frame_widgets.CodeEditor import CodeEditor
from src.view.style import style


class EditorFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config, sig_message):
        """
        Editor frame. Contains a toolbar and an editor widget

        :param config: application configuration file
        :param sig_message: signal to emit to display a message in the main frame's status bar
        """
        QWidget.__init__(self)

        self.setMinimumSize(QSize(630, 500))

        self.config = config

        # Widgets
        self.editor = CodeEditor(config)
        self.editor.setMinimumSize(QSize(600, 430))

        self.open_file_btn = OpenFileButton(config)
        self.open_file_btn.set_content = self.editor.setPlainText  # Reroute text set method directly to the text editor widget
        self.open_file_btn.set_new_file_name = self.__init_title

        self.save_as_btn = SaveAsFileButton(config, sig_message)
        self.save_as_btn.get_content_to_save = self.retrieve_text  # Bind the text retrieve method in order to get the text to save
        self.save_as_btn.set_new_file_name = self.__init_title

        self.save_btn = SaveFileButton(config, sig_message)
        self.save_btn.get_content_to_save = self.retrieve_text

        self.assemble_btn = AssembleButton(config)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search (press return)")
        self.search_field.returnPressed.connect(self.do_search)

        # Editor's shortcuts binding
        self.editor.on_ctrl_o_activated = self.open_file_btn.on_open  # Open action
        self.editor.on_ctrl_s_activated = self.do_save
        self.editor.on_ctrl_f_activated = self.do_search

        # Final initialization
        self.__init_title()
        self._init_tool_bar()
        self._set_layout()
        self._connect_all()
        self._set_stylesheet()

        self.editor.setFocus()  # Set the default focus on the Editor

    def __init_title(self, file_name=""):
        """
        Sets the currently edited file in this frame's title

        :param file_name: full file path
        """
        if file_name:
            self.setWindowTitle("DigiQt - Editing '" + file_name.split("/")[-1] + "'")
        else:
            # In the case no file name is specified, we have an empty editor, we display default text
            self.setWindowTitle("DigiQt - Assemble Editor")

        self.save_btn.setEnabled(file_name != "")
        self.save_btn.set_file_path(file_name)

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.toolbar.addWidget(self.open_file_btn)
        self.toolbar.addWidget(self.save_btn)
        self.toolbar.addWidget(self.save_as_btn)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.search_field)

        # Empty space to align the assemble button to the right
        spacer = QWidget()
        spacer.setStyleSheet("background-color: transparent;")
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

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

        self.search_field.setStyleSheet(
            "border: 2px solid gray; border-radius: 10px; padding: 0 8px; background: #585858; color: white")

        # Execution Frame
        self.setStyleSheet(style.get_stylesheet("common"))

    # --- Buttons callbacks methods ---

    def retrieve_text(self):
        """
        Gets the content of the code editor widget
        :return: the code
        """
        return self.editor.toPlainText()

    def do_save(self):
        """
        Delegating method triggered upon Ctrl+S action. Performs a Save if a file is opened, or a SaveAs if not.
        """
        if self.save_btn.file_path:
            self.save_btn.on_save()
        else:
            self.save_as_btn.on_save_as()

    def do_search(self, text=None):
        """
        Searches the value present in the search field, or the places the specified text if there is one as search
        value, but does not triggers the search.

        :param text: Text to search (None will trigger a search on the field content)
        """
        if text:
            self.search_field.setText(text)
        else:
            self.editor.selectNext(self.search_field.text())

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
