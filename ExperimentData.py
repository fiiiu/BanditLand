
import BanditGameData
import BanditExperiment
import BanditGame
from collections import defaultdict

class ExperimentData():

    def __init__(self, subject, directory="Output/"):
        self.subject=subject
        self.directory=directory
        self.n_blocks=0
        #self.raw_data=[]
        self.conditions=[]
        self.payrates=[]
        self.reports=[]
        self.bandit_data=defaultdict(dict)
        self.is_loaded=False



    def load_files(self):
        self.load_experiment_file()
        for block in range(self.n_blocks):
            bgd=BanditGameData.BanditGameData(self.subject, self.directory)
            bgd.load_file(block)
            #self.bandit_data.append(bgd)
            self.bandit_data[self.conditions[block]][self.payrates[block]]=bgd
        self.is_loaded=True


    def load_experiment_file(self):
        with open(self.directory+"{0}_REPORT.txt".format(self.subject), 'r') as datafile:
            for line in datafile:
                self.n_blocks+=1
                data = line.split()
                #self.raw_data.append((data[1], data[2], data[3], data[4], data[5]))
                block=int(data[0])
                self.conditions.append(int(data[1]))
                self.payrates.append((float(data[2]),float(data[3])))
                if self.conditions[block]==0:
                    self.reports.append((None,None))
                elif self.conditions[block]==1:
                    self.reports.append((float(data[4]),None))
                elif self.conditions[block]==2:
                    self.reports.append((float(data[4]),float(data[5])))

    def save_experiment_file(self):
        if self.is_loaded:
            save_file=open(self.directory+"{0}_REPORT.txt".format(self.subject),'w')
            for i in range(self.n_blocks):
                save_file.write("{0} {1} {2} {3} {4} {5}\n".format(i, self.conditions[i], self.payrates[i][0], self.payrates[i][1],\
                                 self.reports[i][0], self.reports[i][1]))
            save_file.close()

    def load_block(self, condition, payrates, report):
        self.n_blocks+=1
        self.conditions.append(condition)
        self.payrates.append(payrates)
        if condition==0:
            self.reports.append(('None', 'None'))
        elif condition==1:
            self.reports.append((report, 'None'))
        elif condition==2:
            self.reports.append(report)
        elif condition==3:
            self.reports.append(report)
        self.is_loaded=True


    def get_payrates(self, metacog_types):
        payrates=[]
        for block in range(self.n_blocks):
            if self.conditions[block] in metacog_types:
                payrates.append(self.payrates[block])
        return payrates

    def get_reports(self, metacog_types, report_part):
        reports=[]
        for block in range(self.n_blocks):
            if self.conditions[block] in metacog_types:
                reports.append(self.reports[block][report_part])
        return reports
