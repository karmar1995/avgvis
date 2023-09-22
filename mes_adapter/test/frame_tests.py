import unittest
from mes_adapter.test_utils.test_data import getTestFrame
from mes_adapter.frame_parser import MesFrameParser, MesFrameBuilder
from frames_utils.frame import DtlDateTime


class TasksSchedulingTests(unittest.TestCase):


    def test_parsesFrameCorrectly(self):
        parser = MesFrameParser()
        parsedFrame = parser.onFrameReceived(getTestFrame())
        self.assertEqual(parsedFrame.id, 5000)
        self.assertEqual(parsedFrame.beginning, 3950171)
        self.assertEqual(parsedFrame.data, 0)
        self.assertEqual(parsedFrame.empty, 0)
        self.assertEqual(parsedFrame.ending, 0)
        self.assertEqual(parsedFrame.length, 70)
        self.assertEqual(parsedFrame.number, 2600)
        self.assertEqual(parsedFrame.status, 1)
        self.assertEqual(parsedFrame.version, 1)
        dtlTimeStamp = parsedFrame.timestamp
        self.assertEqual(dtlTimeStamp.year, 1970)
        self.assertEqual(dtlTimeStamp.month, 1)
        self.assertEqual(dtlTimeStamp.day, 1)
        self.assertEqual(dtlTimeStamp.dayOfWeek, 5)
        self.assertEqual(dtlTimeStamp.hour, 0)
        self.assertEqual(dtlTimeStamp.minute, 0)
        self.assertEqual(dtlTimeStamp.second, 0)
        self.assertEqual(dtlTimeStamp.millisecond, 0)


    def test_buildsFrameCorrectly(self):
        mesFrameBuilder = MesFrameBuilder()
        mesFrameBuilder.setFieldValue('id', 5000).setFieldValue('beginning', 3950171).setFieldValue('data', 0).\
            setFieldValue('empty', 0).setFieldValue('ending', 0).setFieldValue('length', 70).setFieldValue('number', 2600).\
            setFieldValue('status', 1).setFieldValue('timestamp', DtlDateTime(2023, 9, 22, 5, 14, 0, 0, 12)).setFieldValue('version', 1)
        frameBytes = mesFrameBuilder.build()
        parsedFrame = MesFrameParser().onFrameReceived(frameBytes)
        self.assertEqual(parsedFrame.id, 5000)
        self.assertEqual(parsedFrame.beginning, 3950171)
        self.assertEqual(parsedFrame.data, 0)
        self.assertEqual(parsedFrame.empty, 0)
        self.assertEqual(parsedFrame.ending, 0)
        self.assertEqual(parsedFrame.length, 70)
        self.assertEqual(parsedFrame.number, 2600)
        self.assertEqual(parsedFrame.status, 1)
        self.assertEqual(parsedFrame.version, 1)
        dtlTimeStamp = parsedFrame.timestamp
        self.assertEqual(dtlTimeStamp.year, 2023)
        self.assertEqual(dtlTimeStamp.month, 9)
        self.assertEqual(dtlTimeStamp.day, 22)
        self.assertEqual(dtlTimeStamp.dayOfWeek, 5)
        self.assertEqual(dtlTimeStamp.hour, 14)
        self.assertEqual(dtlTimeStamp.minute, 0)
        self.assertEqual(dtlTimeStamp.second, 0)
        self.assertEqual(dtlTimeStamp.millisecond, 12)

    def test_buildBinarlyCompatibleFrame(self):
        mesFrameBuilder = MesFrameBuilder()
        mesFrameBuilder.setFieldValue('id', 5000).setFieldValue('beginning', 3950171).setFieldValue('data', 0).\
            setFieldValue('empty', 0).setFieldValue('ending', 0).setFieldValue('length', 70).setFieldValue('number', 2600).\
            setFieldValue('status', 1).setFieldValue('timestamp', DtlDateTime(1970, 1, 11, 5, 0, 0, 0, 0)).setFieldValue('version', 1)
        frameBytes = mesFrameBuilder.build()
        goldenBytes = getTestFrame()
        self.assertEqual(frameBytes, goldenBytes)