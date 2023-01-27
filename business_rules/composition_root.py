import model.composition_root as model_root
import opc_adapter.composition_root as opc_root
from business_rules.usecase_controller import UseCaseController
from collections import namedtuple

ViewInterfaces = namedtuple('ViewInterfaces', 'modelView userView')
DataInterfaces = namedtuple('DataInterfaces', 'opcDataAccess configurationDataAccess')


class CompositionRoot:
    def __init__(self, viewInterfaces, dataInterfaces):
        self.modelRoot = model_root.CompositionRoot(viewInterfaces.modelView)

        self.opcRoot = opc_root.CompositionRoot(self.modelRoot.eventsHub(), dataInterfaces.opcDataAccess)

        self.useCaseController = UseCaseController(self.modelRoot.objectsIdsGenerator(),
                                                   viewInterfaces.userView,
                                                   dataInterfaces.configurationDataAccess)

        self.useCaseController.addObjectFactory("OPC", self.opcRoot.objectsFactory())


    def initialize(self):
        self.useCaseController.driveInitialization(self.modelRoot, self.opcRoot)
