from simulation.core.controller import Controller
from simulation.simpy_adapter.composition_root import CompositionRoot
from experiments_utils.jobs_generator import *
from experiments_utils.runner import Runner
from simulation.simpy_adapter.graphs_builders import *
from experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *


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


testGraphBuilder = FullGraphBuilder()
experimentCollector = ExperimentCollector(Logger())
analyzer = ExperimentAnalyzer(experimentCollector)

JOBS_NUMBER = 10
NODES_NUMBER = 15

for iterations in range(100, 1600, 100):
    experiment = AverageJobCostExperiment(JOBS_NUMBER, NODES_NUMBER, iterations, testGraphBuilder)
    Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=20)


plotSeries(analyzer.analyze('cost', ['mean']), 'Average scheduling cost', 'cost', 'iterations')
plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions', 'collisions', 'iterations')
