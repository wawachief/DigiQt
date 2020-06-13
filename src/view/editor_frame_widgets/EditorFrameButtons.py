# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of editor frame
#

from PySide2.QtWidgets import QPushButton, QFileDialog
import src.assets_manager as assets_mgr


class OpenFileButton(QPushButton):
    def __init__(self, config):
        """
        Button handling the open file operation
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("open_file"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Open File")
        self.setStyleSheet('border: none; padding-left: 10px; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(self.on_open)

    def on_open(self):
        """
        Shows a file chooser dialog
        """
        dlg = QFileDialog()
        dlg.setWindowTitle("Choose a file to open")
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("ASM files (*.asm);;Text files (*.txt)")

        if dlg.exec_():
            file_path = dlg.selectedFiles()[0]

            with open(file_path, "r") as file:
                code = file.read()
                self.set_content(code)

                self.set_new_file_name(file_path)

    def set_content(self, text):
        """
        Method to reroute in the Editor in order to write down the content given
        """
        pass

    def set_new_file_name(self, file_name):
        """
        Method to reroute in order to update the current file name displayed
        :param file_name: opened file name
        """
        pass


class AssembleButton(QPushButton):
    def __init__(self, config):
        """
        Button handling the assemble operation
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("assemble"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Assemble")
        self.setStyleSheet('border: none; margin-right: 10px; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(self.on_assemble)

    def on_assemble(self):
        """
        Method to reroute in the Editor in order to process the assemble operation event
        """
        pass


class SaveAsFileButton(QPushButton):
    def __init__(self, config, sig_message):
        """
        Button handling the save as operation

        :param sig_message: signal to emit to display a message in the main frame's status bar
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("save_as"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Save As")
        self.setStyleSheet(
            'border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.clicked.connect(self.on_save_as)
        self.sig_message = sig_message

    def on_save_as(self):
        """
        Shows a file chooser dialog to select a save destination
        """
        dlg = QFileDialog()
        file_name = dlg.getSaveFileName(self, 'Browse destination', filter='ASM files (*.asm)')
        if file_name[0]:
            with open(file_name[0], "w") as file:
                file.write(self.get_content_to_save())
                self.set_new_file_name(file_name[0])
                self.sig_message.emit("File successfully saved: " + file_name[0])

    def get_content_to_save(self):
        """
        Method to reroute in order to return here the content of the file to save.

        :rtype: str
        """
        pass

    def set_new_file_name(self, file_name):
        """
        Method to reroute in order to update the current file name displayed
        :param file_name: saved file name
        """
        pass


class SaveFileButton(QPushButton):
    def __init__(self, config, sig_message):
        """
        Button handling the save file operation

        :param sig_message: signal to emit to display a message in the main frame's status bar
        """
        QPushButton.__init__(self)

        self.setIcon(assets_mgr.get_icon("save"))
        self.setIconSize(assets_mgr.ICON_SIZE)
        self.setToolTip("Save")
        self.setStyleSheet(
            'border: none; background-color: ' + config.get('colors', 'toolbar_icon_btn_bg') + ';')

        self.file_path = ""

        self.clicked.connect(self.on_save)

        self.sig_message = sig_message

    def on_save(self):
        """
        Shaves the file at the registered location
        """
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.get_content_to_save())
                self.sig_message.emit("File successfully saved: " + self.file_path)

    def get_content_to_save(self):
        """
        Method to reroute in order to return here the content of the file to save.

        :rtype: str
        """
        pass

    def set_file_path(self, path):
        """
        Method to reroute in order to update the current file name displayed
        :param path: file path
        """
        self.file_path = path

    def setEnabled(self, b):
        """
        Changes the tooltip of this button when disabled
        :param b: True to enable
        """
        super().setEnabled(b)
        self.setToolTip("Save" if b else "No file opened")
