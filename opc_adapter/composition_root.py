from opc_adapter.opc_object import OpcObject


class OpcFactory:
    def __init__(self, dataAccess):
        self.__dataAccess = dataAccess

    def createObject(self, objectId, registerData):
        return OpcObject(objectId=objectId,
                         dataAccess=self.__dataAccess,
                         width=registerData['width'],
                         height=registerData['height'],
                         type=registerData['type'])


class CompositionRoot:
    def __init__(self, eventsHub, dataAccess):
        self.__eventsHub = eventsHub
        self.__objectsFactory = OpcFactory(dataAccess=dataAccess)

    def objectsFactory(self):
        return self.__objectsFactory
