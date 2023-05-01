import os
from simulation.experiments.generic_experiments.tasks_scheduling_experiment import RandomTasksScheduling
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *
from simulation.experiments_utils.tasks_generator import generateTasksQueue
from simulation.experiments_utils.csv_writer import CsvWriter


def run(tasksNumber, agvsNumber, stationsNumber, graphBuilderName):
    experimentCollector = ExperimentCollector(Logger())
    analyzer = ExperimentAnalyzer(experimentCollector)

    tasksQueue = generateTasksQueue(tasksNumber, stationsNumber)

    for iterations in range(100, 1600, 100):
        experiment = RandomTasksScheduling(tasksQueue, agvsNumber, stationsNumber, iterations, graphBuilderName)
        Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=20)

    legend = {
        'Tasks number': tasksNumber,
        'AGVs number': agvsNumber,
        'Stations Number': stationsNumber
    }

    resultsDir = '/home/kmarszal/Documents/dev/avgvis/simulation/experiments/results/agv_random_task_scheduling'
    csvWriter = CsvWriter(resultsDir, analyzer)
    csvWriter.write('cost', 'iterations', legend)
    csvWriter.write('collisions', 'iterations', legend)
    plotSeries(analyzer.analyze('cost', ['mean', 'min', 'max']), 'Average scheduling cost', 'cost', 'iterations', os.path.join(resultsDir, "cost.png"))
    plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions', 'collisions', 'iterations', os.path.join(resultsDir, "collisions.png"))


run(tasksNumber=100, agvsNumber=20, stationsNumber=15, graphBuilderName='FullGraphBuilder')