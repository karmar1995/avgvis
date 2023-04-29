from simulation.core.controller import Controller
from simulation.simpy_adapter.composition_root import CompositionRoot
from experiments_utils.jobs_generator import *
from experiments_utils.runner import Runner
from simulation.simpy_adapter.graphs_builders import *
from experiments_utils.plotters.boxplot import boxplot


class AverageJobCostExperiment:

    def __init__(self, jobsNumber, nodesNumber, iterations, topologyBuilder):
        self.__systemBuilder = SystemBuilder()
        self.__simpyRoot = CompositionRoot(1000000)
        self.__jobsNumber = jobsNumber
        self.__nodesNumber = nodesNumber
        self.__iterations = iterations
        topologyBuilder.setNodesNumber(nodesNumber).build(self.__systemBuilder, self.__simpyRoot.simulation.env)

    def run(self, statisticsCollector):
        controller = Controller(system=self.__systemBuilder.system(), agentsFactory=self.__simpyRoot.simpyAgentsFactory,
                                simulation=self.__simpyRoot.simulation)
        testJobs = generateRandomJobs(jobsNumber=self.__jobsNumber, nodesNumber=self.__nodesNumber)
        pathsPerJobId = controller.coordinatePaths(jobsDict=testJobs, iterations=self.__iterations)

        for jobId in pathsPerJobId:
            path = pathsPerJobId[jobId]
            statisticsCollector.collect('cost', path.cost)
            statisticsCollector.collect('collisions', path.collisions)


class Log2StdOutObserver:
    def __init__(self):
        pass

    def onPartialResult(self, result):
        print("Partial result: {} ".format(result))


class StatisticsCollector:
    def __init__(self):
        self.__statistics = dict()

    def collect(self, statistic, value):
        if statistic not in self.__statistics:
            self.__statistics[statistic] = list()
        self.__statistics[statistic].append(value)

    def avg(self, statistic):
        return sum(self.__statistics[statistic]) / len(self.__statistics[statistic])

    def statistic(self, statistic):
        return self.__statistics[statistic][-1]


class RetriesCollector:
    def __init__(self, partialResultsObserver):
        self.__statisticsCollectors = list()
        self.__partialResultsObserver = partialResultsObserver

    def statisticsCollector(self):
        self.__statisticsCollectors.append(StatisticsCollector())
        return self.__statisticsCollectors[-1]

    def statistics(self, statistic):
        res = list()
        for statisticsCollector in self.__statisticsCollectors:
            res.append(statisticsCollector.statistic(statistic))
        return res

    def onRetryFinished(self):
        self.__partialResultsObserver.onPartialResult(self.__statisticsCollectors[-1].statistic('cost'))


observer = Log2StdOutObserver()
testGraphBuilder = FullGraphBuilder()

costsDict = dict()
collisionsDict = dict()

JOBS_NUMBER = 40
NODES_NUMBER = 10

for iterations in range(100, 200, 50):
    retriesCollector = RetriesCollector(observer)
    experiment = AverageJobCostExperiment(JOBS_NUMBER, NODES_NUMBER, iterations, testGraphBuilder)
    experimentRunner = Runner(experiment, retriesCollector)
    experimentRunner.run(times=4)
    costsDict[iterations] = retriesCollector.statistics('cost')
    collisionsDict[iterations] = retriesCollector.statistics('collisions')


boxplot(costsDict, 'Average scheduling cost', 'cost', 'iterations')
boxplot(collisionsDict, 'Average collisions', 'collisions', 'iterations')