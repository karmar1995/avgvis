from business_rules.composition_root import CompositionRoot, ViewInterfaces, DataInterfaces
from data_access.opc_data_access import OpcClientFactory
from configuration.configuration_in_memory import ConfigurationInJson
from view.console_view import ConsoleModelView, ConsoleUserView

modelView = ConsoleModelView()
userView = ConsoleUserView()
viewInterfaces = ViewInterfaces(modelView=modelView, userView=userView)

opcDataAccess = OpcClientFactory()
configurationDataAccess = ConfigurationInJson()
dataInterfaces = DataInterfaces(opcDataAccess=opcDataAccess, configurationDataAccess=configurationDataAccess)

businessRulesRoot = CompositionRoot(viewInterfaces=viewInterfaces, dataInterfaces=dataInterfaces)
businessRulesRoot.initialize()
businessRulesRoot.startApp()