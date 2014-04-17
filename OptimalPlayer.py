
import BanditPlayer
import numpy
import parameters


class OptimalPlayer(BanditPlayer.BanditPlayer):

    def __init__(self, n_bandits=len(parameters.p_list)):

        super(OptimalPlayer, self).__init__(n_bandits)
        self.alpha=1
        self.beta=1
        self.trials_played=0
        self.expected_reward_table={}
        self.maximizing_choice_table={}


    def reset(self, full=False):
        self.trials_played=0
        if full:
            self.expected_reward_table={}
            self.maximizing_choice_table={}


    def choose(self):
        _, maximizing_choices=self.expected_reward(parameters.n_trials-self.trials_played, self.successes, self.failures)
        choice=numpy.random.choice(maximizing_choices)
        self.choices.append(choice)
        self.trials_played+=1
        return choice


    def expected_reward(self, trials_remaining, successes, failures):
        """Solve optimal recursion.
            successes is a list containing the number of successes for each arm of the bandit.
            failures likewise.
            all stored in self.expected_reward_table to avoid recomputation
        """
        if (trials_remaining, tuple(successes), tuple(failures)) in self.expected_reward_table.keys():
            return (self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))],\
                    self.maximizing_choice_table[(trials_remaining, tuple(successes), tuple(failures))])
        else:
            if trials_remaining==0:
                self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))]=0
                self.maximizing_choice_table[(trials_remaining, tuple(successes), tuple(failures))]=range(self.n_bandits)
                return (0, range(self.n_bandits))
            else:
                posterior_success=[]
                posterior_failure=[]
                future_rewards=[]
                for b in range(self.n_bandits):
                    posterior_success.append(float(successes[b]+self.alpha)/(successes[b]+failures[b]+self.alpha+self.beta))
                    posterior_failure.append(float(failures[b]+self.beta)/(successes[b]+failures[b]+self.alpha+self.beta))
                    
                    future_successes_if_success=list(successes)
                    future_successes_if_success[b]+=1
                    future_failures_if_success=list(failures)
                    
                    future_successes_if_failure=list(successes)
                    future_failures_if_failure=list(failures)
                    future_failures_if_failure[b]+=1
                                        
                    exp_reward_success=self.expected_reward(trials_remaining-1, future_successes_if_success, future_failures_if_success)[0]
                    exp_reward_failure=self.expected_reward(trials_remaining-1, future_successes_if_failure, future_failures_if_failure)[0] 

                    future_reward=posterior_success[b]*(1+exp_reward_success) + \
                                  posterior_failure[b]*exp_reward_failure
                    future_rewards.append(future_reward)

                self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))]=max(future_rewards)
                maximizing_choices=numpy.where(numpy.array(future_rewards)==numpy.array(future_rewards).max())[0]
                self.maximizing_choice_table[(trials_remaining, tuple(successes), tuple(failures))]=maximizing_choices
                
                return (self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))],\
                        self.maximizing_choice_table[(trials_remaining, tuple(successes), tuple(failures))])
                

    def update_rewards(self, reward):
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1


