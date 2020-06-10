# Author: Thomas Lécluse
# Licence GPL-3

#
# Execution frame
#

from PySide2.QtWidgets import QToolBar, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide2.QtCore import Qt

from src.view.EditorFrame import EditorFrame
from src.view.RamFrame import RAMFrame
from src.view.exec_frame_widgets.DigiruleCanvas import DRCanvas
from src.view.exec_frame_widgets.DigiruleModelDropdown import DigiruleModelDropdown
from src.view.exec_frame_widgets.OpenEditorButton import OpenEditorButton
from src.view.exec_frame_widgets.OpenRamButton import OpenRamButton
from src.view.exec_frame_widgets.StatusBar import StatusBar
from src.view.exec_frame_widgets.SpeedSlider import SpeedSlider
from src.view.style import style


class ExecutionFrame(QWidget):

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

        self.editor_frame = EditorFrame(config)
        self.open_editor_btn = OpenEditorButton(self.editor_frame, config)
        self.editor_frame.on_close = lambda: self.open_editor_btn.show_editor_frame(False)

        self.ram_frame = RAMFrame()
        self.open_ram_btn = OpenRamButton(self.ram_frame, config)
        self.ram_frame.on_close = lambda: self.open_ram_btn.show_ram_frame(False)

        self.statusbar = StatusBar(window_width - sliderbar_width, bottom_widget_height, config)
        self.dr_canvas = DRCanvas(self.statusbar.sig_temp_message, window_width, self.current_digirule_model, config)
        self.slider = SpeedSlider(self.statusbar.sig_temp_message, sliderbar_width, bottom_widget_height, config)

        self._init_tool_bar()
        self._set_layout()
        self._set_stylesheets()

        self.sig_update_config = sig_update_config

    def _init_tool_bar(self):
        """
        Creates the main toolbar with all its content
        """
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(70)

        self.toolbar.addWidget(self.open_editor_btn)

        self.toolbar.addWidget(self.open_ram_btn)

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

        # Call the secondary frames close methods as well
        self.editor_frame.on_close()
        self.ram_frame.on_close()
        event.accept()