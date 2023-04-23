import copy
import random
import time
import simpy
from simulation.simpy_adapter.node import Node
from simulation.core.system_builder import *
from simulation.core.controller import Controller
from simulation.simpy_adapter.simpy_agents_factory import SimpyAgentsFactory


def buildTestGraph(builder):
    for i in range(0, 10):
        builder.addVertex(Vertex(node=Node(env=env, serviceTime=i*100)))

    for i in range(0, 10):
        for j in range(0, 10):
            builder.addEdge(Edge(source=i, target=j, weight=10 * i + j))


class EnvironmentWrapper:
    def __init__(self, environment, timeout):
        self.__env = environment
        self.__timeout = timeout
        self.__curTime = 0

    def run(self):
        self.__curTime += self.__timeout
        self.__env.run(until=self.__curTime)


env = simpy.Environment()
simulation = EnvironmentWrapper(environment=env, timeout=10000000)
simpyAgentsFactory = SimpyAgentsFactory(env=env)

systemBuilder = SystemBuilder()
buildTestGraph(systemBuilder)

permutations = list()
for i in range(0, 10):
    permutations.append(i)

jobsNumber = 50
testJobs = dict()

for i in range(0, jobsNumber):
    random.shuffle(permutations)
    testJobs[str(i)] = copy.deepcopy(permutations)

for i in range(0, 50):
    controller = Controller(system=systemBuilder.system(), agentsFactory=simpyAgentsFactory, simulation=simulation)
    res = controller.coordinatePaths(testJobs)

    avgCost = 0

    for jobId in res:
        avgCost += res[jobId].cost

    avgCost /= len(res)

    print("Average cost: {}".format(avgCost))