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
        collisions = 0
        timeInQueue = 0
        timeInPenalty = 0
        timeInTransition = 0
        while i <= len(tasks):
            task = tasks[i-1]

            if self.currentNode is not None and self.currentNode.index != task.source():
                # collisions
                sourceNode = self.traverser.node(task.source())
                self.currentNode.addAgentLeavingNode(self)
                agents = sourceNode.getAgentsLeavingNode()
                penaltyTime = 200

                for agentId in agents:
                    if agents[agentId].nextNode.index == self.currentNode.index:
                        beforePenalty = self.env.now
                        yield self.env.timeout(transitionTimeout(penaltyTime))
                        collisions += 1
                        timeInPenalty += (self.env.now - beforePenalty)
                        break

                self.currentNode.removeAgentLeavingNode(self)
                # end of - collisions

                beforeTransit = self.env.now
                path = self.traverser.pathBetweenNodes(self.currentNode, sourceNode)
                i = 1
                while i < len(path):
                    transitionTime = self.traverser.transitionTime(path[i - 1], path[i])
                    yield self.env.timeout(transitionTimeout(transitionTime))
                    i += 1
                afterTransit = self.env.now
                timeInTransition += afterTransit - beforeTransit

            self.currentNode = self.traverser.node(task.source())
            self.nextNode = self.traverser.node(task.destination())

            currentNodeEnter = self.env.now
            self.currentNode.onEnqueue()
            with self.currentNode.executor.request() as request:
                yield request
                yield self.env.process(self.currentNode.startTask(task.taskNumber()))
            self.currentNode.onDeque()
            currentNodeLeaving = self.env.now
            timeInQueue += currentNodeLeaving - currentNodeEnter

            # collisions
            self.currentNode.addAgentLeavingNode(self)
            agents = self.nextNode.getAgentsLeavingNode()
            penaltyTime = 200

            for agentId in agents:
                if agents[agentId].nextNode.index == self.currentNode.index:
                    beforePenalty = self.env.now
                    yield self.env.timeout(transitionTimeout(penaltyTime))
                    collisions += 1
                    timeInPenalty += (self.env.now - beforePenalty)
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
            timeInTransition += afterTransit - beforeTransit

            nextNodeEnterTime = self.env.now
            self.nextNode.onEnqueue()
            with self.nextNode.executor.request() as request:
                yield request
                yield self.env.process(self.nextNode.startTask(task.taskNumber()))
            self.nextNode.onDeque()
            nextNodeLeaveTime = self.env.now
            timeInQueue += (nextNodeLeaveTime - nextNodeEnterTime)

            self.currentNode = self.nextNode

            i += 1

        endTime = self.env.now
        tasksCost = endTime - startTime
        self.traverser.feedback(tasksCost, collisions, timeInQueue, timeInPenalty, timeInTransition)
