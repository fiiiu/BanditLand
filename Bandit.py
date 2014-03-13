
import numpy.random

class Bandit():
    """docstring for Bandit"""

    def __init__(self, p):
        self.p = p

    def pull(self):
        return numpy.random.binomial(1, self.p)

