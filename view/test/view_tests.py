import unittest
from view.fakes.fake_ui.fake_app import FakeApp
from view.fakes.fake_ui.updates_sequence_generator import UpdatesSequenceGenerator
from collections import namedtuple
MapSize = namedtuple("MapSize", "x y width height")


def defaultMapSize():
    return MapSize(x=0, y=0, width=50, height=100)


def defaultViewSize():
    return 200, 400


def createFakeApp(mapSize, viewSize, updatesGenerator):
    fakeApp = FakeApp(mapSize, updatesGenerator)
    fakeApp.mainframe.setViewSize(viewSize[0], viewSize[1])
    fakeApp.mainframe.initialize()
    return fakeApp


class ViewTests(unittest.TestCase):
    def test_viewLogicCalculatesPositionOfObjectOnMap(self):
        updatesGenerator = UpdatesSequenceGenerator()
        fakeApp = createFakeApp(defaultMapSize(), defaultViewSize(), updatesGenerator)

        updatesGenerator.updateObjectPosition(0, 1, 2)
        objectWidget = fakeApp.mainframe.mapWidget.objectWidget(0)
        self.assertEqual(objectWidget.x(), 4)
        self.assertEqual(objectWidget.y(), 392)
        updatesGenerator.updateObjectPosition(0, 10, 20)
        self.assertEqual(objectWidget.x(), 40)
        self.assertEqual(objectWidget.y(), 320)

    def test_incorrectPositionDoesNotUpdateObject(self):
        updatesGenerator = UpdatesSequenceGenerator()
        fakeApp = createFakeApp(defaultMapSize(), defaultViewSize(), updatesGenerator)

        updatesGenerator.updateObjectPosition(0, 10, 20)
        objectWidget = fakeApp.mainframe.mapWidget.objectWidget(0)
        self.assertEqual(objectWidget.x(), 40)
        self.assertEqual(objectWidget.y(), 320)

        updatesGenerator.updateObjectPosition(0, 10, -2)
        self.assertEqual(objectWidget.x(), 40)
        self.assertEqual(objectWidget.y(), 320)

        updatesGenerator.updateObjectPosition(0, -1, 20)
        self.assertEqual(objectWidget.x(), 40)
        self.assertEqual(objectWidget.y(), 320)

        updatesGenerator.updateObjectPosition(0, -1, -2)
        self.assertEqual(objectWidget.x(), 40)
        self.assertEqual(objectWidget.y(), 320)

if __name__ == '__main__':
    unittest.main()
