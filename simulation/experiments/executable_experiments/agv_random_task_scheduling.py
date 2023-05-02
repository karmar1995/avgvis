import os
from simulation.experiments.generic_experiments.tasks_scheduling_experiment import RandomTasksScheduling
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *
from simulation.experiments_utils.tasks_generator import generateTasksQueue
from simulation.experiments_utils.csv_writer import CsvWriter
from simulation.experiments_utils.test_graphs_builders import LongServiceTimeFullGraphBuilder, ShortServiceTimeFullGraphBuilder


def run(tasksNumber, agvsNumber, stationsNumber, graphBuilderClass, subdirectory):
    experimentCollector = ExperimentCollector(Logger())
    analyzer = ExperimentAnalyzer(experimentCollector)

    tasksQueue = generateTasksQueue(tasksNumber, stationsNumber)
    graphBuilder = graphBuilderClass(stationsNumber)

    for iterations in range(100, 2100, 100):
        experiment = RandomTasksScheduling(tasksQueue, agvsNumber, iterations, graphBuilder)
        Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=20)

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
    plotSeries(analyzer.analyze('cost', ['mean']), 'Average scheduling cost', 'cost', 'iterations', os.path.join(resultsDir, "cost.png"))
    plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions', 'collisions', 'iterations', os.path.join(resultsDir, "collisions.png"))
    plotSeries(analyzer.analyze('time', ['mean']), 'Calculation time', 'time', 'iterations', os.path.join(resultsDir, "time.png"))


run(tasksNumber=100, agvsNumber=20, stationsNumber=15, graphBuilderClass=LongServiceTimeFullGraphBuilder, subdirectory='long_service_few_agvs')
run(tasksNumber=300, agvsNumber=60, stationsNumber=10, graphBuilderClass=ShortServiceTimeFullGraphBuilder, subdirectory='short_service_many_agvs')