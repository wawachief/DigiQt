from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap, QPainter, QColor, QPen, QMatrix
from PySide2.QtCore import QPoint

from src.digirules.DigiruleInfo import DigiruleInfo
from random import randint

TOP_ROW_LED_COLOR = "red"
BOTTOM_ROW_LED_COLOR = "blue"


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

    def __init__(self, parent_frame, digirule_model="2A"):
        """
        Canvas in witch is drawn the Digirule as well as its buttons

        :param parent_frame: Main application frame (the execution frame)
        :type parent_frame: ExecutionFrame
        :param digirule_model: Default digirule model
        :type digirule_model: str
        """
        QLabel.__init__(self)

        self.exec_frame = parent_frame

        self.setFixedSize(1064, 204)  # 1/4 of the original size
        self.setScaledContents(True)

        self.digirule = DigiruleInfo(digirule_model)

        self.redraw()

    def digirule_changed(self, digirule_model):
        """
        Updates the digirule model used

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return:
        """
        self.digirule = DigiruleInfo(digirule_model)

    def redraw(self):
        """
        Re-draws the buttons. May be called as initialization method too.
        """
        # Pixmap that contains the painter and the DR
        canvas = QPixmap("assets/" + self.digirule.get_img_name())
        self.setPixmap(canvas)
        painter = QPainter(self.pixmap())  # Create a painter in which buttons and LEDs are drawn

        translate_matrix = QMatrix()
        offset_scale = self.digirule.get_scale_offset()
        translate_matrix.scale(offset_scale[0], offset_scale[1])
        painter.setMatrix(translate_matrix)

        # Drawing
        pen = QPen()
        pen.setWidth(self.digirule.get_buttons_width())
        pen.setColor(QColor(70, 70, 90, 150))  # Buttons color
        painter.setPen(pen)

        # Buttons
        buttons_dico = self.digirule.get_buttons_positions_dic()
        for btn in buttons_dico:
            painter.drawPoint(QPoint(btn[0], btn[1]))

    def paintEvent(self, event):
        """
        Handles the LEDs redraw process

        :param event:
        """
        super().paintEvent(event)

        # LEDs
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(10)

        led_dico = self.digirule.get_led_positions_dic()
        for led in led_dico:
            if self.led_states[led_dico[led]]:  # LED active color
                pen.setColor(QColor(TOP_ROW_LED_COLOR if "top" in led_dico[led] else BOTTOM_ROW_LED_COLOR))
            else:  # LED inactive color
                pen.setColor(QColor("black"))
            painter.setPen(pen)
            painter.drawPoint(QPoint(led[0], led[1]))

    def mouseReleaseEvent(self, event):
        """
        Intercepts the click on the canvas and calls the method associated to the clicked button, if there is one

        :param event:
        """
        print(event.x(), event.y())

        w = self.digirule.get_buttons_width() / 2  # Accepted offset to click position
        btns_dico = self.digirule.get_buttons_positions_dic()
        for btn in btns_dico:
            if btn[0] - w <= event.x() <= btn[0] + w and btn[1] - w <= event.y() <= btn[1] + w:
                btn_name = btns_dico[btn]
                if 'd_' in btn_name:  # Particular case for the 'd' buttons, we call the same method with the btn number
                    self.on_d(int(btn_name[-1]))
                else:  # Generic process, calling the method given the full button name
                    eval("self.on_" + btn_name)()

    def set_led_state(self, top_row, led, active):
        """
        Sets the given LED state

        :param top_row: top (True) or bottom (False) row
        :type top_row: bool
        :param led: LED number, between 0 and 7
        :type led: int
        :param active: state
        :type active: bool
        """
        led_key = "topLed" if top_row else "bottomLed"
        led_key += str(led)

        self.led_states[led_key] = active

        self.repaint()  # Forces the label to repaint

    def set_row_state(self, top_row, octet):
        """
        Sets the given LED row state
        :param top_row: top (True) or bottom (False) row
        :type top_row: bool
        :param octet: decimal value of the byte
        :type octet: int
        """
        led_key = "topLed" if top_row else "bottomLed"

        index = 7  # Starts at 7 and ends at 0

        for value in bin(octet)[2:].rjust(8, '0'):
            self.led_states[led_key + str(index)] = value == '1'
            index -= 1

        self.repaint()  # Forces the label to repaint

    # --- Buttons callbacks ---

    def on_d(self, btn):
        """
        Callback for press on a 'd' button.

        :param btn: button number
        :type btn: int
        """
        print("Click on btn-" + str(btn))
        self.set_row_state(randint(0, 1), randint(0, 255))
