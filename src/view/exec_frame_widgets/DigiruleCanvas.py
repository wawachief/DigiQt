# Author: Thomas Lécluse
# License GPL-3

#
# Widget of execution frame
#

from PySide2.QtWidgets import QLabel, QApplication
from PySide2.QtGui import QPixmap, QPainter, QColor, QPen, QMatrix
from PySide2.QtCore import QPoint, QRect, Qt

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
        "stopLed": True,
        "runLed": False,
        "pin1Led": 0,
        "pin0Led": 0
    }

    def __init__(self, sig_status, window_width, digirule_model, config):
        """
        Canvas in witch is drawn the Digirule as well as its buttons

        :param parent_frame: Main application frame (the execution frame)
        :type parent_frame: ExecutionFrame
        :param sig_status: signal that is connected to the statusbar
        :type sig_status: Signal
        :param digirule_model: Default digirule model
        :type digirule_model: str
        :param window_width: application window width, to use as width for this label as well
        :type window_width: int
        """
        QLabel.__init__(self)

        self.config = config
        self.sig_status = sig_status
        self.sig_PIN_in = None

        self.setFixedSize(window_width, 204)  # 1/4 of the original size
        self.setScaledContents(True)

        self.digirule_changed(digirule_model)

    def digirule_changed(self, digirule_model):
        """
        Updates the digirule model used and then calls the redraw method to update the background image and buttons

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return:
        """
        self.digirule = DigiruleInfo(digirule_model)
        self.redraw()

        self.sig_status.emit("Digirule model switched to " + digirule_model)

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
        pen.setColor(QColor(0, 0, 0, 0))  # Buttons color 
        painter.setPen(pen)

        # Buttons
        for btn in self.digirule.get_buttons_positions_dic():
            painter.drawPoint(QPoint(btn[0], btn[1]))

        pen.setWidth(2)
        painter.setPen(pen)

        for btn in self.digirule.get_special_buttons_rects_dic():
            # Draw rectangle given the top-left and bottom-right corners coordinates
            painter.drawRect(self._build_rect(btn))

    def _build_rect(self, coordinates):
        """
        Utility method for building a rectangle given its top-left and bottom-right corners coordinates

        :param coordinates: coordinates (x0, y0, x1, y1) of the rectangle where:
        - x0 is top-left x coordinate
        - y0 is top-left y coordinate
        - x1 is bottom-right x coordinate
        - y1 is bottom-right y coordinate
        :type coordinates: tuple
        :return: associated rectangle
        :rtype: QRect
        """
        return QRect(QPoint(coordinates[0], coordinates[1]), QPoint(coordinates[2], coordinates[3]))

    def paintEvent(self, event):
        """
        Handles the LEDs redraw process

        :param event:
        """
        super().paintEvent(event)

        top_color = self.config.get('colors', 'led_top_row')
        bottom_color = self.config.get('colors', 'led_bottom_row')

        # LEDs
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(10)
        pinColor=["black", "red", "grey", "yellow"]

        led_dico = self.digirule.get_led_positions_dic()
        for led in led_dico:
            if led_dico[led] == "pin0Led" or led_dico[led] == "pin1Led":
                # pin Leds can be of 4 different colors
                pen.setColor(QColor(pinColor[self.led_states[led_dico[led]]]))
            elif self.led_states[led_dico[led]]:  # LED active color
                pen.setColor(QColor(top_color if "top" in led_dico[led] else bottom_color))
            else:  # LED inactive color
                pen.setColor(QColor("black"))
            painter.setPen(pen)
            painter.drawPoint(QPoint(led[0], led[1]))

    def is_ctrl_pressed(self):
        """
        :return: True if "ctrl" keyboard key is held down
        """
        return QApplication.keyboardModifiers() == Qt.ControlModifier

    def mouseReleaseEvent(self, event):
        """
        Intercepts the click release on the canvas and calls the method associated to the clicked button, if there is one
        """
        # print(event.x(), event.y())

        w = self.digirule.get_buttons_width() / 2  # Accepted offset to click position
        btns_dico = self.digirule.get_buttons_positions_dic()
        for btn in btns_dico:
            if btn[0] - w <= event.x() <= btn[0] + w and btn[1] - w <= event.y() <= btn[1] + w:
                btn_name = btns_dico[btn]

                # Particular case for the 'd' buttons, we call the same method with the btn number
                if 'd_' == btn_name[0:2]:
                    self.on_d(int(btn_name[-1]), False)
                else:  # Generic process, calling the method given the full button name
                    eval("self.on_" + btn_name)()

                return  # No need to continue once found

        special_btns_dico = self.digirule.get_special_buttons_rects_dic()
        for btn in special_btns_dico:
            if self._build_rect(btn).contains(event.x(), event.y()):
                eval("self.on_" + special_btns_dico[btn])()

                return  # No need to continue once found

    def mousePressEvent(self, event):
        """
        Intercepts the click press on the canvas and calls the method associated to the clicked button. This is only
        applied to dx buttons
        """
        w = self.digirule.get_buttons_width() / 2  # Accepted offset to click position

        btns_dico = self.digirule.get_buttons_positions_dic()
        for btn in btns_dico:
            if btn[0] - w <= event.x() <= btn[0] + w and btn[1] - w <= event.y() <= btn[1] + w:
                btn_name = btns_dico[btn]

                if 'd_' == btn_name[0:2]:  # dx buttons
                    self.on_d(int(btn_name[-1]), True)
                    return  # No need to continue once found

    def set_led_state(self, top_row, led, active, do_repaint=True):
        """
        Sets the given LED state

        :param top_row: top (True) or bottom (False) row
        :type top_row: bool
        :param led: LED number, between 0 and 7
        :type led: int
        :param active: state
        :type active: bool
        :param do_repaint: repaint after setting
        :type do_repaint: bool
        """
        led_key = "topLed" if top_row else "bottomLed"
        led_key += str(led)

        self.led_states[led_key] = active

        if do_repaint:
            self.repaint()  # Forces the label to repaint

    def set_running_leds(self, is_running, do_repaint=True):
        """
        Sets both the stop and run LEDs given the specified running state

        :param is_running: True if cpu running
        :type is_running: bool
        :param do_repaint: repaint after setting
        :type do_repaint: bool
        """
        self.led_states["stopLed"] = not is_running
        self.led_states["runLed"] = is_running

        if do_repaint:
            self.repaint()  # Forces the label to repaint
    
    def set_pin_leds(self, pin, mode, do_repaint=True):
        """
        Sets pins LEDs given the specified running state

        :param pin: 0 or 1 for pin0 or pin1
        :type pin: int
        :param mode: int 
             0 : LOW
             1 : HIGH
             2 : INPUT LOW
             3 : INPUT HIGH
        :type mode: int
        :param do_repaint: repaint after setting
        :type do_repaint: bool
        """
        if pin == 0:
            self.led_states["pin0Led"] = mode
        else:
            self.led_states["pin1Led"] = mode

        if do_repaint:
            self.repaint()  # Forces the label to repaint

    def set_row_state(self, top_row, octet, do_repaint=True):
        """
        Sets the given LED row state
        :param top_row: top (True) or bottom (False) row
        :type top_row: bool
        :param octet: decimal value of the byte
        :type octet: int
        :param do_repaint: repaint after setting
        :type do_repaint: bool
        """
        led_key = "topLed" if top_row else "bottomLed"

        index = 7  # Starts at 7 and ends at 0

        for value in bin(octet)[2:].rjust(8, '0'):
            self.led_states[led_key + str(index)] = value == '1'
            index -= 1

        if do_repaint:
            self.repaint()  # Forces the label to repaint

    # --- Buttons callbacks ---

    def on_d(self, btn, is_pressed):
        """
        Callback for press on a 'd' button.

        :param btn: button number
        :type btn: int
        :param is_pressed: True if the button was pressed, False if released
        :type is_pressed: bool
        """
        pass

    def on_btn_goto(self):
        pass

    def on_btn_store(self):
        pass

    def on_btn_prev(self):
       pass

    def on_btn_next(self):
        pass

    def on_btn_run(self):
        pass

    def on_btn_save(self):
        pass

    def on_btn_load(self):
        pass

    def on_btn_ram(self):
        pass

    def on_btn_clear(self):
        pass

    def on_btn_power(self):
        pass

    def on_btn_pin0(self):
        if self.led_states["pin0Led"]>=2:
            # pindir is input
            self.sig_PIN_in.emit(0)

    def on_btn_pin1(self):
        if self.led_states["pin1Led"]>=2:
            # pindir is input
            self.sig_PIN_in.emit(1)
