import ParticleFilter
import distributions
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DEBUG=False

L=10000
T=1000
N=100
prior=distributions.Beta(lambda x: (1,1))
likelihood=distributions.Bernoulli(lambda x: x)
drift=distributions.Beta(lambda x: (L*x+1, L*(1-x)+1))

if DEBUG:
    print prior.sample()
    print likelihood.value(1,0.3)
    print likelihood.value(0,0.3)
    print likelihood.sample(0.4)
    print drift.sample(0.3)



pf=ParticleFilter.ParticleFilter(prior, likelihood, drift, N, T)
data=np.random.binomial(1, 0.8, T)
#pf.run_ess(data)
pf.run(data)
#pf.show()
print np.mean(data)
pf.summary()
#print pf.final_value()

#print pf.weights[:,0], sum(pf.weights[:,0])
#print pf.weights[:,8], sum(pf.weights[:,8])
#print pf.weights[:,9], sum(pf.weights[:,9])
    
# plt.plot(range(T),np.mean(pf.z, 0))
plt.ylim([0,1])
# #plt.hist(pf.final_value())
# #plt.xlim([0,1])

sns.tsplot(pf.z)
w=30#int(float(T)/50)
convolved_data=[np.mean(data[t:t+w]) for t in range(T-w)]
plt.plot(range(w/2,T-w/2), convolved_data, 'g')
#print pf.z

plt.show()

plt.plot(range(T),np.std(pf.weights, 0), 'r')
plt.show()


print np.std(pf.weights, 0).shape
