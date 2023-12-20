import os
from simulation.experiments.generic_experiments.tasks_scheduling_experiment import RandomTasksScheduling
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *
from simulation.test_utils.tasks_generator import generateTasksQueue
from simulation.experiments_utils.csv_writer import CsvWriter


def run(tasksNumber, agvsNumber, stationsNumber, graphBuilderClass, subdirectory):
    experimentCollector = ExperimentCollector(Logger())
    analyzer = ExperimentAnalyzer(experimentCollector)

    tasksQueue = generateTasksQueue(tasksNumber, stationsNumber)
    graphBuilder = graphBuilderClass(stationsNumber)

    for iterations in range(1, 160, 10):
        experiment = RandomTasksScheduling(tasksQueue, agvsNumber, iterations, graphBuilder)
        Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=10)

    legend = {
        'Tasks number': tasksNumber,
        'AGVs number': agvsNumber,
        'Stations Number': stationsNumber
    }

    resultsDir = '/home/kmarszal/Documents/dev/avgvis/simulation/experiments/results/agv_random_task_scheduling/{}'.format(subdirectory)
    csvWriter = CsvWriter(resultsDir, analyzer)
    csvWriter.write('cost', 'iterations', legend)
    csvWriter.write('time', 'iterations', legend)
    csvWriter.write('collisions', 'iterations', legend)
    csvWriter.write('queueLength', 'iterations', legend)

    x_label = 'Calculation time [iterations]'
    plotSeries(analyzer.analyze('cost', ['mean']), 'Average job cost', 'Cost', x_label, os.path.join(resultsDir, "cost.png"))
    plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions during job execution', 'Collisions', x_label, os.path.join(resultsDir, "collisions.png"))
    plotSeries(analyzer.analyze('time', ['mean']), 'Calculation time', 'Time [s]', x_label, os.path.join(resultsDir, "time.png"))
    plotSeries(analyzer.analyze('queueLength', ['mean']), 'Average queue length', 'Queue length', x_label, os.path.join(resultsDir, "queueLength.png"))


