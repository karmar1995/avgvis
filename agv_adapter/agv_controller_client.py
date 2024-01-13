from tcp_utils.client_utils import TcpClient
from agv_adapter.data_structures import *


class REQUESTS:
    GET_AGVS_IDS = 0
    GET_AGV_STATUS = 1
    GO_TO_POINTS = 2


class AgvControllerClient:
    def __init__(self, agvControllerIp, agvControllerPort):
        self.__tcpClient = TcpClient(agvControllerIp, agvControllerPort)

    def requestAgvsIds(self):
        self.__tcpClient.sendDataToServer(self.__prepareRequest(REQUESTS.GET_AGV_STATUS, ""))
        return agvIdsFromJson(self.__tcpClient.readDataFromServer())

    def requestAgvStatus(self, agvId):
        self.__tcpClient.sendDataToServer(self.__prepareRequest(REQUESTS.GET_AGV_STATUS, agvId))
        return agvStatusFromJson(self.__tcpClient.readDataFromServer())

    def requestGoToPoints(self, points):
        self.__tcpClient.sendDataToServer(self.__prepareRequest(REQUESTS.GO_TO_POINTS, points))

    def __prepareRequest(self, requestId, payload):
        return requestId