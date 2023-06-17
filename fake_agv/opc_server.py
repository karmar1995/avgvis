import opcua
from agv_type_definitions import *
from agv_manipulator import AgvManipulator
import threading, time


class OpcServer:
    def __init__(self):
        self.__agvType = None
        self.__server = opcua.Server()
        self.__index = self.__server.register_namespace("opc.tcp://127.0.0.1:4840/fake_agv/")
        self.__createAgvType()
        self.__agvsFolder = self.__server.get_objects_node().add_folder(self.__index, "AGVs")
        self.__objects = dict()
        self.__addObject("AGV1")
        self.__addObject("AGV2")
        self.__addObject("AGV3")

    def __addObject(self, name):
        self.__objects[name] = self.__agvsFolder.add_object(self.__index, name, self.__agvType)

    def __createAgvType(self):
        self.__agvType = self.__server.nodes.base_object_type.add_object_type(self.__index, "AGV")
        self.__agvType.add_variable(self.__index, x_signal, 1.0).set_modelling_rule(True)
        self.__agvType.add_variable(self.__index, y_signal, 1.5).set_modelling_rule(True)
        self.__agvType.add_variable(self.__index, heading_signal, 1.0).set_modelling_rule(True)
        self.__agvType.add_property(self.__index, source_node_signal, "A").set_modelling_rule(True)
        self.__agvType.add_property(self.__index, destination_node_signal, "B").set_modelling_rule(True)
        self.__agvType.add_property(self.__index, battery_signal, "10%").set_modelling_rule(True)
        self.__agvType.add_property(self.__index, state_signal, "Idle").set_modelling_rule(True)

    def start(self):
        self.__server.start()

    def getAgvManipulator(self, objectName):
        return AgvManipulator(self.__objects[objectName], self.__index)


class AgvTest:
    def __init__(self, agvManipulator):
        self.__stopped = False
        self.__agv = agvManipulator
        self.__thread = threading.Thread(target=self.__run)
        self.__x = 2.0
        self.__thread.daemon = True
        self.__thread.start()

    def __run(self):
        while not self.__stopped:
            time.sleep(1)
            self.__x += 0.5
            print("***********************************: Setting X to: {}".format(self.__x))
            self.__agv.setX(self.__x)


server = OpcServer()
agvtest = AgvTest(server.getAgvManipulator("AGV1"))
server.start()

