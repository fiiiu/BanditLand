
import MultiarmedBandit
import SuccessRatePlayer
import OptimalPlayer
import playerFactory
import parameters
import numpy

class BanditGame(object):

    def __init__(self, p_list=parameters.p_list, n_trials=parameters.n_trials, player_choice=parameters.player_choice,\
                 metacognition=0):
        self.p_list=p_list
        self.n_bandits=len(p_list)
        self.n_trials=n_trials
        self.player_choice=player_choice
        self.bandits=MultiarmedBandit.MultiarmedBandit(p_list)
        self.choices=[]
        self.rewards=[]
        if self.player_choice is not None:
            self.create_player(self.player_choice)
        self.metacognition=metacognition
        #self.metacognitive_report=None
        self.oracle=OptimalPlayer.OptimalPlayer(n_bandits=self.n_bandits, n_trials=self.n_trials)

    def reset(self, new_player_choice=None):
        if new_player_choice is not None:
            #self.player_choice=new_player_choice
            self.player_select(new_player_choice)
        # reset player if optimal
        elif self.player_choice==3:
            self.player.reset() #partial reset, keep reward table for faster computation
        self.choices=[]
        self.rewards=[]


        
    def player_select(self, player_choice=None):
        if player_choice is None:
            self.player_choice=int(raw_input("Select player: you (0), random (1), success rate (2), optimal (3): "))
            print "{0} player selected.".format(playerFactory.player_type(self.player_choice))
        else:
            self.player_choice=player_choice
        self.create_player(self.player_choice)
    
    def create_player(self, player_choice):
        self.player=playerFactory.create_player(player_choice, n_trials=self.n_trials)

    def play(self):
        self.reset()
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
            #if self.metacognition and self.player_choice<=0 and i==int((self.n_trials-1)/2):
            #    self.metacognitive_report=self.player.metacognitive_report()
            if self.player_choice<0 and i==int((self.n_trials-1)/2):
                self.metacognitive_report=self.player.metacognitive_report(self.metacognition)
        return (self.choices, self.rewards)
        
    def average_reward(self):
        return float(sum(self.rewards))/self.n_trials

    def report(self):
        print "\nGame report:"
        for i in range(self.n_trials):
            print "Trial {0}: choice={1}, reward={2}".format(i, self.choices[i], self.rewards[i])
        print "Average reward achieved: {0}".format(self.average_reward())
        print "Average yoked optimal reward: {0}".format(float(self.yoked_optimal_play())/self.n_trials)

    def save(self, filename):
        numpy.savetxt(filename, numpy.array([range(self.n_trials), self.choices, self.rewards]).T,\
                      fmt='%d', header="Payoff probabilities: {0}\nMetacognitive report type: {1}\nMetacognitive report: {2}"\
                      .format(self.p_list, self.metacognition, self.metacognitive_report))



    def yoked_optimal_play(self):
        if len(self.choices)<self.n_trials:
            print "Must play first for yoked optimum computation."
            return None
        self.yoked_optimal_choices=[]
        self.yoked_optimal_rewards=[]
        total_reward=0
        progressive_successes=[0]*self.n_bandits
        progressive_failures=[0]*self.n_bandits
        for i in range(self.n_trials):
            if self.rewards[i]==1:
                progressive_successes[self.choices[i]]+=1
            elif self.rewards[i]==0:
                progressive_failures[self.choices[i]]+=1
            
            if i==0:
                choice=self.choices[0]
            else:
                choice=self.oracle.yoked_choose(progressive_successes, progressive_failures, self.n_trials-i)
            reward=self.bandits.pull(choice)
            total_reward+=reward
            self.yoked_optimal_choices.append(choice)
            self.yoked_optimal_rewards.append(reward)
        #return float(total_reward)/self.n_trials
        return total_reward

