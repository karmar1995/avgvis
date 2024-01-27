import os
from simulation.experiments.generic_experiments.tasks_scheduling_experiment import RandomTasksScheduling
from simulation.experiments_utils.runner import Runner
from simulation.experiments_utils.plotters.boxplot import plotSeries, plotStackedSeries
from simulation.experiments_utils.logger import Logger
from simulation.experiments_utils.analytics.experiment_analyzer import *
from simulation.test_utils.tasks_generator import generateTasksQueue
from simulation.experiments_utils.csv_writer import CsvWriter


traversersLabels = {
    'geneticAlgorithm': 'Genetic Algorithm',
    'simulatedAnnealing': 'Simulated Annealing'
}


def prepateDataSeries(analyzer, traverserName, measure):
    seriesName = "{}_{}".format(traverserName, measure)
    return seriesName, analyzer.analyze(measure, ['mean'])['mean']


def prepareSeriesCollections(analyzer, traverserName, seriesCollection, labelsBySeriesName, measure):
    seriesName, series = prepateDataSeries(analyzer, traverserName, measure)
    seriesCollection[seriesName] = series
    labelsBySeriesName[seriesName] = traversersLabels[traverserName]


def run(tasksNumber, agvsNumber, stationsNumber, graphBuilderClass, subdirectory):
    traverserNames = [
        'simulatedAnnealing',
#        'geneticAlgorithm'
    ]
    tasksQueue = generateTasksQueue(tasksNumber, stationsNumber)
    graphBuilder = graphBuilderClass(stationsNumber)

    analyzerPerTraverser = dict()

    resultsDir = '/home/kmarszal/Documents/dev/avgvis/simulation/experiments/results_tmp/agv_random_task_scheduling/{}'.format(subdirectory)
    for traverserName in traverserNames:
        experimentCollector = ExperimentCollector(Logger())
        analyzerPerTraverser[traverserName] = ExperimentAnalyzer(experimentCollector)

        for iterations in range(10, 810, 20):
            experiment = RandomTasksScheduling(tasksQueue, agvsNumber, iterations, graphBuilder, traverserName)
            Runner(experiment, experimentCollector.getRetriesCollector(iterations)).run(times=5)

        legend = {
            'Tasks number': tasksNumber,
            'AGVs number': agvsNumber,
            'Stations Number': stationsNumber
        }

        csvWriter = CsvWriter(os.path.join(resultsDir, traverserName), analyzerPerTraverser[traverserName])
        csvWriter.write('cost', 'iterations', legend)
        csvWriter.write('time', 'iterations', legend)
#        csvWriter.write('collisions', 'iterations', legend)
#        csvWriter.write('queueLength', 'iterations', legend)
#        csvWriter.write('timeInQueue', 'iterations', legend)
#        csvWriter.write('timeInPenalty', 'iterations', legend)
#        csvWriter.write('timeInTransition', 'iterations', legend)
#        stackedSeriesDict = {'Time in queue': analyzerPerTraverser[traverserName].analyze('timeInQueue')['mean'],
#                             'Penalty time': analyzerPerTraverser[traverserName].analyze('timeInPenalty')['mean'],
#                             'Time in transit': analyzerPerTraverser[traverserName].analyze('timeInTransition')['mean']
#                             }
#        plotStackedSeries(stackedSeriesDict, 'Time constituents - {}'.format(traversersLabels[traverserName]), os.path.join(resultsDir, '{}_timeComposition.png'.format(traverserName)))

    costs = dict()
    collisions = dict()
    times = dict()
    queueLengths = dict()
    timeInQueue = dict()
    timeInPenalty = dict()
    timeInTransition = dict()

    labelsBySeriesName = dict()

    for traverserName in traverserNames:
        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, costs, labelsBySeriesName, 'cost')
#        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, collisions, labelsBySeriesName, 'collisions')
        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, times, labelsBySeriesName, 'time')
#        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, queueLengths, labelsBySeriesName, 'queueLength')
#        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, timeInQueue, labelsBySeriesName, 'timeInQueue')
#        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, timeInPenalty, labelsBySeriesName, 'timeInPenalty')
#        prepareSeriesCollections(analyzerPerTraverser[traverserName], traverserName, timeInTransition, labelsBySeriesName, 'timeInTransition')

    x_label = 'Calculation time [iterations]'
    plotSeries(costs, 'Average job cost', 'Cost', x_label, os.path.join(resultsDir, "cost.png"), labelsBySeriesName)
 #   plotSeries(collisions, 'Average collisions during job execution', 'Collisions', x_label, os.path.join(resultsDir, "collisions.png"), labelsBySeriesName)
#    plotSeries(times, 'Calculation time', 'Time [s]', x_label, os.path.join(resultsDir, "time.png"), labelsBySeriesName)
#    plotSeries(queueLengths, 'Average queue length', 'Queue length', x_label, os.path.join(resultsDir, "queueLength.png"), labelsBySeriesName)
#    plotSeries(timeInQueue, 'Average time in queue', 'Time in queue', x_label, os.path.join(resultsDir, "timeInQueue.png"), labelsBySeriesName)
#    plotSeries(timeInPenalty, 'Average time in penalty', 'Time in penalty', x_label, os.path.join(resultsDir, "timeInPenalty.png"), labelsBySeriesName)
#    plotSeries(timeInTransition, 'Average time in transit', 'Time in transit', x_label, os.path.join(resultsDir, "timeInTransit.png"), labelsBySeriesName)


