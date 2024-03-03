from dataclasses import dataclass
from simulation.core.agents_factory import AgentsFactory
from simulation.core.tasks_queue import TasksQueue, TasksQueueView
from simulation.core.traverser_base import TraverserStatistics


@dataclass
class OptimizationResult:
    queueView: TasksQueueView
    statistics: TraverserStatistics


class QueueOptimizer:
    def __init__(self, system, agentsFactory : AgentsFactory, simulation, traverserFactory, queue: TasksQueue, executorsManager):
        self.__system = system
        self.__agentsFactory = agentsFactory
        self.__simulation = simulation
        self.__traverserFactory = traverserFactory
        self.__traverser = None
        self.__queue = queue
        self.__executorsManager = executorsManager

    def optimizeQueue(self, iterations) -> OptimizationResult:
        executorsNumber = self.__executorsManager.onlineExecutorsNumber()
        self.__traverser = self.__traverserFactory(self.__system)
        if executorsNumber > 0:
            self.__queue.onOptimizationStart()
            tasksToOptimize = self.__queue.tasksList()
            oldSize = len(tasksToOptimize)
            if len(tasksToOptimize) > 1:
                self.__traverser.assignSequence(sequence=tasksToOptimize)
                for i in range(0, iterations):
                    agents = list()
                    for agentId in range(0, self.__executorsManager.onlineExecutorsNumber()):
                        agent = self.__createAgent(self.__traverser)
                        agents.append(agent)

                    while not self.__traverser.finished():
                        for agent in agents:
                            agent.start()
                        self.__simulation.run()

                    self.__traverser.nextIteration()

                optimizedSequence = self.__traverser.sequence()
                newSize = len(optimizedSequence)
                if oldSize != newSize:
                    raise Exception("Queue corrupted by optimizer, old: {}, new: {}!".format(oldSize, newSize))
                self.__queue.onOptimizationFeedback(optimizedSequence, self.__traverser.cost())
            self.__queue.onOptimizationFinished()
        return OptimizationResult(self.__queue.queueView(), self.__traverser.statistics())

    def queue(self):
        return self.__queue

    def __createAgent(self, traverser):
        return self.__agentsFactory.createAgent({'traverser': traverser})
