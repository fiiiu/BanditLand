
import MultiarmedBandit
import SuccessRatePlayer
import OptimalPlayer
import playerFactory
import parameters
import numpy.random

class BanditGame(object):

    def __init__(self, p_list=parameters.p_list, n_trials=parameters.n_trials, player_choice=parameters.player_choice):
        self.n_bandits=len(p_list)
        self.n_trials=n_trials
        self.player_choice=player_choice
        self.bandits=MultiarmedBandit.MultiarmedBandit(p_list)
        #self.player_select(self.player_choice)
        self.choices=[]
        self.rewards=[]
        
    def reset(self, new_player_choice=None):
        if new_player_choice is not None:
            self.player_choice=new_player_choice
        self.choices=[]
        self.rewards=[]
        
    def player_select(self, player_choice=None):
        if player_choice is None:
            self.player_choice=int(raw_input("Select player: you (0), random (1), success rate (2), optimal (3): "))
            print "{0} player selected.".format(playerFactory.player_type(self.player_choice))
        else:
            self.player_choice=player_choice
    
    def create_player(self, player_choice):
        self.player=playerFactory.create_player(player_choice)

    def play(self):
        if self.player_choice is None:
            self.player_select()
        self.create_player(self.player_choice)

        for i in range(self.n_trials):
            choice=self.player.choose()
            #print "Choice made: {0}".format(choice)
            reward=self.bandits.pull(choice)
            self.player.update_rewards(reward)
            #print "Reward obtained: {0}".format(reward)
            self.choices.append(choice)
            self.rewards.append(reward)

        average_reward=float(sum(self.rewards))/self.n_trials
        #self.report(average_reward)
        return average_reward

    
    def report(self, average_reward):
        print "Game report:\n"
        for i in range(self.n_trials):
            print "Trial {0}: choice={1}, reward={2}".format(i, self.choices[i], self.rewards[i])
        print "Average reward achieved: {0}".format(average_reward)
        




