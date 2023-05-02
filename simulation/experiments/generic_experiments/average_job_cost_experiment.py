from simulation.core.composition_root import CompositionRoot as CoreRoot
from simulation.simpy_adapter.composition_root import CompositionRoot as SimpyRoot
from simulation.experiments_utils.jobs_generator import *
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.test_graphs_builders import *
from simulation.experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *


class AverageJobCostExperiment:

    def __init__(self, jobsNumber, nodesNumber, iterations):
        self.__coreRoot = CoreRoot()
        self.__simpyRoot = SimpyRoot(1000000)
        self.__jobsNumber = jobsNumber
        self.__nodesNumber = nodesNumber
        self.__iterations = iterations
        self.__testGraphBuilder = FullGraphBuilder(self.__simpyRoot.simulation.env).setNodesNumber(nodesNumber)

    def run(self, statisticsCollector):
        dependencies = {'agentsFactory': self.__simpyRoot.simpyAgentsFactory, 'simulation': self.__simpyRoot.simulation}
        initInfo = {'executorsNumber': self.__jobsNumber}
        self.__coreRoot.initialize(dependencies, self.__testGraphBuilder, initInfo)
        testJobs = generateRandomJobs(jobsNumber=self.__jobsNumber, nodesNumber=self.__nodesNumber)

        pathsPerJobId = self.__coreRoot.pathsController().coordinatePaths(jobsDict=testJobs, iterations=self.__iterations)

        for jobId in pathsPerJobId:
            path = pathsPerJobId[jobId]
            statisticsCollector.collect('cost', path.cost)
            statisticsCollector.collect('collisions', path.collisions)


experimentCollector = ExperimentCollector(Logger())
analyzer = ExperimentAnalyzer(experimentCollector)

JOBS_NUMBER = 10
NODES_NUMBER = 15

for iterations in range(100, 600, 100):
    experiment = AverageJobCostExperiment(JOBS_NUMBER, NODES_NUMBER, iterations)
    Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=10)


plotSeries(analyzer.analyze('cost', ['mean']), 'Average scheduling cost', 'cost', 'iterations')
plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions', 'collisions', 'iterations')
