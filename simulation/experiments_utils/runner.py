class Runner:
    def __init__(self, experiment, observer):
        self.__experiment = experiment
        self.__observer = observer

    def run(self, times):
        res = list()
        for i in range(0, times):
            singleResult = self.__experiment.run()
            self.__observer.onPartialResult(singleResult)
            res.append(singleResult)
        return res

