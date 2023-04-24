from simulation.core.controller import Controller
from simulation.simpy_adapter.composition_root import CompositionRoot
from experiments_utils.jobs_generator import *
from experiments_utils.runner import Runner
from simulation.simpy_adapter.graphs_builders import *
from experiments_utils.plotters.boxplot import boxplot


class AverageJobCostExperiment:

    def __init__(self, jobsNumber, nodesNumber, iterations, topologyBuilder):
        self.__systemBuilder = SystemBuilder()
        self.__simpyRoot = CompositionRoot(100000)
        self.__jobsNumber = jobsNumber
        self.__nodesNumber = nodesNumber
        self.__iterations = iterations
        topologyBuilder.setNodesNumber(nodesNumber).build(self.__systemBuilder, self.__simpyRoot.simulation.env)

    def run(self):
        controller = Controller(system=self.__systemBuilder.system(), agentsFactory=self.__simpyRoot.simpyAgentsFactory,
                                simulation=self.__simpyRoot.simulation)
        testJobs = generateRandomJobs(jobsNumber=self.__jobsNumber, nodesNumber=self.__nodesNumber)
        pathsPerJobId = controller.coordinatePaths(jobsDict=testJobs, iterations=self.__iterations)

        costSum = 0
        for jobId in pathsPerJobId:
            costSum += pathsPerJobId[jobId].cost
        return costSum / len(pathsPerJobId)


class Log2StdOutObserver:
    def __init__(self):
        pass

    def onPartialResult(self, result):
        print("Partial result: {} ".format(result))


observer = Log2StdOutObserver()
testGraphBuilder = FullGraphBuilder()

resultsDict = dict()

JOBS_NUMBER = 50
NODES_NUMBER = 10

for iterations in range(300, 400, 50):
    experiment = AverageJobCostExperiment(JOBS_NUMBER, NODES_NUMBER, iterations, testGraphBuilder)
    experimentRunner = Runner(experiment, observer)
    resultsDict[iterations] = experimentRunner.run(times=50)


boxplot(resultsDict, 'Average scheduling cost', 'cost', 'iterations')