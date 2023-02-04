class Selection:

    def __init__(self):
        self.__selectedObject = None
        self.__selectionListeners = []

    def updateSelection(self, newSelection):
        if self.__selectedObject:
            self.__selectedObject.setObserver(None)
        self.__selectedObject = newSelection
        if self.__selectedObject:
            self.__selectedObject.setObserver(self)
        self.__broadcastSelectionChanged()

    def selectedObject(self):
        return self.__selectedObject

    def addListener(self, listener):
        self.__selectionListeners.append(listener)

    def objectChanged(self):
        self.__broadcastSelectionChanged()

    def __broadcastSelectionChanged(self):
        for listener in self.__selectionListeners:
            listener.onSelectionChanged()

