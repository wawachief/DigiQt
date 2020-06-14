# Author: Thomas Lécluse
# License GPL-3

#
# Assets getter
#
import platform

from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize

ASSETS_PATH = "assets/"
ICON_SIZE = QSize(50, 50)


def get_icon(icon_name, internal_path="icons/", extension=".png"):
    """
    Given the icon name, returns the associated QIcon
    :param icon_name: icon file name (without the extension)
    :type icon_name: str
    :param extension: icon extension (starting with a '.')
    :type extension: str
    :param internal_path: path within the ASSETS_PATH
    :type internal_path: str
    :return: Icon object
    :rtype: QIcon
    """
    return QIcon(ASSETS_PATH + internal_path + icon_name + extension)


def get_font(conf):
    """
    Returns the config file's font given the current operating system

    :param conf: configuration file
    :return: font family
    :rtype: str
    """

    if platform.system() == "Linux":
        font_fam = conf.get('font', 'font_linux')
    elif platform.system() == "Darwin":  # Mac OSX
        font_fam = conf.get('font', 'font_osx')
    else:  # Windows
        font_fam = conf.get('font', 'font_win')
    return font_fam
