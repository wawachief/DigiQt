from src.model.cpu import Cpu
from src.model.assemble import Assemble
from configparser import ConfigParser
from src.view.MainApp import ExecutionFrame

class Controller:
    def __init__(self):
        config = ConfigParser()
        config.read('src/config.ini')
        dr_model = config.get('digirule', 'DR_MODEL')
        self.widget = ExecutionFrame(config)
        self.widget.show()
