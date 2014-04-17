


class BanditGameData():

    def __init__(self, subject=None, directory=None):
        self.subject=subject
        self.directory=directory
        self.choices=[]
        self.rewards=[]
        self.n_trials=0
        self.is_loaded=False

    def load_file(self, block):
        with open(self.directory+"{0}_{1}.txt".format(self.subject, block), 'r') as datafile:
            for line in datafile:
                data = line.split()
                if data[0]=='#':
                    continue #comment line
                self.choices.append(int(data[1]))
                self.rewards.append(int(data[2]))

        self.n_trials=len(self.choices)
        self.is_loaded=True


    def load(self, choices, rewards):
        self.choices=choices
        self.rewards=rewards
        self.n_trials=len(self.choices)
        self.is_loaded=True


