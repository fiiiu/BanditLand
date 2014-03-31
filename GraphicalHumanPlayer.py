import BanditPlayer
import GraphicalInterface
import parameters

class GraphicalHumanPlayer(BanditPlayer.BanditPlayer):

    def __init__(self, n_bandits=len(parameters.p_list)):
        super(GraphicalHumanPlayer, self).__init__(n_bandits)
        
    def set_interface(self, graphical_interface):
        self.interface=graphical_interface

    def choose(self):
        choice=self.interface.choice_screen()
        self.choices.append(choice)
        return choice

    def update_rewards(self, reward):
        #show rewards
        self.interface.feedback_screen(reward)
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1
       
    def metacognitive_report(self, report_type):
        metacognitive_report=self.interface.metacognitive_screen(report_type)
        return metacognitive_report