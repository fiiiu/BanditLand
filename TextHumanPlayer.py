import BanditPlayer
import parameters

class TextHumanPlayer(BanditPlayer.BanditPlayer):

    def __init__(self, n_bandits=len(parameters.p_list)):

        super(TextHumanPlayer, self).__init__(n_bandits)
        

    def choose(self):
        choice=int(raw_input('Enter bandit choice (0 to {0}): '.format(self.n_bandits-1)))   
        self.choices.append(choice)
        return choice

    def update_rewards(self, reward):
        #show rewards
        print "Reward this trial: {0}".format(reward)
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1
       