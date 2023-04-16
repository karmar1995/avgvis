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
        while i < len(path):
            self.currentNode = self.traverser.node(path[i-1])
            self.nextNode = self.traverser.node(path[i])
            with self.currentNode.executor.request() as request:
                yield request
                yield self.env.process(self.currentNode.process())
            yield self.env.timeout(self.traverser.transitionTime(path[i-1], path[i]))
            i += 1
        with self.nextNode.executor.request() as request:
            yield request
            yield self.env.process(self.currentNode.process())

        self.currentNode = None
        self.nextNode = None

        endTime = self.env.now
        self.traverser.feedback(path, endTime - startTime)
