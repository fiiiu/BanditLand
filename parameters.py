import numpy

p_list=[0.35, 0.3]
n_trials=10
player_choice=None

#Experiment parameters
#metacognitive report: 'sorted' (0,1,2,3,..) for testing; 'random' for experiment, ..
block_ordering='sorted'
include_conditions=[0,1]
graphical_interface=True
n_bandits=2
blocks_per_condition=1
#bandit probabilities hyperparameters
experiment_alpha=1
experiment_beta=1


#Graphical Interface
bandit_width=0.1
bandit_height=0.2
progress_width=0.5
progress_height=0.05
reward_size=0.01
