import simpy, copy
from simulation.simpy_adapter.timeout_utils import *


class Node:
    def __init__(self, env, serviceTime, index):
        self.env = env
        self.executor = simpy.Resource(env, 1)
        self.serviceTime = serviceTime
        self.index = index
        self.__agentsLeaving = dict()

    def process(self):
        yield self.env.timeout(timeoutFor(self.serviceTime))

    def addAgentLeavingNode(self, agent):
        self.__agentsLeaving[id(agent)] = agent

    def removeAgentLeavingNode(self, agent):
        del self.__agentsLeaving[id(agent)]

    def getAgentsLeavingNode(self):
        return self.__agentsLeaving.copy()

