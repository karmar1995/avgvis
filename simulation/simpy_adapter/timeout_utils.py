import random


def timeoutFor(val):
    if val == 0:
        val = 0.00001
    return random.expovariate(1/val)
