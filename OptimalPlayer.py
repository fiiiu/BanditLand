
import BanditPlayer
import numpy
import parameters


class OptimalPlayer(BanditPlayer.BanditPlayer):

    def __init__(self, n_bandits=len(parameters.p_list)):

        super(OptimalPlayer, self).__init__(n_bandits)
        self.alpha=1
        self.beta=1
        self.expected_reward_table={}


    def choose(self):
        choice_worths=numpy.zeros(self.n_bandits)
        for i in range(self.n_bandits):
            choice_worths[i]=float(self.successes[i]+1)/(self.successes[i]+self.failures[i]+2)
        bests=numpy.where(choice_worths==choice_worths.max())[0]
        choice=numpy.random.choice(bests)
        self.choices.append(choice)
        #update!
        #self.trials_played=self.trials_played+1
        return choice


    def expected_reward(self, trials_remaining, successes, failures):
        """Solve optimal recursion.
            successes is a list containing the number of successes for each arm of the bandit.
            failures likewise.
            all stored in self.expected_reward_table to avoid recomputation
        """
        if (trials_remaining, tuple(successes), tuple(failures)) in self.expected_reward_table.keys():
            return self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))]
        else:
            if trials_remaining==0:
                self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))]=0
                return 0
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
                                        
                    future_reward=posterior_success[b]*\
                                        (1+self.expected_reward(trials_remaining-1, future_successes_if_success, future_failures_if_success)) + \
                                  posterior_failure[b]*\
                                        self.expected_reward(trials_remaining-1, future_successes_if_failure, future_failures_if_failure) 
                    future_rewards.append(future_reward)

                self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))]=max(future_rewards)
                return self.expected_reward_table[(trials_remaining, tuple(successes), tuple(failures))]
                

    def update_rewards(self, reward):
        #update rewards
        self.rewards.append(reward)
        #update successes/failures of last bandit chosen
        if reward==1:
            self.successes[self.choices[-1]]+=1
        elif reward==0:
            self.failures[self.choices[-1]]+=1


