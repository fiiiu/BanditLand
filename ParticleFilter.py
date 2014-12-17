
import numpy as np

class ParticleFilter(object):
    """ParticleFilter Sampler.
       
       Attributes:
            likelihood, prior, drift: Distribution
            N, T: Int

    """

    def __init__(self, prior, likelihood, drift, N, T):
        self.prior=prior
        self.likelihood=likelihood
        self.drift=drift
        self.N=N
        self.T=T
        self.z=np.empty((self.N, self.T))
        self.ztilde=np.empty((self.N, self.T))
        self.weights=np.empty((self.N, self.T))
        self.initialize()
        self.thin=1#0

    def initialize(self):
        for i in range(self.N):
            self.weights[i,0]=1./self.N
            self.z[i,0]=self.prior.sample()
            #print self.z[i,0]

    def sample_step(self, t, y):
        for i in range(self.N):
            self.ztilde[i,t]=self.drift.sample(self.z[i,t-1])
            #self.weights[i,t]=self.weights[i,t-1]*self.likelihood.sample()
            #I keep the weights for saving instead of renormalizing, and here use 1/N:
            self.weights[i,t]=self.likelihood.value(y, self.ztilde[i,t]) #1./self.N*
        self.weights[:,t]/=sum(self.weights[:,t])


    def selection_step(self, t):
        for i in range(self.N):
            #multinomial sampling
            #renormalized_weights=self.weights[:,t]/sum(self.weights[:,t])
            self.z[i,t]=self.ztilde[np.where(np.random.multinomial(1, self.weights[:,t]))[0][0],t]
                
    def run(self, data):
        self.initialize()
        for t in range(1, self.T):
            self.sample_step(t, data[t])
            if t % self.thin == 0:  
                self.selection_step(t)
            else:
                for i in range(self.N):
                    self.z[i,t]=self.ztilde[i,t]

    def run_ess(self, data):
        resamples=0
        self.initialize()
        for t in range(1, self.T):
            self.sample_step(t, data[t])
            if 1./sum(self.weights[:,t]**2) < self.N*0.9:
                self.selection_step(t)
                resamples+=1
            else:
                for i in range(self.N):
                    self.z[i,t]=self.ztilde[i,t] 
        print resamples
        print 1./sum(self.weights[:,13]**2)

    def show(self):
        print self.z, self.weights

    def summary(self):
        print np.mean(self.z[:,self.T-1])

    def final_value(self):
        return self.z[:,self.T-1]

    def save(self, output_dir='./', identifier=''):
        np.savetxt(output_dir+identifier+'z.txt', self.z)
        np.savetxt(output_dir+identifier+'ztilde.txt', self.ztilde)
        np.savetxt(output_dir+identifier+'w.txt', self.weights)





