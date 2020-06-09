# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of editor frame
#

from PySide2.QtWidgets import QPushButton, QFileDialog
import src.assets_manager as assets_mgr


class OpenFileButton(QPushButton):
    def __init__(self):
        """
        Button handling the open file operation
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_file"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Open File")
        self.setStyleSheet('border: none; padding-left: 10px; background-color: #333333;')

        self.clicked.connect(self.on_open)

        self.file_path = ""

    def on_open(self):
        """
        Shows a file chooser dialog
        """
        print("click")
        dlg = QFileDialog()
        dlg.setWindowTitle("Choose a file to open")
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Text files (*.txt);;ASM files (*.asm)")

        if dlg.exec_():
            self.file_path = dlg.selectedFiles()[0]

            file = open(self.file_path, "r")
            with file:
                code = file.read()
                self.set_content(code)

    def set_content(self, text):
        """
        Method to reroute in the Editor in order to write down the content given
        """
        pass
