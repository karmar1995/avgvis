import time, threading

from tcp_utils.client_utils import TcpClient
from agv_adapter.data_structures import *
from agv_adapter.request_builder import RequestBuilder


class REQUESTS:
    GET_AGVS_IDS = 1
    GET_AGV_STATUS = 2
    GO_TO_POINTS = 3


class AgvControllerClient:
    def __init__(self, agvControllerIp, agvControllerPort):
        self.__tcpClient = TcpClient(agvControllerIp, agvControllerPort)
        self.__lock = threading.Lock()

    def requestAgvsIds(self):
        with self.__lock:
            request = RequestBuilder().startRequest(REQUESTS.GET_AGVS_IDS).finalize()
            self.__tcpClient.sendDataToServer(request.encode('ASCII'))
            response = self.__waitForResponse()
            return agvIdsFromJson(response.decode('ASCII'))

    def requestAgvStatus(self, agvId):
        with self.__lock:
            request = RequestBuilder().startRequest(REQUESTS.GET_AGV_STATUS).withAgvId(agvId).finalize()
            self.__tcpClient.sendDataToServer(request.encode('ASCII'))
            response = self.__waitForResponse()
            return agvStatusFromJson(response.decode('ASCII'))

    def requestGoToPoints(self, agvId, points):
        with self.__lock:
            request = RequestBuilder().startRequest(REQUESTS.GO_TO_POINTS).withAgvId(agvId).withPoints(points).finalize()
            self.__tcpClient.sendDataToServer(request.encode('ASCII'))
            self.__waitForResponse() # response not used for now

    def __waitForResponse(self):
        response = self.__tcpClient.readDataFromServer()
        while response is None:
            time.sleep(0.1)
            response = self.__tcpClient.readDataFromServer()
        return response
