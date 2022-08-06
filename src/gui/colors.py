from PySide6.QtGui import QColor

background_color = 'EEF0F5'
background_darker_color = 'D9DFE7'


def hex2QColor(c):
    r = int(c[0:2], 16)
    g = int(c[2:4], 16)
    b = int(c[4:6], 16)

    return QColor(r, g, b)


BACKGROUND = hex2QColor(background_color)
BACKGROUND_DARKER = hex2QColor(background_darker_color)
