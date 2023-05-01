import os
from simulation.experiments.generic_experiments.tasks_scheduling_experiment import RandomTasksScheduling
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *
from simulation.experiments_utils.tasks_generator import generateTasksQueue
from simulation.experiments_utils.csv_writer import CsvWriter
from simulation.experiments_utils.test_graphs_builders import TreeGraphBuilder


def run(connectionsNumber, switchesNumber, hostsPerSwitch, graphBuilderClass):
    experimentCollector = ExperimentCollector(Logger())
    analyzer = ExperimentAnalyzer(experimentCollector)

    graphBuilder = graphBuilderClass(switchesNumber, hostsPerSwitch)
    tasksQueue = generateTasksQueue(connectionsNumber, switchesNumber + hostsPerSwitch)

    executorsNumber = int(connectionsNumber / 10)

    for iterations in range(100, 1100, 100):
        experiment = RandomTasksScheduling(tasksQueue, executorsNumber, iterations, graphBuilder)
        Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=10)

    legend = {
        'TCP connections number': connectionsNumber,
        'Switches Number': switchesNumber
    }

    resultsDir = '/home/kmarszal/Documents/dev/avgvis/simulation/experiments/results/tcp_random_task_scheduling'
    csvWriter = CsvWriter(resultsDir, analyzer)
    csvWriter.write('cost', 'iterations', legend)
    csvWriter.write('collisions', 'iterations', legend)
    plotSeries(analyzer.analyze('cost', ['mean', 'min', 'max']), 'Average scheduling cost', 'cost', 'iterations', os.path.join(resultsDir, "cost.png"))
    plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions', 'collisions', 'iterations', os.path.join(resultsDir, "collisions.png"))


run(connectionsNumber=100, switchesNumber=15, hostsPerSwitch=5, graphBuilderClass=TreeGraphBuilder)