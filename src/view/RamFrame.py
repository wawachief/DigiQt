# Author: Thomas Lécluse
# Licence GPL-3

#
# RAM frame
#

from PySide2.QtWidgets import QFormLayout, QGridLayout, QWidget, QCheckBox, QLabel
from PySide2.QtCore import QSize, Qt

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
        self.setFixedWidth(300)

        self.ram_content = RamDebugText(config)
        self.ram_content.setFixedSize(QSize(300, 530))

        self.lab_ac = QLabel("AC:")
        self.lab_pc = QLabel("PC:")
        self.lab_stack = QLabel("Stack:")
        self.lab_st = QLabel("ST:")

        self.val_ac = QLabel("")
        self.val_pc = QLabel("")
        self.val_stack = QLabel("")
        self.val_st = QLabel("")

        self.hexa_checkbox = QCheckBox()
        self.hexa_checkbox.setText("Hexadecimal mode")
        self.hexa_checkbox.stateChanged.connect(self.on_hexa_box_changed)
        self.hexa_checkbox.setFixedHeight(50)

        self._set_layout()
        self.setStyleSheet(style.get_stylesheet("debug_frame"))

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        form_layout = QFormLayout()

        form_layout.addRow(self.lab_ac, self.val_ac)
        form_layout.addRow(self.lab_pc, self.val_pc)
        form_layout.addRow(self.lab_st, self.val_st)
        form_layout.addRow(self.lab_stack, self.val_stack)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)

        grid.addLayout(form_layout, 0, 0)

        grid.addWidget(self.ram_content, 1, 0)

        grid.addWidget(self.hexa_checkbox, 2, 0)
        grid.setAlignment(self.hexa_checkbox, Qt.AlignCenter)

        self.setLayout(grid)

    def on_hexa_box_changed(self):
        """
        Called when the Hexadecimal mode checkbox is selected or unselected
        """
        print(self.hexa_checkbox.isChecked())

    def _connect_all(self):
        """
        Connects all the buttons to methods
        """

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
