from experiments.tasks_scheduling_experiment import RandomTasksScheduling
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.plotters.boxplot import plotSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *
from simulation.experiments_utils.tasks_generator import generateTasksQueue


experimentCollector = ExperimentCollector(Logger())
analyzer = ExperimentAnalyzer(experimentCollector)

TASKS_NUMBER = 100
EXECUTORS_NUMBER = 20
NODES_NUMBER = 15

tasksQueue = generateTasksQueue(TASKS_NUMBER, NODES_NUMBER)

for iterations in range(100, 1600, 100):
    experiment = RandomTasksScheduling(tasksQueue, EXECUTORS_NUMBER, NODES_NUMBER, iterations)
    Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=20)


plotSeries(analyzer.analyze('cost', ['mean']), 'Average scheduling cost', 'cost', 'iterations')
plotSeries(analyzer.analyze('collisions', ['mean']), 'Average collisions', 'collisions', 'iterations')
