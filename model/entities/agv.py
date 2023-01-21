from model.entities.visobject import *


class AgvObjectData:
    def __init__(self, visObjectData, battery):
        self.visObjectData = visObjectData
        self.battery = battery


class AgvObject(VisObject):
    def __init__(self, agvObjectData):
        super().__init__(agvObjectData.visObjectData)
        self.battery = agvObjectData.battery

