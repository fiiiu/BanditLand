import BanditPlayer
import numpy
import parameters

class SuccessRatePlayer(BanditPlayer.BanditPlayer):

    def __init__(self, n_bandits=len(parameters.p_list)):

        super(SuccessRatePlayer, self).__init__(n_bandits)
        

    def choose(self):
        choice_worths=numpy.zeros(self.n_bandits)
        for i in range(self.n_bandits):
            choice_worths[i]=float(self.successes[i]+1)/(self.successes[i]+self.failures[i]+2)
        bests=numpy.where(choice_worths==choice_worths.max())[0]
        choice=numpy.random.choice(bests)
        self.choices.append(choice)
        #update!
        #self.trials_played=self.trials_played+1
        return choice

    def update_rewards(self, reward):
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1
       

