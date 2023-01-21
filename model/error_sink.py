class ErrorSink:
    def __init__(self):
        self.listeners = dict()

    def addListener(self, listener):
        self.listeners[id(listener)] = listener

    def removeListener(self, listener):
        self.listeners.pop(id(listener))

    def logError(self, errorMessage):
        for listener in self.listeners:
            listener.logError(errorMessage)

