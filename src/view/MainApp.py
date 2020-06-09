# Author: Thomas Lécluse
# Licence GPL-3

#
# Execution frame
#

from PySide2.QtWidgets import QToolBar, QVBoxLayout, QHBoxLayout, QWidget, QSlider
from PySide2.QtCore import Qt, Signal

from src.view.Editor import EditorFrame
from src.view.exec_frame_widgets.DigiruleCanvas import DRCanvas
from src.view.exec_frame_widgets.DigiruleModelDropdown import DigiruleModelDropdown
from src.view.exec_frame_widgets.OpenEditorButton import OpenEditorButton
from src.view.exec_frame_widgets.StatusBar import StatusBar
from src.view.exec_frame_widgets.SpeedSlider import SpeedSlider
from src.view.style import style


class ExecutionFrame(QWidget):

    sig_status_message = Signal(str)  # new statusbar message signal

    # --- Init methods ---

    def __init__(self, config, sig_update_config):
        """
        Main application frame. Contains the MenuBar, main toolbar, DR canvas and status bar.

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.config = config

        app_version = self.config.get('main', 'APP_VERSION')
        self.setWindowTitle("DigiQt - Emulator for Digirule - " + str(app_version))
        window_width = int(self.config.get('main', 'WINDOW_WIDTH'))
        self.setFixedSize(window_width, 340)

        self.current_digirule_model = self.config.get('digirule', 'DR_MODEL')

        sliderbar_width = 200
        bottom_widget_height = 26

        self.editor_frame = EditorFrame(self)
        self.dr_canvas = DRCanvas(self, self.sig_status_message, window_width, self.current_digirule_model)
        self.statusbar = StatusBar(window_width - sliderbar_width, bottom_widget_height)
        self.slider = SpeedSlider(self.sig_status_message, sliderbar_width, bottom_widget_height)

        self._init_tool_bar()
        self._set_layout()
        self._set_stylesheets()

        self.sig_status_message.connect(self.statusbar.display_for_4_sec)
        self.sig_update_config = sig_update_config

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.open_editor_btn = OpenEditorButton(self.editor_frame)
        self.toolbar.addWidget(self.open_editor_btn)

        self.toolbar.addSeparator()
        self.digimodel_dropdown = DigiruleModelDropdown(self.on_digimodel_dropdown_changed, self.current_digirule_model)
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

        bottom_box = QHBoxLayout()
        bottom_box.setContentsMargins(0, 0, 0, 0)

        bottom_box.addWidget(self.statusbar)
        bottom_box.addWidget(self.slider)

        box.addLayout(bottom_box)
        box.setAlignment(bottom_box, Qt.AlignBottom)

        self.setLayout(box)

    def _set_stylesheets(self):
        self.toolbar.setStyleSheet(style.get_stylesheet("qtoolbar"))

        # Execution Frame
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
        self.sig_update_config.emit(self.digimodel_dropdown.get_digirule_model())

        self.dr_canvas.digirule_changed(self.config.get('digirule', 'DR_MODEL'))

    # --- Close handler ---
    def do_quit(self):
        pass
    def closeEvent(self, event):
        """
        Event called upon a red-cross click
        """
        self.do_quit()
        event.accept()
