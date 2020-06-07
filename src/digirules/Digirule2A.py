# This file's purpose is to describe the Digirule 2A model elements position

IMG_NAME = "DR_2A.png"  # Image file name
BUTTONS_WIDTH = 30  # Push buttons width

# The drawing painter in which is drawn buttons and LEDs needs to be rescaled.
# Those values where calculated with a point (1px wide) placed at (wrong) coordinates (1000, 500), and real position
# prompt on click, to get the offset.
OFFSET_SCALE = (1000/399, 500/200)

# All the positions for buttons
buttons_positions = {
    (25, 140): "btn7",
    (71, 140): "btn6",
    (117, 140): "btn5",
    (165, 140): "btn4",
    (213, 140): "btn3",
    (262, 140): "btn2",
    (310, 140): "btn1",
    (360, 140): "btn0",
}

# First row of LEDs
top_led_positions = {
    (28, 64): "topLed7",
    (74, 64): "topLed6",
    (120, 64): "topLed5",
    (168, 64): "topLed4",
    (216, 64): "topLed3",
    (264, 64): "topLed2",
    (312, 64): "topLed1",
    (360, 64): "topLed0",
}
