import model.composition_root as model_root
import opc_adapter.composition_root as opc_root


class UseCaseController:
    def __init__(self, objectIdsGenerator, view, persistency):
        self.__objectFactoriesByType = dict()
        self.__objectIdsGenerator = objectIdsGenerator
        self.__view = view
        self.__persistency = persistency

    def driveInitialization(self, modelRoot, opcRoot):
        self.addObjectFactory("OPC", opcRoot.objectsFactory())
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
        self.__objectFactoriesByType[registerData['sourceType']].createObject(objectId, registerData).registerObject()

    def __registerObjectsFromPersistency(self):
        registerDataList = self.__persistency.objectsList()
        for registerData in registerDataList:
            objectId = self.__objectIdsGenerator.generateId()
            self.__objectFactoriesByType[registerData['sourceType']].createObject(objectId,
                                                                                  registerData).registerObject()
