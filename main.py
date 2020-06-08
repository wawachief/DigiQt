import sys
from PySide2.QtWidgets import QApplication

from src.view.MainApp import ExecutionFrame

WINDOW_WIDTH = 1064

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = ExecutionFrame(WINDOW_WIDTH)
    widget.show()

    sys.exit(app.exec_())
