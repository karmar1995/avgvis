import model.composition_root as model_root
import opc_adapter.composition_root as opc_root


class UseCaseController:
    def __init__(self, objectIdsGenerator, persistency):
        self.__objectFactoriesByType = dict()
        self.__objectIdsGenerator = objectIdsGenerator
        self.__view = None
        self.__persistency = persistency
        self.__errorSink = None

    def setView(self, view):
        self.__view = view

    def driveInitialization(self, modelRoot, opcRoot):
        self.__errorSink = modelRoot.errorSink()
        mapData = self.__getMapData()
        modelInitData = model_root.InitData(model_root.MapData(x=mapData[0], y=mapData[1], width=mapData[2], height=mapData[3]))

        if not modelRoot.initialize(modelInitData):
            pass #todo: handle error on model initialization
        if not opcRoot.initialize():
            pass #todo: handle error on opc adapter initialization

        self.__registerObjectsFromPersistency()

        if self.__startObjectsRegistration():
            self.__registerObject()

    def addObjectFactory(self, typeName, factory):
        self.__objectFactoriesByType[typeName] = factory

    def __getMapData(self):
        if self.__persistency.hasMapData():
            return self.__persistency.mapData()
        mapData = self.__view.requestMapData()
        self.__persistency.saveMapData(mapData)
        return mapData

    def __startObjectsRegistration(self):
        return self.__view.askForObjectsRegistration()

    def __registerObject(self):
        registerData = self.__view.requestObjectRegistration()
        objectId = self.__objectIdsGenerator.generateId()
        self.__objectFactoriesByType[registerData['sourceType']].createObject(objectId, registerData, self.__errorSink).registerObject()

    def __registerObjectsFromPersistency(self):
        registerDataList = self.__persistency.objectsList()
        for registerData in registerDataList:
            objectId = self.__objectIdsGenerator.generateId()
            visObject = self.__objectFactoriesByType[registerData['sourceType']].createObject(objectId,
                                                                                  registerData,
                                                                                  self.__errorSink)
            if visObject:
                visObject.registerObject()
            else:
                self.__errorSink.logError("Object not created: " + registerData['name'])
