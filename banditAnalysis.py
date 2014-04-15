

#import BanditExperiment
#import BanditGame
import utils
import ExperimentData
import matplotlib.pyplot as plt
from scipy import stats


subject='mati'
directory='/Users/alejo/Neuro/CostOfTheories/Data/Mati/'
data=ExperimentData.ExperimentData(subject, directory)

data.load_file()


def type2_perfo(metacog_types, addition=False):
    payrates=data.get_payrates(metacog_types=metacog_types)
    reports=data.get_reports(metacog_types=metacog_types,report_part=0)
    dif=[]
    rep=[]
    for payrate, report in zip(payrates, reports):
        if addition:
            dif.append(payrate[1]+payrate[0])
            rep.append(report==(payrate[1]-payrate[0]>0))
        else:
            dif.append(payrate[1]-payrate[0])
            rep.append(report)

    return dif, rep
    

def type2_perfo_plot(addition=False):

    dif1,rep1=type2_perfo([1], addition)
    dif2,rep2=type2_perfo([2], addition)
    jitrep2=[0.96*rep+0.02 for rep in rep2]

    plt.plot(dif1, rep1, 'bo')
    plt.plot(dif2, jitrep2, 'rs')
    #plt.xlim([-0.7, 0.7])
    plt.ylim([-0.02, 1.02])
    plt.legend(['1', '2'])
    plt.show()


def type2_perfo_plot_binned(addition=False):

    # pairs1=[(dif1,rep1) for dif1,rep1 in type2_perfo([1])]
    dif,rep=type2_perfo([1,2], addition)
    dif1,rep1=type2_perfo([1])
    dif2,rep2=type2_perfo([2])
    jitrep2=[0.96*repz+0.02 for repz in rep2]

    bave,bcenters,num=utils.binned_average(zip(dif,rep), nbins=6)
    print bave, bcenters, num
    plt.plot(bcenters, bave, 'k-s')
    plt.ylim([-0.02, 1.02])
    plt.xlim([-0.9,0.9])
    plt.show()

    # plt.plot(dif1, rep1, 'bo')
    # plt.plot(dif2, jitrep2, 'rs')
    # plt.xlim([-0.7, 0.7])
    # plt.ylim([-0.02, 1.02])
    # plt.legend(['1', '2'])
    # plt.show()



def confidence_plot(addition=False):
    payrates=data.get_payrates(metacog_types=[2])
    reports=data.get_reports(metacog_types=[2],report_part=1)
    dif=[]
    rep=[]
    for payrate, report in zip(payrates, reports):
        if addition:
            dif.append(payrate[1]+payrate[0])
        else:
            dif.append(abs(payrate[1]-payrate[0]))
        rep.append(report)


    utils.plot_and_correlate(dif, rep)

    #test for mati's progression. 
    #utils.plot_and_correlate(dif[0:12], rep[0:12])
    #utils.plot_and_correlate(dif[12:24], rep[12:24])
    
    # plt.plot(dif,rep, 'ks')
    # plt.xlim([0, 0.7])
    #plt.ylim([-0.02, 1.02])
    # plt.show()


def main():
    type2_perfo_plot() #o yea
    #type2_perfo_plot(True) # can't see, perfect score for mati!
    confidence_plot() #corr
    #confidence_plot(True) #no corr
    type2_perfo_plot_binned()


if __name__ == '__main__':
    main()
