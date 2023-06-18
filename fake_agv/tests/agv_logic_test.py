import unittest
from fake_agv.agv_logic import *


def createTestNodes():
    nodes = list()
    nodes.append(Node(id="0", x=1, y=1))
    nodes.append(Node(id="1", x=1, y=21))
    nodes.append(Node(id="2", x=21, y=1))
    nodes.append(Node(id="3", x=21, y=21))
    return nodes


class FakeObserver:
    def __init__(self):
        self.xHistory = list()
        self.yHistory = list()

    def onAgvStateChanged(self, agv):
        self.xHistory.append(agv.x())
        self.yHistory.append(agv.y())


class FakeAgvLogicTest(unittest.TestCase):

    def test_goToNodeVertically(self):
        agv = AgvLogic(createTestNodes())
        observer = FakeObserver()
        agv.addObserver(observer)

        agv.goToNode("1")
        watchdog = 100
        while len(observer.xHistory) < 10:
            time.sleep(0.1)
            watchdog -= 1
            if watchdog == 0:
                self.fail("Watchdog causing failure")

        self.assertEqual(len(observer.xHistory), 10)
        self.assertEqual(len(observer.yHistory), 10)
        for x in observer.xHistory:
            self.assertEqual(x, 1.0)

        currentY = 1.0
        for y in observer.yHistory:
            currentY += 2.0
            self.assertEqual(y, currentY)

    def test_goToNodeHorizontally(self):
        agv = AgvLogic(createTestNodes())
        observer = FakeObserver()
        agv.addObserver(observer)

        agv.goToNode("2")
        watchdog = 100
        while len(observer.xHistory) < 10:
            time.sleep(0.1)
            watchdog -= 1
            if watchdog == 0:
                self.fail("Watchdog causing failure")

        self.assertEqual(len(observer.xHistory), 10)
        self.assertEqual(len(observer.yHistory), 10)
        for y in observer.yHistory:
            self.assertEqual(y, 1.0)

        currentX = 1.0
        for x in observer.xHistory:
            currentX += 2.0
            self.assertEqual(x, currentX)

    def test_goToNodeDiagonally(self):
        agv = AgvLogic(createTestNodes())
        observer = FakeObserver()
        agv.addObserver(observer)

        agv.goToNode("3")
        watchdog = 100
        while len(observer.xHistory) < 10:
            time.sleep(0.1)
            watchdog -= 1
            if watchdog == 0:
                self.fail("Watchdog causing failure")

        self.assertEqual(len(observer.xHistory), 10)
        self.assertEqual(len(observer.yHistory), 10)

        currentY = 1.0
        for y in observer.yHistory:
            currentY += 2.0
            self.assertEqual(y, currentY)

        currentX = 1.0
        for x in observer.xHistory:
            currentX += 2.0
            self.assertEqual(x, currentX)


if __name__ == '__main__':
    unittest.main()
