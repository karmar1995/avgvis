from dataclasses import dataclass
from simulation.core.agents_factory import AgentsFactory
from simulation.core.tasks_queue import TasksQueue, TasksQueueView
from simulation.core.traverser_base import TraverserStatistics


@dataclass
class OptimizationResult:
    queueView: TasksQueueView
    statistics: TraverserStatistics


class QueueOptimizer:
    def __init__(self, system, agentsFactory : AgentsFactory, simulation, traverserFactory, queue: TasksQueue, agentsNumber):
        self.__system = system
        self.__agentsFactory = agentsFactory
        self.__simulation = simulation
        self.__traverser = traverserFactory(system)
        self.__queue = queue
        self.__agentsNumber = agentsNumber

    def optimizeQueue(self, iterations) -> OptimizationResult:
        self.__queue.onOptimizationStart()

        tasksToOptimize = self.__queue.tasksList()
        self.__traverser.assignSequence(sequence=tasksToOptimize)
        for i in range(0, iterations):
            agents = list()
            for agentId in range(0, self.__agentsNumber):
                agent = self.__createAgent(self.__traverser)
                agents.append(agent)

            while not self.__traverser.finished():
                for agent in agents:
                    agent.start()
                self.__simulation.run()

            self.__traverser.nextIteration()

        self.__queue.onOptimizationFinished(self.__traverser.sequence(), self.__traverser.cost())
        return OptimizationResult(self.__queue.queueView(), self.__traverser.statistics())

    def __createAgent(self, traverser):
        return self.__agentsFactory.createAgent({'traverser': traverser})