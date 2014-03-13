
import MultiarmedBandit
import SuccessRatePlayer
import OptimalPlayer
import playerFactory
import parameters
import numpy.random

class BanditGame(object):

    def __init__(self, p_list=parameters.p_list, n_trials=parameters.n_trials):
        self.n_bandits=len(p_list)
        self.n_trials=n_trials
        self.bandits=MultiarmedBandit.MultiarmedBandit(p_list)
        self.choices=[]
        self.rewards=[]

        self.player_select()

    def player_select(self):
        if parameters.player_choice is not None:
            player_choice=parameters.player_choice
        else:
            player_choice=int(raw_input("Select player: you (0), random (1), success rate (2), optimal (3): "))
        print "{0} player selected.".format(playerFactory.player_type(player_choice))
        self.player=playerFactory.create_player(player_choice)

    def play(self):
        for i in range(self.n_trials):
            choice=self.player.choose()
            print "Choice made: {0}".format(choice)
            reward=self.bandits.pull(choice)
            self.player.update_rewards(reward)
            print "Reward obtained: {0}".format(reward)
            self.choices.append(choice)
            self.rewards.append(reward)
        self.report()

    def report(self):
        print "Game report:\n"
        for i in range(self.n_trials):
            print "Trial {0}: choice={1}, reward={2}".format(i, self.choices[i], self.rewards[i])
        print "Average reward achieved: {0}".format(float(sum(self.rewards))/self.n_trials)





