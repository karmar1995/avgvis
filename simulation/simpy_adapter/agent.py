from simulation.simpy_adapter.timeout_utils import *


class Agent:

    def __init__(self, env, number, traverser, startingNode = None):
        self.env = env
        self.number = number
        self.traverser = traverser
        self.currentNode = startingNode
        self.nextNode = None

    def start(self):
        self.env.process(self.__run())


    def __run(self):
        startTime = self.env.now

        tasks = self.traverser.tasks()
        i = 1
        while i <= len(tasks):
            task = tasks[i-1]

#            if self.currentNode is not None:
#                self.__performTransitionBetweenNodes(self.currentNode, task.source())

            self.currentNode = self.traverser.node(task.source())
            self.nextNode = self.traverser.node(task.destination())

            currentNodeEnter = self.env.now
            self.currentNode.onEnqueue()
            with self.currentNode.executor.request() as request:
                yield request
                yield self.env.process(self.currentNode.startTask(task.taskNumber()))
            self.currentNode.onDeque()
            currentNodeLeaving = self.env.now
            currentNodeTime = currentNodeLeaving - currentNodeEnter

            self.currentNode.addAgentLeavingNode(self)
            agents = self.nextNode.getAgentsLeavingNode()
            penaltyTime = 200

            for agentId in agents:
                if agents[agentId].nextNode.index == self.currentNode.index:
                    yield self.env.timeout(transitionTimeout(penaltyTime))
                    break

            self.currentNode.removeAgentLeavingNode(self)
            # end of - collisions

            beforeTransit = self.env.now
            path = self.traverser.pathBetweenNodes(self.currentNode, self.nextNode)
            i = 1
            while i < len(path):
                transitionTime = self.traverser.transitionTime(path[i - 1], path[i])
                yield self.env.timeout(transitionTimeout(transitionTime))
                i += 1
            afterTransit = self.env.now
            timeInTransit = afterTransit - beforeTransit

            nextNodeEnterTime = self.env.now
            self.nextNode.onEnqueue()
            with self.nextNode.executor.request() as request:
                yield request
                yield self.env.process(self.nextNode.startTask(task.taskNumber()))
            self.nextNode.onDeque()
            nextNodeLeaveTime = self.env.now
            self.nextNodeLeaving = nextNodeLeaveTime - nextNodeEnterTime

            self.currentNode = self.nextNode

            i += 1

        self.currentNode = None
        self.nextNode = None

        endTime = self.env.now
        tasksCost = endTime - startTime
        self.traverser.feedback(tasksCost, 0, 0, 0, 0)
