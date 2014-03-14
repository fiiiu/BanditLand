
import GraphicalInterface
import BanditGame
import parameters
import numpy

class BanditExperiment():

    def __init__(self, n_bandits=parameters.n_bandits, n_blocks=parameters.n_blocks, n_trials=parameters.n_trials,\
                 graphical_interface=parameters.graphical_interface):
        self.n_bandits=n_bandits
        self.n_blocks=n_blocks
        self.n_trials=n_trials
        self.alpha=parameters.experiment_alpha
        self.beta=parameters.experiment_beta

        self.games=[]
        
        #construct bandits' payrates
        self.payrates=[numpy.random.beta(self.alpha, self.beta, n_bandits) for blo in range(n_blocks)]

        #graphical interface
        self.graphical_interface=graphical_interface
        if graphical_interface:
            self.interface=GraphicalInterface.GraphicalInterface()
            

    def run(self):
        if self.graphical_interface:
            self.run_graphical()
        else:
            self.run_text()
    
    def run_text(self):
        for i in range(self.n_blocks):
            print "\nStarting block {0}...\n".format(i)
            self.games.append(BanditGame.BanditGame(p_list=self.payrates[i], n_trials=self.n_trials, player_choice=0))
            self.games[-1].play()
            print "\nBlock {0} finished.\nBandit probabilities: {1}\nAverage reward achieved: {2}".format(i, self.payrates[i], self.games[-1].average_reward())

    def run_graphical(self):
        for i in range(self.n_blocks):
            self.interface.start_block(i)
            self.games.append(BanditGame.BanditGame(p_list=self.payrates[i], n_trials=self.n_trials, player_choice=-1))
            self.games[-1].player.set_interface(self.interface)
            self.games[-1].play()
            self.interface.end_block()

    def report(self):
        for game in self.games:
            game.report()


