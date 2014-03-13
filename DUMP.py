

    def interactive_play(self):
        for i in range(self.n_trials):
            choice=int(raw_input('Trial {0}: enter bandit choice (0 to {1}): '.format(i, self.n_bandits-1)))
            reward=self.bandits.pull(choice)
            print "Reward obtained: {0}".format(reward)
            self.choices.append(choice)
            self.rewards.append(reward)
        self.report()

    def random_play(self):
        for i in range(self.n_trials):
            choice=numpy.random.choice(range(self.n_bandits))
            print "Random choice made: {0}".format(choice)
            reward=self.bandits.pull(choice)
            print "Reward obtained: {0}".format(reward)
            self.choices.append(choice)
            self.rewards.append(reward)
        self.report()
    
    def successrate_play(self):
        successrate_player=SuccessRatePlayer.SuccessRatePlayer()
        for i in range(self.n_trials):
            choice=successrate_player.choose()
            print "Optimal choice made: {0}".format(choice)
            reward=self.bandits.pull(choice)
            successrate_player.update_rewards(reward)
            print "Reward obtained: {0}".format(reward)
            self.choices.append(choice)
            self.rewards.append(reward)
        self.report()

    def optimal_play(self):
        optimal_player=OptimalPlayer.OptimalPlayer()
        for i in range(self.n_trials):
            choice=optimal_player.choose()
            print "Optimal choice made: {0}".format(choice)
            reward=self.bandits.pull(choice)
            optimal_player.update_rewards(reward)
            print "Reward obtained: {0}".format(reward)
            self.choices.append(choice)
            self.rewards.append(reward)
        self.report()

