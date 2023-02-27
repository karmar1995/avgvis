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
        configPath = self.__view.askForConfigPath()

        if not self.__persistency.fileExists(configPath):
            self.__persistency.setFilename(configPath)
            self.__view.driveConfigCreation(self.__persistency)

        try:
            self.__persistency.read(configPath)
            mapData = self.__getMapData()
            modelInitData = model_root.InitData(
                model_root.MapData(x=mapData[0], y=mapData[1], width=mapData[2], height=mapData[3]))

            if not modelRoot.initialize(modelInitData):
                return False
            if not opcRoot.initialize():
                return False

            self.__registerObjectsFromPersistency()
            return True

        except:
            self.__view.onIncorrectConfig(configPath)
            return False

    def addObjectFactory(self, typeName, factory):
        self.__objectFactoriesByType[typeName] = factory

    def __getMapData(self):
        return self.__persistency.mapData()

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
