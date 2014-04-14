

#import BanditExperiment
#import BanditGame
import ExperimentData
import matplotlib.pyplot as plt


subject='alego'
data=ExperimentData.ExperimentData(subject)

data.load_file()


def type2_perfo(metacog_types):
    payrates=data.get_payrates(metacog_types=metacog_types)
    reports=data.get_reports(metacog_types=metacog_types,report_part=0)
    dif=[]
    rep=[]
    for payrate, report in zip(payrates, reports):
        dif.append(payrate[1]-payrate[0])
        rep.append(report)
    return dif, rep
    

def type2_perfo_plot():

    dif1,rep1=type2_perfo([1])
    dif2,rep2=type2_perfo([2])
    jitrep2=[0.96*rep+0.02 for rep in rep2]

    plt.plot(dif1, rep1, 'bo')
    plt.plot(dif2, jitrep2, 'rs')
    plt.xlim([-0.7, 0.7])
    plt.ylim([-0.02, 1.02])
    plt.legend(['1', '2'])
    plt.show()


def confidence_plot():
    payrates=data.get_payrates(metacog_types=[2])
    reports=data.get_reports(metacog_types=[2],report_part=1)
    dif=[]
    rep=[]
    for payrate, report in zip(payrates, reports):
        dif.append(abs(payrate[1]-payrate[0]))
        rep.append(report)
    plt.plot(dif,rep, 'ks')
    plt.xlim([0, 0.7])
    plt.ylim([-0.02, 1.02])
    plt.show()


def main():
    #type2_perfo_plot()
    confidence_plot()

if __name__ == '__main__':
    main()
