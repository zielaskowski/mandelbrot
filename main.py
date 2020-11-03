import sys
from PyQt5.QtWidgets import QApplication
from gui import GUIMandelbrot


app = QApplication([])
view = GUIMandelbrot()
view.show()
sys.exit(app.exec())



