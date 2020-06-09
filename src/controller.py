from src.model.cpu import Cpu
from src.model.assemble import Assemble
from configparser import ConfigParser
from src.view.MainApp import ExecutionFrame

from PySide2.QtCore import Signal, Slot, QObject

CONFIG_FILE_PATH = 'src/config.ini'


class Controller(QObject):

    sig_config_changed = Signal(str)

    def __init__(self):
        QObject.__init__(self)

        self.config = ConfigParser()
        self.config.read(CONFIG_FILE_PATH)
        dr_model = self.config.get('digirule', 'DR_MODEL')
        self.widget = ExecutionFrame(self.config, self.sig_config_changed)
        self.widget.show()

        self.sig_config_changed.connect(self.on_config_changed)

    @Slot(str)
    def on_config_changed(self, new_value):
        """
        Updates the stored value for the current digirule model in the configuration file

        :param new_value: new digirule model value
        """
        self.config.set('digirule', 'DR_MODEL', new_value)

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)
