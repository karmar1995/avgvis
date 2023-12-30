from simulation.simpy_adapter.timeout_utils import *


class Agent:

    def __init__(self, env, number, traverser):
        self.env = env
        self.number = number
        self.traverser = traverser
        self.currentNode = None
        self.nextNode = None

    def start(self):
        self.env.process(self.__run())

    def __run(self):
        startTime = self.env.now

        path = self.traverser.path()
        i = 1
        collisions = 0
        timeInQueue = 0
        timeInPenalty = 0
        while i < len(path):
            self.currentNode = self.traverser.node(path[i-1])
            self.nextNode = self.traverser.node(path[i])

            enqueueTime = self.env.now
            self.currentNode.onEnqueue()
            with self.currentNode.executor.request() as request:
                yield request
                yield self.env.process(self.currentNode.process())

            self.currentNode.onDeque()
            dequeTime = self.env.now
            timeInQueue += (dequeTime - enqueueTime)
            self.currentNode.addAgentLeavingNode(self)
            agents = self.nextNode.getAgentsLeavingNode()
            transitionTime = self.traverser.transitionTime(path[i-1], path[i])
            penaltyTime = transitionTime * 0.25

            for agentId in agents:
                if agents[agentId].nextNode.index == self.currentNode.index:
                    collisions += 1
                    timeInPenalty += penaltyTime
                    yield self.env.timeout(transitionTimeout(penaltyTime))
                    break

            yield self.env.timeout(transitionTimeout(transitionTime))
            self.currentNode.removeAgentLeavingNode(self)

            i += 1
        self.currentNode = self.traverser.node(path[i - 1])
        with self.nextNode.executor.request() as request:
            yield request
            yield self.env.process(self.currentNode.process())

        self.currentNode = None
        self.nextNode = None

        endTime = self.env.now
        pathCost = endTime - startTime
        self.traverser.feedback(path, pathCost, collisions, timeInQueue, timeInPenalty)
