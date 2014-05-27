
import ExperimentData
import GraphicalInterface
import BanditGame
import playerFactory
import parameters
import numpy

class BanditExperiment():

    def __init__(self, subject, n_bandits=parameters.n_bandits, blocks_per_condition=parameters.blocks_per_condition, \
                 include_conditions=parameters.include_conditions, block_ordering=parameters.block_ordering, \
                 n_trials=parameters.n_trials, alpha=parameters.experiment_alpha, beta=parameters.experiment_beta, \
                 graphical_interface=parameters.graphical_interface, payrates=None, demo=False):#, metacognition=parameters.metacognition):
        
        self.subject=subject
        self.n_bandits=n_bandits
        self.n_blocks=blocks_per_condition*len(include_conditions)
        self.n_trials=n_trials
        block_ordering=block_ordering
        self.alpha=alpha
        self.beta=beta

        self.data=ExperimentData.ExperimentData(self.subject)
        
        self.accumulated_player_reward=0
        self.accumulated_optimal_reward=0

        #payrates
        if payrates is None:
            #construct bandits' payrates
            self.payrates=[numpy.random.beta(self.alpha, self.beta, n_bandits) for blo in range(blocks_per_condition)]
            #self.save_payrates()
        elif type(payrates) is str:
            preprepayrates=numpy.loadtxt(payrates)
            prepayrates=[numpy.random.permutation(pay) for pay in preprepayrates]
            self.payrates=numpy.random.permutation(prepayrates)[0:blocks_per_condition]
            #print self.payrates
        #elif payrates=="load":
        #    self.payrates=numpy.loadtxt("Input/payrates_{0}Ban_{1}Blo_{2}Tri.txt".format(n_bandits, blocks_per_condition, n_trials))
        else:
            self.payrates=payrates

        #metacognition order
        ordered_conditions=numpy.array([[el]*blocks_per_condition for el in include_conditions]).flatten()
        expanded_payrates=numpy.tile(self.payrates, (len(include_conditions), 1))
        sort_order=range(self.n_blocks)
        if block_ordering=='random':
            numpy.random.shuffle(sort_order)
        self.conditions=ordered_conditions[sort_order]
        self.payrates=expanded_payrates[sort_order]

        #graphical interface
        self.graphical_interface=graphical_interface
        if graphical_interface:
            self.interface=GraphicalInterface.GraphicalInterface(self.n_trials)
            
        if demo:
            self.conditions=[0,0,0,1,1,2,2]
            self.payrates=[[0.1,0.9],[0.8,0.65],[0.1,0.1],[0.9,0.1],[0.4,0.4],[0.1,0.9],[0.9,0.9]]
            #self.conditions=[0,0]
            #self.payrates=[[0.1,0.1],[0.1,0.1]]
            self.n_blocks=len(self.conditions)

    def run(self, model=None):
        self.games=[]
        if model is not None:
            self.subject=playerFactory.player_type(model)
            self.run_model(model)
        else:
            #if self.metacognition:
            self.run_metacognition()
            #elif self.graphical_interface:
            #    self.run_graphical()
            #else:
            #    self.run_text()

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
        for i in range(self.n_blocks):
            this_condition=self.conditions[i]
            #this_metacognition=this_condition=="metacog"
            these_payrates=self.payrates[i]
            self.interface.start_block(i)
            self.games.append(BanditGame.BanditGame(p_list=these_payrates, n_trials=self.n_trials, player_choice=-1, metacognition=this_condition))
            self.games[-1].player.set_interface(self.interface)
            self.games[-1].play()
            player_reward=sum(self.games[-1].rewards)
            optimal_reward=self.games[-1].yoked_optimal_play()
            self.accumulated_player_reward+=player_reward
            self.accumulated_optimal_reward+=optimal_reward
            #self.interface.end_block(player_reward, optimal_reward, \
            #    float(self.accumulated_player_reward)/(i+1), float(self.accumulated_optimal_reward)/(i+1))
            self.interface.end_block(player_reward, optimal_reward, \
                float(self.accumulated_player_reward)/self.n_blocks, float(self.accumulated_optimal_reward)/self.n_blocks)
            self.games[-1].save("Output/{0}_{1}.txt".format(self.subject, i))
            self.data.load_block(this_condition, these_payrates, self.games[-1].metacognitive_report)

        self.interface.close()



    def report(self):
        for game in self.games:
            game.report()

    def save(self):
        self.data.save_experiment_file()


    def save_payrates(self):
        numpy.savetxt("Input/payrates_{0}Ban_{1}Blo_{2}Tri.txt".format(self.n_bandits, self.n_blocks, self.n_trials), self.payrates)