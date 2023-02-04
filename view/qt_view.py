import sys
from PyQt6.QtWidgets import QApplication
from view.mainframe import Mainframe
from fakes.fake_events_hub import *
from collections import namedtuple

MapSize = namedtuple("MapSize", "x y width height")

mapSize = MapSize(x=5, y=5, width=100, height=100)
testObjectsNum = 10
businessRules = FakeBusinessRules(range(0, testObjectsNum), 2, mapSize)

app = QApplication([])

window = Mainframe(businessRules)
window.show()
sys.exit(app.exec())