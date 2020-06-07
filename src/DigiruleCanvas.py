from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap, QPainter, QColor, QPen, QMatrix
from PySide2.QtCore import QPoint

from src.digirules.DigiruleInfo import DigiruleInfo


class DRCanvas(QLabel):
    led_states = {
        "topLed7": False,
        "topLed6": False,
        "topLed5": False,
        "topLed4": False,
        "topLed3": False,
        "topLed2": False,
        "topLed1": False,
        "topLed0": False,
        "bottomLed7": False,
        "bottomLed6": False,
        "bottomLed5": False,
        "bottomLed4": False,
        "bottomLed3": False,
        "bottomLed2": False,
        "bottomLed1": False,
        "bottomLed0": False,
    }

    def __init__(self, parent_frame):
        """
        Canvas in witch is drawn the Digirule as well as its buttons

        :param parent_frame: Main application frame (the execution frame)
        :type parent_frame: ExecutionFrame
        """
        QLabel.__init__(self)

        self.exec_frame = parent_frame

        self.setFixedSize(1064, 204)  # 1/4 of the original size
        self.setScaledContents(True)

    def paintEvent(self, event):
        """
        Re-draws everything
        """
        super().paintEvent(event)

        # Pixmap that contains the painter and the DR
        current_digirule = self.exec_frame.getUsedDR()
        canvas = QPixmap("assets/" + DigiruleInfo.getImgName(current_digirule))
        self.setPixmap(canvas)
        painter = QPainter(self.pixmap())  # Create a painter in which buttons and LEDs are drawn

        translate_matrix = QMatrix()
        offset_scale = DigiruleInfo.getScaleOffset(current_digirule)
        translate_matrix.scale(offset_scale[0], offset_scale[1])
        painter.setMatrix(translate_matrix)

        # Drawing
        pen = QPen()
        pen.setWidth(DigiruleInfo.getButtonsWidth(current_digirule))
        pen.setColor(QColor(70, 70, 90, 150))  # Buttons color
        painter.setPen(pen)

        # Buttons
        buttons_dico = DigiruleInfo.getButtonsPositionsDico(current_digirule)
        for btn in buttons_dico:
            painter.drawPoint(QPoint(btn[0], btn[1]))

        # LEDs
        pen.setWidth(10)

        # First row of LEDs
        top_led_dico = DigiruleInfo.getTopLedPositionsDico(current_digirule)
        for led in top_led_dico:
            if self.led_states[top_led_dico[led]]:
                pen.setColor(QColor("red"))  # Top row of LEDs active color
            else:
                pen.setColor(QColor("black"))
            painter.setPen(pen)
            painter.drawPoint(QPoint(led[0], led[1]))

    def mouseReleaseEvent(self, event):
        """
        Intercepts the click on the canvas and calls the method associated to the clicked button, if there is one

        :param event:
        """
        print(event.x(), event.y())

        current_digirule = self.exec_frame.getUsedDR()
        w = DigiruleInfo.getButtonsWidth(current_digirule) / 2  # Accepted offset to click position
        btns_dico = DigiruleInfo.getButtonsPositionsDico(current_digirule)

        for btn in btns_dico:
            if btn[0] - w <= event.x() <= btn[0] + w and btn[1] - w <= event.y() <= btn[1] + w:
                self.processMethod(btns_dico[btn])

    def processMethod(self, btn_clicked):
        """
        Processes the method associated to the button pressed in the digirule's canvas

        :param btn_clicked: name of the button clicked
        :type btn_clicked: str
        """
        if btn_clicked == "btn1":
            print("btn1")
        elif btn_clicked == "btn2":
            print("btn2")
        elif btn_clicked == "btn3":
            print("btn3")
        elif btn_clicked == "btn4":
            print("btn4")
        elif btn_clicked == "btn4":
            print("btn4")
        elif btn_clicked == "btn5":
            print("btn5")
        elif btn_clicked == "btn6":
            print("btn6")
        elif btn_clicked == "btn7":
            print("btn7")
        elif btn_clicked == "btn0":
            print("btn0")

    def setLedState(self, toprow, led, active):
        """
        Sets the given LED state

        :param toprow: top (True) or bottom (False) row
        :type toprow: bool
        :param led: LED number, between 0 and 7
        :type led: int
        :param active: state
        :type active: bool
        """
        ledkey = "topLed" if toprow else "bottomLed"
        ledkey += str(led)

        self.led_states[ledkey] = active

    def setRowState(self, toprow, octet):
        """
        Sets the given LED row state
        :param toprow: top (True) or bottom (False) row
        :type toprow: bool
        :param octet: decimal value of the byte
        :type octet: int
        """
        ledkey = "topLed" if toprow else "bottomLed"

        index = 7  # Starts at 7 and ends at 0

        for value in bin(octet)[2:].rjust(8, '0'):
            self.led_states[ledkey + str(index)] = value == '1'
            index -= 1
