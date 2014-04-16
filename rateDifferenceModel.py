
import numpy as np
import pymc


def make_model(data):

    #n_blocks=len(data0)
    n_blocks=data.shape[1]
    n_trials_0=10
    n_trials_1=10

    theta0=np.empty(n_blocks, dtype=object)
    theta1=np.empty(n_blocks, dtype=object)
    k0=np.empty(n_blocks, dtype=object)
    k1=np.empty(n_blocks, dtype=object)

    #theta0=pymc.Uniform('theta0', 0, 1)
    #theta1=pymc.Uniform('theta1', 0, 1)

    for i in range(n_blocks):
        theta0[i]=pymc.Uniform('theta0_{0}'.format(i), 0, 1)
        theta1[i]=pymc.Uniform('theta1_{0}'.format(i), 0, 1)

        k0[i]=pymc.Binomial('k0_{0}'.format(i), p=theta0[i], n=n_trials_0, value=data[0,i], observed=True)
        k1[i]=pymc.Binomial('k1_{0}'.format(i), p=theta1[i], n=n_trials_1, value=data[1,i], observed=True)

    # @pymc.deterministic
    # def delta(x=theta0, y=theta1):
    #     return x - y

    @pymc.deterministic
    def delta(x=theta0, y=theta1):
        return [xi-yi for xi,yi in zip(x,y)]
        
    return locals()

