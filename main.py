import sys
from PySide2.QtWidgets import QApplication

from src.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctrl = Controller()
    ctrl.widget.show()

    sys.exit(app.exec_())
