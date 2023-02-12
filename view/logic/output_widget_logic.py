class LogLevel:
    Error = 0
    Warning = 1
    Information = 2
    Debug = 3


class OutputWidgetLogic:
    def __init__(self):
        self.__errorsLog = list()
        self.__warningsLog = list()
        self.__informationLog = list()
        self.__debugLog = list()
        self.__viewAccess = None

    def setViewAccess(self, viewAccess):
        self.__viewAccess = viewAccess

    def logError(self, message):
        self.__log(self.__errorsLog, message)

    def logWarning(self, message):
        self.__log(self.__warningsLog, message)

    def logInformation(self, message):
        self.__log(self.__informationLog, message)

    def logDebug(self, message):
        self.__log(self.__debugLog, message)

    def getLogs(self, logLevel):
        logs = dict()
        if logLevel >= LogLevel.Error:
            logs['errors'] = self.__errorsLog
        if logLevel >= LogLevel.Warning:
            logs['warnings'] = self.__warningsLog
        if logLevel >= LogLevel.Information:
            logs['information'] = self.__informationLog
        if logLevel >= LogLevel.Debug:
            logs['debug'] = self.__debugLog
        return logs

    def clear(self):
        self.__errorsLog.clear()
        self.__warningsLog.clear()
        self.__informationLog.clear()
        self.__debugLog.clear()

    def __log(self, logCollection, message):
        logCollection.append(message)
        if self.__viewAccess is not None:
            self.__viewAccess.updateLogs()
