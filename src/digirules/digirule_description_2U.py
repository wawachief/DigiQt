# Author: Thomas Lécluse
# License GPL-3

#
# This file's purpose is to describe the Digirule 2U model elements position
#

IMG_NAME = "DR_2U.png"  # Image file name
BUTTONS_WIDTH = 30  # Push buttons width

# The drawing painter in which is drawn buttons and LEDs needs to be rescaled.
# Those values where calculated with a point (1px wide) placed at (wrong) coordinates (1000, 500), and real position
# prompt on click, to get the offset.
OFFSET_SCALE = (1000/399, 500/200)

# Test position with changing transparency line 93 in DigiruleCanvas.py
# All the positions for buttons
buttons_positions = {
    (28, 139): "d_btn7",
    (75, 139): "d_btn6",
    (122, 139): "d_btn5",
    (167, 139): "d_btn4",
    (214, 139): "d_btn3",
    (260, 139): "d_btn2",
    (305, 139): "d_btn1",
    (353, 139): "d_btn0",
    (816, 67): "btn_goto",
    (871, 67): "btn_store",
    (871, 131): "btn_next",
    (816, 131): "btn_prev",
    (738, 115): "btn_run",
    (940, 131): "btn_save",
    (940, 67): "btn_load",
}

# Rectangle-shape buttons and larger buttons
special_buttons_rectangles = {
    (597, 103, 643, 150): "btn_ram",
    (510, 118, 550, 135): "btn_clear",
    (395, 40, 473, 123): "btn_power",
    (1036, 142, 1046, 152): "btn_pin1",
    (1036, 155, 1046, 165): "btn_pin0"
}

# Rows of LEDs
led_positions = {
    (27, 62): "topLed7",
    (75, 62): "topLed6",
    (122, 62): "topLed5",
    (167, 62): "topLed4",
    (213, 62): "topLed3",
    (261, 62): "topLed2",
    (306, 62): "topLed1",
    (353, 62): "topLed0",
    (27, 98): "bottomLed7",
    (75, 98): "bottomLed6",
    (122, 98): "bottomLed5",
    (167, 98): "bottomLed4",
    (213, 98): "bottomLed3",
    (261, 98): "bottomLed2",
    (306, 98): "bottomLed1",
    (353, 98): "bottomLed0",
    (772, 147): "stopLed",
    (708, 147): "runLed",
    (1041, 147): "pin1Led",
    (1041, 160): "pin0Led"
}
