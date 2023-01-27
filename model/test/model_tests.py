import unittest
from fake_view import FakeView
from fake_event_source import FakeEventsSource
from fake_error_sink import FakeErrorSink
from model.composition_root import CompositionRoot, InitData, MapData


class ModelTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.view = FakeView()
        self.eventsSource = FakeEventsSource()
        self.errorSink = FakeErrorSink()
        self.compositionRoot = CompositionRoot(self.view)
        self.compositionRoot.addErrorListener(self.errorSink)
        mapData = MapData(10, 20, 1000, 2000)
        initData = InitData(mapData)
        self.compositionRoot.initialize(initData)
        self.compositionRoot.eventsHub().addEventsSource(self.eventsSource)

    def test_WhenAgvObjectIsRegisteredAndUpdatedViewRendersIt(self):
        self.eventsSource.registerAgvObject(12)
        self.assertEqual(len(self.view.knownObjects), 1)

        self.eventsSource.updateObjectPosition(12, 100, 213)
        lastRenderedObject = self.view.lastRenderedObject()
        self.assertEqual(lastRenderedObject.getObjectId(), 12)
        self.assertEqual(lastRenderedObject.getX(), 100)
        self.assertEqual(lastRenderedObject.getY(), 213)

        self.eventsSource.updateObjectPosition(12, 200, 413)
        lastRenderedObject = self.view.lastRenderedObject()
        self.assertEqual(lastRenderedObject.getObjectId(), 12)
        self.assertEqual(lastRenderedObject.getX(), 200)
        self.assertEqual(lastRenderedObject.getY(), 413)

        self.eventsSource.updateObjectRotation(12, 120)
        lastRenderedObject = self.view.lastRenderedObject()
        self.assertEqual(lastRenderedObject.getObjectId(), 12)
        self.assertEqual(lastRenderedObject.getRotation(), 120)

    def test_AgvObjectCanUpdateBatteryState(self):
        self.eventsSource.registerAgvObject(12)
        self.assertEqual(self.view.lastRenderedObject().getBattery(), '10%')
        self.eventsSource.updateObjectProperties(12, { 'battery': '20%' })
        self.assertEqual(self.view.lastRenderedObject().getBattery(), '20%')

    def test_IncorrectPositionEventIsIgnoredAndErrorIsLogged(self):
        self.eventsSource.registerAgvObject(12)
        self.assertEqual(len(self.view.knownObjects), 1)

        self.eventsSource.updateObjectPosition(12, 100, 213)
        self.assertEqual(self.view.lastRenderedObject().getObjectId(), 12)
        self.assertEqual(self.view.lastRenderedObject().getX(), 100)
        self.assertEqual(self.view.lastRenderedObject().getY(), 213)

        self.eventsSource.updateObjectPosition(12, 1, 2)
        self.assertEqual(len(self.errorSink.errors), 1)
        self.assertEqual(self.view.lastRenderedObject().getObjectId(), 12)
        self.assertEqual(self.view.lastRenderedObject().getX(), 100)
        self.assertEqual(self.view.lastRenderedObject().getY(), 213)

        self.eventsSource.updateObjectPosition(12, 1000000000, 200000000)
        self.assertEqual(len(self.errorSink.errors), 2)
        self.assertEqual(self.view.lastRenderedObject().getObjectId(), 12)
        self.assertEqual(self.view.lastRenderedObject().getX(), 100)
        self.assertEqual(self.view.lastRenderedObject().getY(), 213)

        self.eventsSource.updateObjectPosition(12, -3, -2)
        self.assertEqual(len(self.errorSink.errors), 3)
        self.assertEqual(self.view.lastRenderedObject().getObjectId(), 12)
        self.assertEqual(self.view.lastRenderedObject().getX(), 100)
        self.assertEqual(self.view.lastRenderedObject().getY(), 213)

    def test_WhenAgvObjectIsRegisteredTwiceOnlyOneInstanceExistsAndErrorIsLogged(self):
        self.eventsSource.registerAgvObject(12)
        self.eventsSource.registerAgvObject(12)
        self.assertEqual(len(self.view.knownObjects), 1)
        self.assertEqual(len(self.errorSink.errors), 1)

    def test_WhenObjectIsUnregisteredTwiceNoneInstanceExistsAndErrorIsLogged(self):
        self.eventsSource.registerAgvObject(12)
        self.assertEqual(len(self.view.knownObjects), 1)
        self.eventsSource.unregisterObject(12)
        self.eventsSource.unregisterObject(12)
        self.assertEqual(len(self.view.knownObjects), 0)

    def test_AgvObjectGetsCorrectBoundingRect(self):
        self.eventsSource.registerAgvObject(12)
        self.eventsSource.updateObjectPosition(12, 200, 413)
        lastRenderedObject = self.view.lastRenderedObject()
        boundingRect = lastRenderedObject.getBoundingRect()
        topLeft = boundingRect[0]
        bottomRight = boundingRect[1]
        self.assertEqual(topLeft[0], 200)
        self.assertEqual(topLeft[1], 413)
        self.assertEqual(bottomRight[0], 204)
        self.assertEqual(bottomRight[1], 416)

    def tearDown(self):
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
