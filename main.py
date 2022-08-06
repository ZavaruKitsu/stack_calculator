import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from src import MathWindow

app = QApplication()
font = QFont('Montserrat', 14)
app.setFont(font)

app.setStyle('fusion')

math_window = MathWindow(app)

math_window.show()

sys.exit(app.exec())
