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
        self.compositionRoot = CompositionRoot()
        mapData = MapData(10, 20, 1000, 2000)
        initData = InitData(self.view, self.errorSink, mapData)
        initData.addEventSource(self.eventsSource)
        self.compositionRoot.initialize(initData)

    def test_WhenAgvObjectIsRegisteredAndUpdatedViewRendersIt(self):
        self.eventsSource.registerAgvObject(12)
        self.assertNotEqual(len(self.view.knownObjects), 0)

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


    def tearDown(self):
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
