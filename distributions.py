import numpy as np

class Distribution(object):

    def __init__(self, pdf):
        self.pdf=pdf
        #self.parameters=parameters

    #def sample(self, arguments=None):
    #    parameters=tuple([*self.parameters])+tuple(arguments)
    #    return self.pdf(*parameters)


# class Beta(Distribution):

#     def __init__(self, alpha, beta):
#         super(Beta, self).__init__(np.random.beta)
#         self.alpha=alpha
#         self.beta=beta

#     def sample(self):
#         return self.pdf(self.alpha, self.beta)


class Beta():

    def __init__(self, argument_builder):
        self.argument_builder=argument_builder

    def sample(self, args=None):
        return np.random.beta(*self.argument_builder(args))

    def value(self):
        pass


# class Uniform(Distribution):

#     def __init__(self, a, b):
#         super(Uniform, self).__init__(np.random.uniform)
#         self.a=a
#         self.b=b

#     def sample(self):
#         return self.pdf(self.a, self.b)


class Bernoulli():

    def __init__(self, argument_builder):
        self.argument_builder=argument_builder

    def sample(self, arg):
        return np.random.binomial(1, self.argument_builder(arg))
        
    def value(self, result, p):
        #return scipy.stats.distributions.binom(1,p).pmf(result)
        #ok, but it's just this:
        return p*result+(1-p)*(1-result)