from agv_type_definitions import *


class AgvManipulator:
    def __init__(self, node, index):
        self.__node = node
        self.__index = index

    def setX(self, newValue):
        self.__getProxy(x_signal).set_value(newValue)

    def __getProxy(self, signal):
        return self.__node.get_child("{}:{}".format(self.__index, signal))