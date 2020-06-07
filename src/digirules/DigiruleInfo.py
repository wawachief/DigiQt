# This class provides methods to get the information associated to the currently used digirule

import src.digirules.Digirule2A as DR_2A


class DigiruleInfo:

    @staticmethod
    def getImgName(digirule_model):
        """
        Retrieves the IMG file name given the Digirule currently used

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return: Digirule's img file name
        :rtype: str
        """
        if digirule_model == "2A":
            return DR_2A.IMG_NAME

    @staticmethod
    def getScaleOffset(digirule_model):
        """
        Retrieves the Offset scale to apply to the painter given the Digirule currently used

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return: Digirule's associated offset scale
        :rtype: tuple
        """
        if digirule_model == "2A":
            return DR_2A.OFFSET_SCALE

    @staticmethod
    def getButtonsWidth(digirule_model):
        """
        Retrieves the buttons width to use given the Digirule currently used

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return: Digirule's associated buttons width
        :rtype: int
        """
        if digirule_model == "2A":
            return DR_2A.BUTTONS_WIDTH

    @staticmethod
    def getButtonsPositionsDico(digirule_model):
        """
        Retrieves the position dictionary of the buttons given the Digirule currently used

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return: Digirule buttons' positions
        :rtype: dict
        """
        if digirule_model == "2A":
            return DR_2A.buttons_positions

    @staticmethod
    def getTopLedPositionsDico(digirule_model):
        """
        Retrieves the position dictionary of the first row of LEDs given the Digirule currently used

        :param digirule_model: Digirule model
        :type digirule_model: str
        :return: Digirule 1st LEDs' row positions
        :rtype: dict
        """
        if digirule_model == "2A":
            return DR_2A.top_led_positions
