# Author: Thomas Lécluse
# Licence GPL-3

#
# Style resources getter
#

def get_stylesheet(file, ext=".qss", path="src/view/style/"):
    """
    Gets the qss content into a string

    :param file: file name (without extension)
    :param ext: extension (not mandatory)
    :param path: path (not mandatory)
    :return:
    """
    f = open(path + file + ext, "r")
    txt = f.read()
    f.close()

    return txt
