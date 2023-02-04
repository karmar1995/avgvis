import sys
from business_rules.composition_root import CompositionRoot, DataInterfaces
from data_access.opc_data_access import OpcClientFactory
from configuration.configuration_in_memory import ConfigurationInJson
from PyQt6.QtWidgets import QApplication
from view.mainframe import Mainframe

opcDataAccess = OpcClientFactory()
configurationDataAccess = ConfigurationInJson()
dataInterfaces = DataInterfaces(opcDataAccess=opcDataAccess, configurationDataAccess=configurationDataAccess)
businessRulesRoot = CompositionRoot(dataInterfaces=dataInterfaces)

app = QApplication([])

mainframe = Mainframe(businessRulesRoot)
mainframe.show()
sys.exit(app.exec())