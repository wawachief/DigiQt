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

# All the positions for buttons
buttons_positions = {
    (25, 140): "d_btn7",
    (71, 140): "d_btn6",
    (117, 140): "d_btn5",
    (165, 140): "d_btn4",
    (212, 139): "d_btn3",
    (260, 139): "d_btn2",
    (306, 139): "d_btn1",
    (353, 139): "d_btn0",
    (818, 68): "btn_goto",
    (876, 68): "btn_store",
    (876, 135): "btn_next",
    (818, 135): "btn_prev",
    (740, 115): "btn_run",
    (946, 133): "btn_save",
    (947, 67): "btn_load",
}

# Rectangle-shape buttons and larger buttons
special_buttons_rectangles = {
    (597, 103, 643, 150): "btn_ram",
    (510, 118, 550, 135): "btn_clear",
    (395, 40, 470, 120): "btn_power"
}

# Rows of LEDs
led_positions = {
    (27, 62): "topLed7",
    (73, 62): "topLed6",
    (120, 62): "topLed5",
    (167, 62): "topLed4",
    (213, 62): "topLed3",
    (261, 62): "topLed2",
    (308, 62): "topLed1",
    (355, 62): "topLed0",
    (27, 99): "bottomLed7",
    (73, 99): "bottomLed6",
    (120, 99): "bottomLed5",
    (167, 99): "bottomLed4",
    (213, 99): "bottomLed3",
    (261, 99): "bottomLed2",
    (308, 99): "bottomLed1",
    (355, 99): "bottomLed0",
    (771, 148): "stopLed",
    (707, 148): "runLed"
}
