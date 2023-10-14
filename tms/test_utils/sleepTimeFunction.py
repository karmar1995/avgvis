import random

avg = 5


def sleepFunction(mean):
    return random.gauss(mu=mean, sigma=0.5)


def check(samples):
    res = []

    for i in range(0, samples):
        res.append(sleepFunction(avg))

    print("Min: {}".format(min(res)))
    print("Avg: {}".format(sum(res)/len(res)))
    print("Max: {}".format(max(res)))

#check(100)