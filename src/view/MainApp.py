# Author: Thomas Lécluse
# Licence GPL-3

#
# Execution frame
#

from PySide2.QtWidgets import QToolBar, QVBoxLayout, QWidget
from PySide2.QtCore import Qt, Signal

from src.view.Editor import EditorFrame
from src.view.exec_frame_widgets.DigiruleCanvas import DRCanvas
from src.view.exec_frame_widgets.DigiruleModelDropdown import DigiruleModelDropdown
from src.view.exec_frame_widgets.OpenEditorButton import OpenEditorButton
from src.view.exec_frame_widgets.StatusBar import StatusBar
from src.view.style import style

APP_VERSION = "BETA-0.1"  # Application version


class ExecutionFrame(QWidget):

    sig_status_message = Signal(str)  # new statusbar message signal

    # --- Init methods ---

    def __init__(self, window_width):
        """
        Main application frame. Contains the MenuBar, main toolbar, DR canvas and status bar.

        :param window_width: application window width, to use as width for this label as well
        :type window_width: int
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - Emulator for Digirule - " + str(APP_VERSION))
        self.setFixedSize(window_width, 400)

        self.current_digirule_model = "2B"  # Insert here the load process from config file for the digirule's model

        self.editor_frame = EditorFrame(self)
        self.dr_canvas = DRCanvas(self, self.sig_status_message, window_width, self.current_digirule_model)
        self.statusbar = StatusBar(window_width)

        self._init_tool_bar()
        self._set_layout()
        self._set_stylesheets()

        self.sig_status_message.connect(self.statusbar.display)

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.open_editor_btn = OpenEditorButton(self.editor_frame)
        self.toolbar.addWidget(self.open_editor_btn)

        self.toolbar.addSeparator()
        self.digimodel_dropdown = DigiruleModelDropdown(self.on_digimodel_dropdown_changed)
        self.toolbar.addWidget(self.digimodel_dropdown)

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.toolbar)
        box.setAlignment(self.toolbar, Qt.AlignTop)

        box.addWidget(self.dr_canvas)
        box.setAlignment(self.dr_canvas, Qt.AlignTop)

        box.addSpacing(20)

        box.addWidget(self.statusbar)
        box.setAlignment(self.statusbar, Qt.AlignBottom)

        self.setLayout(box)

    def _set_stylesheets(self):
        # ToolBar
        self.toolbar.setStyleSheet('border: none; background-color: #333333;')

        # Execution Frame
        self.setStyleSheet('background-color: #000000;')
        self.setStyleSheet(style.get_stylesheet("common"))

    # --- Callbacks methods ---

    def show_editor_frame(self, do_display):
        """
        Delegates the process to the editor's open/close button
        """
        self.open_editor_btn.show_editor_frame(do_display)

    def on_digimodel_dropdown_changed(self):
        """
        Handles the Digirule's model-combo-box-selection-changed process. Calls the canvas redraw.
        """
        # Insert here the persistent save operation in the config file for the digirule's model
        self.current_digirule_model = self.digimodel_dropdown.get_digirule_model()

        self.dr_canvas.digirule_changed(self.current_digirule_model)

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click
        """
        print("bye")
        event.accept()
