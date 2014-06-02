import numpy

p_list=[0.35, 0.3]
n_trials=16
player_choice=None

#Experiment parameters
#metacognitive report: 'sorted' (0,1,2,3,..) for testing; 'random' for experiment, ..
block_ordering='random'#'sorted'
include_conditions=[0,1,2]
graphical_interface=True
n_bandits=2
blocks_per_condition=45
#bandit probabilities hyperparameters
experiment_alpha=1
experiment_beta=1


#Graphical Interface

new=False
if new:
	fullscreen=False
	bandit_width=0.2
	bandit_height=0.24
	progress_width=0.5
	progress_height=0.02
	confidence_height=0.05
	reward_size=0.1
else:
	fullscreen=True
	bandit_width=0.08
	bandit_height=0.18
	progress_width=0.5
	#progress_height=0.02
	progress_height=22
	confidence_height=0.05
	reward_size=0.015
