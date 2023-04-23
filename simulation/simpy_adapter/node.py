import simpy
from simulation.simpy_adapter.timeout_utils import *


class Node:
    def __init__(self, env, serviceTime):
        self.env = env
        self.executor = simpy.Resource(env, 1)
        self.serviceTime = serviceTime

    def process(self):
        yield self.env.timeout(timeoutFor(self.serviceTime))
