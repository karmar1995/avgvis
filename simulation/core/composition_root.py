from simulation.core.system_builder import SystemBuilder
from simulation.core.controller import Controller


class CompositionRoot:
    def __init__(self):
        self.__systemBuilder = SystemBuilder()
        self.__controller = None

    def initialize(self, dependencies, topologyBuilder):
        topologyBuilder.build(self.__systemBuilder)
        self.__controller = Controller(system=self.__systemBuilder.system(),
                                       agentsFactory=dependencies['agentsFactory'],
                                       simulation=dependencies['simulation']
                                       )

    def controller(self):
        return self.__controller