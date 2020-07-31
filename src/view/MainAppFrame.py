# Author: Thomas Lécluse
# License GPL-3

#
# Execution frame
#

from PySide2.QtWidgets import QToolBar, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from PySide2.QtCore import Qt

from src.view.EditorFrame import EditorFrame
from src.view.RamFrame import RAMFrame
from src.view.TerminalFrame import TerminalFrame
from src.view.USBControlFrame import USBFrame
from src.view.SymbolViewFrame import SymbolViewFrame
from src.view.AboutFrame import AboutFrame
from src.view.exec_frame_widgets.DigiruleCanvas import DRCanvas
from src.view.exec_frame_widgets.DigiruleModelDropdown import DigiruleModelDropdown
from src.view.exec_frame_widgets.ExecFrameButtons import OpenEditorButton, OpenRamButton, OpenUSBButton, OpenTerminalButton, AboutButton, OpenSymbolButton
from src.view.exec_frame_widgets.StatusBar import StatusBar
from src.view.exec_frame_widgets.SpeedSlider import SpeedSlider
from src.view.style import style
from src.view.popup.QuitConfirmDialog import DialogQuitConfirmation


class ExecutionFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config, sig_update_config):
        """
        Main application frame. Contains the MenuBar, main toolbar, DR canvas and status bar.

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.config = config
        self.is_quitting = False

        app_version = self.config.get('main', 'APP_VERSION')
        self.setWindowTitle("DigiQt - Emulator for Digirule - " + str(app_version))
        window_width = int(self.config.get('main', 'WINDOW_WIDTH'))
        self.setFixedSize(window_width, 320)

        self.current_digirule_model = self.config.get('digirule', 'DR_MODEL')

        sliderbar_width = 200
        bottom_widget_height = 26

        self.statusbar = StatusBar(window_width - sliderbar_width, bottom_widget_height, config)
        self.dr_canvas = DRCanvas(self.statusbar.sig_temp_message, window_width, self.current_digirule_model, config)
        self.slider = SpeedSlider(sliderbar_width, bottom_widget_height, config)

        # Buttons open/hide frames
        self.editor_frame = EditorFrame(config, self.statusbar.sig_temp_message)
        self.open_editor_btn = OpenEditorButton(self.editor_frame, config)
        self.editor_frame.on_close = lambda: self.open_editor_btn.show_editor_frame(False)

        self.ram_frame = RAMFrame(config)
        self.open_ram_btn = OpenRamButton(self.ram_frame, config)
        self.ram_frame.on_close = lambda: self.open_ram_btn.show_ram_frame(False)

        self.monitor_frame = TerminalFrame(config)
        self.open_monitor_btn = OpenTerminalButton(self.monitor_frame, config)
        self.monitor_frame.on_close = lambda: self.open_monitor_btn.show_terminal_frame(False)

        self.usb_frame = USBFrame(config)
        self.open_usb_btn = OpenUSBButton(self.usb_frame, config)
        self.usb_frame.on_close = lambda: self.open_usb_btn.show_usb_frame(False)

        self.open_monitor_btn.is_opened = lambda b: self.open_usb_btn.setEnabled(not b)
        self.open_usb_btn.is_opened = lambda b: self.open_monitor_btn.setEnabled(not b)

        self.symbol_frame = SymbolViewFrame(config)
        self.open_symbol_btn = OpenSymbolButton(self.symbol_frame, config)
        self.symbol_frame.on_close = lambda: self.open_symbol_btn.show_symbol_frame(False)
        self.symbol_frame.place_search_text = self.editor_frame.do_search

        self.about_frame = AboutFrame(self.config)
        self.open_about_btn = AboutButton(self.about_frame, config)
        self.about_frame.on_close = lambda: self.open_about_btn.show_about_frame(False)

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

        # Open/hide buttons
        self.toolbar.addWidget(self.open_editor_btn)
        self.toolbar.addWidget(self.open_ram_btn)
        self.toolbar.addWidget(self.open_monitor_btn)
        self.toolbar.addWidget(self.open_usb_btn)
        self.toolbar.addWidget(self.open_symbol_btn)

        # Digirule model selection
        self.toolbar.addSeparator()
        self.digimodel_dropdown = DigiruleModelDropdown(self.on_digimodel_dropdown_changed)
        self.toolbar.addWidget(self.digimodel_dropdown)

        # Empty space to align the about button to the right
        spacer = QWidget()
        spacer.setStyleSheet("background-color: transparent;")
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        # About button
        self.toolbar.addWidget(self.open_about_btn)

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
        if self.ask_quit_confirmation():
            self.is_quitting = True
            self.do_quit()

            # Reset status bar
            self.statusbar.sig_persistent_message.emit("")

            # Call the secondary frames close methods as well
            self.editor_frame.on_close()
            self.ram_frame.on_close()
            self.monitor_frame.on_close()
            self.usb_frame.on_close()
            self.symbol_frame.on_close()
            self.about_frame.on_close()

            event.accept()
        else:
            event.ignore()

    def ask_quit_confirmation(self):
        """
        Asks a quit confirmation message
        :return: True if the user wants to quit the app
        """
        return DialogQuitConfirmation().exec_()
