# This file's purpose is to describe the Digirule 2A model elements position

IMG_NAME = "DR_2A.png"  # Image file name
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
    (213, 140): "d_btn3",
    (262, 140): "d_btn2",
    (310, 140): "d_btn1",
    (360, 140): "d_btn0",
    (432, 70): "btn_goto",
    (490, 70): "btn_save",
    (490, 136): "btn_next",
    (432, 136): "btn_prev",
    (793, 136): "btn_run",
    (904, 136): "btn_eepromsave",
    (904, 70): "btn_load",
}

# Rectangle-shape buttons and larger buttons
special_buttons_rectangles = {
    (559, 108, 605, 155): "btn_ram",
    (670, 118, 703, 128): "btn_clear",
    (970, 50, 1050, 130): "btn_power"
}

# Rows of LEDs
led_positions = {
    (28, 64): "topLed7",
    (74, 64): "topLed6",
    (120, 64): "topLed5",
    (168, 64): "topLed4",
    (216, 64): "topLed3",
    (264, 64): "topLed2",
    (312, 64): "topLed1",
    (360, 64): "topLed0",
    (28, 100): "bottomLed7",
    (74, 100): "bottomLed6",
    (120, 100): "bottomLed5",
    (168, 100): "bottomLed4",
    (216, 100): "bottomLed3",
    (264, 100): "bottomLed2",
    (312, 100): "bottomLed1",
    (360, 100): "bottomLed0"
}
