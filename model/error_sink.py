class ErrorSink:
    def __init__(self):
        self.listeners = dict()

    def addListener(self, listener):
        self.listeners[id(listener)] = listener

    def removeListener(self, listener):
        self.listeners.pop(id(listener))

    def logError(self, errorMessage):
        for listenerId in self.listeners:
            self.listeners[listenerId].logError(errorMessage)

