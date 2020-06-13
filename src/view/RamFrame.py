# Author: Thomas Lécluse
# Licence GPL-3

#
# RAM frame
#

from PySide2.QtWidgets import QFormLayout, QGridLayout, QWidget, QPlainTextEdit, QLabel
from PySide2.QtCore import QSize

from src.view.style import style

from src.view.debug_frame_widgets.RamContent import RamDebugText


class RAMFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        Editor frame. Contains a toolbar and an editor widget
        """
        QWidget.__init__(self)

        self.setWindowTitle("DigiQt - RAM")
        self.setFixedSize(QSize(330, 630))

        self.ram_content = RamDebugText(config)
        self.ram_content.setMinimumSize(QSize(350, 650))

        self.lab_ac = QLabel("AC:")
        self.lab_pc = QLabel("PC:")
        self.lab_stack = QLabel("Stack:")
        self.lab_st = QLabel("ST:")

        self.val_ac = QLabel("")
        self.val_pc = QLabel("")
        self.val_stack = QLabel("")
        self.val_st = QLabel("")

        self._set_layout()
        self._set_stylesheet()

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        form_layout = QFormLayout()

        form_layout.addRow(self.lab_ac, self.val_ac)
        form_layout.addRow(self.lab_pc, self.val_pc)
        form_layout.addRow(self.lab_stack, self.val_stack)
        form_layout.addRow(self.lab_st, self.val_st)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)

        grid.addLayout(form_layout, 0, 0)

        grid.addWidget(self.ram_content, 1, 0)

        self.setLayout(grid)

    def _connect_all(self):
        """
        Connects all the buttons to methods
        """

    def _set_stylesheet(self):
        self.setStyleSheet(style.get_stylesheet("debug_frame"))

    def set_ram_content(self, text):
        """
        Sets the content of the RAM text holder

        :param text: text to set
        """
        self.ram_content.setPlainText(text)

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

    def set_pc(self, val):
        self.val_pc.setText(val)

    def set_ac(self, val):
        self.val_ac.setText(val)

    def set_stack(self, val):
        self.val_stack.setText(val)

    def set_st(self, val):
        self.val_st.setText(val)
