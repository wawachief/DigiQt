# This file's purpose is to contain all methods related to assets processing

from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize

ASSETS_PATH = "../assets/"  # We are located in src/, so we need to go to the parent directory before accessing assets/
ICON_SIZE = QSize(25, 25)

def get_icon(icon_name, extension=".png"):
    """
    Given the icon name, returns the associated QIcon
    :param icon_name: icon file name (without the extension)
    :type icon_name: str
    :param extension: icon extension (starting with a '.')
    :type extension: str
    :return: Icon object
    :rtype: QIcon
    """
    return QIcon(ASSETS_PATH + icon_name + extension)
