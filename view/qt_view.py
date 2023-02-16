import sys
from PyQt6.QtWidgets import QApplication
from view.mainframe import Mainframe
from fakes.fake_events_hub import *
from collections import namedtuple

MapSize = namedtuple("MapSize", "x y width height")

mapSize = MapSize(x=0, y=0, width=23, height=46.5)
testObjectsNum = 1
businessRules = FakeBusinessRules(range(0, testObjectsNum), 1, mapSize)

app = QApplication([])

window = Mainframe(businessRules)
window.showMaximized()

sys.exit(app.exec())