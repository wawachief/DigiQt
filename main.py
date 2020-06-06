import sys
from PySide2.QtWidgets import QApplication

from src.MainApp import ExecutionFrame

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = ExecutionFrame()
    widget.resize(800, 400)
    widget.show()

    sys.exit(app.exec_())
