
import Bandit

class MultiarmedBandit():

    def __init__(self, p_list):

        self.bandits=[Bandit.Bandit(p) for p in p_list]
         

    def pull(self, k):
        #return map(Bandit.pull, self.bandits)
        #DOESN'T WORK. HOW TO ACCESS BANDIT.PULL?! NOT WHAT I WANT ANYWAY..
        return self.bandits[k].pull()

        