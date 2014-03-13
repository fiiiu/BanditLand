import numpy
import parameters

class BanditPlayer(object):

    def __init__(self, n_bandits=len(parameters.p_list)):
        self.n_bandits=n_bandits
        #self.trials_played=0
        self.choices=[]
        self.rewards=[]
        self.successes=[0]*self.n_bandits
        self.failures=[0]*self.n_bandits


    def update_rewards(self, reward):
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1
        #print self.successes
        #print self.failures

