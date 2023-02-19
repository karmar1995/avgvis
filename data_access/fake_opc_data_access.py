import random
import threading
import time
from opc_adapter.opc_client_factory import AbstractOpcClientFactory

xSignal = ['x']
ySignal = ['y']
headingSignal = ['heading']
batterySignal = ['battery']
warningSignal1 = ['warning1']
informationSignal1 = ['information1']
KnownSignals = [
    str(xSignal),
    str(ySignal),
    str(headingSignal),
    str(batterySignal),
    str(warningSignal1),
    str(informationSignal1)]
FailureProbability = 0.1  # how often communication with serve will fail
MinX = -20  # outside the map origin
MinY = -20  # outside the map origin
MaxX = 70  # a bit larger than map width
MaxY = 70  # a bit larger than map height
UpdateInterval = 0.1  # s
ConnectionTime = 1  # s


class FakeOpcClientFactory(AbstractOpcClientFactory):
    def __init__(self):
        super().__init__()
        pass

    def createOpcClient(self, errorSink):
        return FakeOpcClient(errorSink)


class ObjectState:
    def __init__(self):
        self.__signals = dict()
        self.__signals[str(xSignal)] = MinX
        self.__signals[str(ySignal)] = MinY
        self.__signals[str(headingSignal)] = 0
        self.__signals[str(batterySignal)] = 0
        self.__signals[str(warningSignal1)] = False
        self.__signals[str(informationSignal1)] = False

    def getSignalValue(self, signal):
        if str(signal) in KnownSignals:
            return self.__signals[str(signal)]
        raise Exception("Unknown signal!")

    def setSignalValue(self, signal, value):
        if str(signal) in KnownSignals:
            self.__signals[str(signal)] = value
        else:
            raise Exception("Unknown signal!")


class StrategyBase:
    def __init__(self, objectState):
        self.__thread = threading.Thread(target=self.__updateMethod)
        self.__thread.daemon = True
        self._objectState = objectState

    def start(self):
        self.__thread.start()

    def __updateMethod(self):
        while True:
            self._objectState.setSignalValue(xSignal, self._updateX())
            self._objectState.setSignalValue(ySignal, self._updateY())
            self._objectState.setSignalValue(headingSignal, self._updateHeading())
            self._objectState.setSignalValue(batterySignal, random.randint(0, 100))
            self._objectState.setSignalValue(warningSignal1, random.randint(0, 1) == 1)
            self._objectState.setSignalValue(informationSignal1, random.randint(0, 1) == 1)
            time.sleep(UpdateInterval)

    def _updateX(self):
        raise Exception("Not Implemented")

    def _updateY(self):
        raise Exception("Not Implemented")

    def _updateHeading(self):
        return random.random()


class HorizontalMovingStrategy(StrategyBase):

    def __init__(self, objectState):
        super().__init__(objectState)
        self.__nextUpdateY = False

    def _updateX(self):
        step = (MaxX - MinX) / 20
        res = self._objectState.getSignalValue(xSignal) + step
        if res > MaxX:
            self.__nextUpdateY = True
            return MinX
        return res

    def _updateY(self):
        y = self._objectState.getSignalValue(ySignal)
        if self.__nextUpdateY:
            self.__nextUpdateY = False
            step = (MaxY - MinY) / 20
            res = y + step
            if res > MaxY:
                return MinY
            return res
        return y


class VerticalMovingStrategy(StrategyBase):
    pass


class DiagonalMovingStrategy(StrategyBase):
    pass


class RoundMovingStrategy(StrategyBase):
    pass


class RandomStrategy(StrategyBase):
    pass


class FakeOpcClient:
    MovingStrategies = [
        HorizontalMovingStrategy,
        # VerticalMovingStrategy,
        # DiagonalMovingStrategy,
        # RoundMovingStrategy,
        # RandomStrategy
    ]  # possible map traversing algorithms

    def __init__(self, errorSink):
        self.__connected = False
        self.__errorSink = errorSink
        self.__objectState = ObjectState()
        self.__strategy = random.choice(self.MovingStrategies)(self.__objectState)

    def connect(self, connectionString):
        time.sleep(ConnectionTime)
        if random.random() <= FailureProbability:
            self.__throw()
        self.__connected = True
        self.__strategy.start()

    def getSignalValue(self, signal):
        return self.__objectState.getSignalValue(signal)

    def getChildSignals(self, root):
        return {}

    def __throw(self):
        raise Exception("Server failure")

