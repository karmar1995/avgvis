import sys
from PyQt6.QtWidgets import QApplication
from view.mainframe import Mainframe

app = QApplication([])

window = Mainframe()
window.show()
sys.exit(app.exec())