from visobject import *


class AgvObjectData:
    def __init__(self, visObjectData, battery):
        self.visObjectData = visObjectData
        self.battery = battery


class AgvObject(VisObject):
    def __init__(self, avgObjectData):
        super().__init__(avgObjectData.visObjectData)
        self.battery = avgObjectData.battery

