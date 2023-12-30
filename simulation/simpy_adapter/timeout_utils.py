import random


def timeoutFor(val):
#    return val
#    if val == 0:
#        val = 0.00001
#    return random.expovariate(1/val)
    return max(random.gauss(val, 0.5), 0.001)


def transitionTimeout(val):
    return max(random.gauss(val, 0.5), 0.001)