
import GraphicalInterface
import BanditGame
import playerFactory
import parameters
import numpy

class BanditExperiment():

    def __init__(self, subject, n_bandits=parameters.n_bandits, n_blocks=parameters.n_blocks, n_trials=parameters.n_trials,\
                 graphical_interface=parameters.graphical_interface, payrates=None, metacognition=parameters.metacognition):
        
        self.subject=subject
        self.n_bandits=n_bandits
        self.n_blocks=n_blocks
        self.n_trials=n_trials
        self.metacognition=metacognition
        self.alpha=parameters.experiment_alpha
        self.beta=parameters.experiment_beta
        
        #payrates
        if payrates is None:
            #construct bandits' payrates
            self.payrates=[numpy.random.beta(self.alpha, self.beta, n_bandits) for blo in range(n_blocks)]
            #self.save_payrates()
        elif payrates=="load":
            self.payrates=numpy.loadtxt("Input/payrates_{0}Ban_{1}Blo_{2}Tri.txt".format(n_bandits, n_blocks, n_trials))
        else:
            self.payrates=payrates

        #metacognition
        if self.metacognition:
            conditions=numpy.array(["plain"]*self.n_blocks+["metacog"]*self.n_blocks)
            doubled_payrates=numpy.concatenate([self.payrates, self.payrates])
            sort_order=numpy.random.permutation(range(2*n_blocks))
            self.conditions=conditions[sort_order]
            self.doubled_payrates=doubled_payrates[sort_order]
            block_numbers=numpy.array(range(n_blocks)+range(n_blocks))
            self.block_numbers=block_numbers[sort_order]
        else:
            self.conditions=["plain"*self.n_blocks]
            sort_order=numpy.random.permutation(range(n_blocks))
            self.payrates=self.payrates[sort_order]
            self.block_numbers=range(n_blocks)
            
        #graphical interface
        self.graphical_interface=graphical_interface
        if graphical_interface:
            self.interface=GraphicalInterface.GraphicalInterface()
            
    def run(self, model=None):
        self.games=[]
        if model is not None:
            self.subject=playerFactory.player_type(model)
            self.run_model(model)
        else:
            if self.metacognition:
                self.run_metacognition()
            elif self.graphical_interface:
                self.run_graphical()
            else:
                self.run_text()
    
    def run_model(self, model):
        for i in range(self.n_blocks):
            self.games.append(BanditGame.BanditGame(p_list=self.payrates[i], n_trials=self.n_trials, player_choice=model))
            self.games[-1].play()
            
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

    def run_metacognition(self):
        for i in range(2*self.n_blocks):
            this_condition=self.conditions[i]
            this_metacognition=this_condition=="metacog"
            these_payrates=self.doubled_payrates[i]
            self.interface.start_block(i)
            self.games.append(BanditGame.BanditGame(p_list=these_payrates, n_trials=self.n_trials, player_choice=-1, metacognition=this_metacognition))
            self.games[-1].player.set_interface(self.interface)
            self.games[-1].play()
            self.interface.end_block()

    def report(self):
        for game in self.games:
            game.report()

    def save(self):
        for i,game in enumerate(self.games):
            game.save("Output/block_{0}_{1}_{2}.txt".format(self.subject, self.block_numbers[i], self.conditions[i]))

    def save_payrates(self):
        numpy.savetxt("Input/payrates_{0}Ban_{1}Blo_{2}Tri.txt".format(self.n_bandits, self.n_blocks, self.n_trials), self.payrates)