# Author: Thomas Lécluse
# Licence GPL-3

#
# Dynamic digirule's model getter
#

from importlib import import_module


class DigiruleInfo:

    def __init__(self, digirule_model):
        """
        This class provides methods to get the information associated to the currently used digirule

        :param digirule_model: Digirule model
        :type digirule_model: str
        """

        self.digi_model = import_module("src.digirules.digirule_description_" + digirule_model)

    def get_img_name(self):
        """
        Retrieves the IMG file name given the Digirule currently used

        :return: Digirule's img file name
        :rtype: str
        """
        return self.digi_model.IMG_NAME

    def get_scale_offset(self):
        """
        Retrieves the Offset scale to apply to the painter given the Digirule currently used

        :return: Digirule's associated offset scale
        :rtype: tuple
        """
        return self.digi_model.OFFSET_SCALE

    def get_buttons_width(self):
        """
        Retrieves the buttons width to use given the Digirule currently used

        :return: Digirule's associated buttons width
        :rtype: int
        """
        return self.digi_model.BUTTONS_WIDTH

    def get_buttons_positions_dic(self):
        """
        Retrieves the position dictionary of the buttons given the Digirule currently used

        :return: Digirule buttons' positions
        :rtype: dict
        """
        return self.digi_model.buttons_positions

    def get_special_buttons_rects_dic(self):
        """
        Retrives the rectangles dictionary for non-square buttons

        :return: Digirule special buttons' positions
        :rtype: dict
        """
        return self.digi_model.special_buttons_rectangles

    def get_led_positions_dic(self):
        """
        Retrieves the position dictionary of the LEDs given the Digirule currently used

        :return: Digirule LEDs' positions
        :rtype: dict
        """
        return self.digi_model.led_positions
