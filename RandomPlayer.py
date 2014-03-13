import BanditPlayer
import numpy
import parameters

class RandomPlayer(BanditPlayer.BanditPlayer):

    def __init__(self, n_bandits=len(parameters.p_list)):

        super(RandomPlayer, self).__init__(n_bandits)
        

    def choose(self):
        choice=numpy.random.choice(self.n_bandits)
        self.choices.append(choice) #stupid yet mnemonic!
        return choice

    def update_rewards(self, reward):
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1
       

