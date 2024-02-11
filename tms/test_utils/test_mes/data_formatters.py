import json
from mes_adapter.test_utils.test_data import getTestFrame


class DataFormatter:
    def __init__(self):
        pass

    def getDataToSend(self, orderId):
        raise NotImplementedError()


class BinaryFormatter(DataFormatter):
    def __init__(self):
        super().__init__()

    def getDataToSend(self, orderId):
        return getTestFrame(orderId)


class JsonFormatter(DataFormatter):
    def __init__(self):
        super().__init__()

    def getDataToSend(self, orderId):
        data = { 'productionOrderId': orderId }
        return bytes(json.dumps(data), encoding='ASCII')