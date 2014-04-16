

#import BanditExperiment
#import BanditGame
import rateDifferenceModel
import gameAnalyzer
import utils
import ExperimentData
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
import numpy as np
import pymc



# LOAD
subject='pato'
subject_trials=16
#directory='/Users/alejo/Neuro/CostOfTheories/Data/Mati/'
directory='/home/alejo/Neuro/CostOfTheories/Data/'+subject+'/'
data=ExperimentData.ExperimentData(subject, directory)
data.load_files()


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

def global_analysis():

    # EXPE WIDE ANALYSIS
    type2_perfo_plot() #o yea
    type2_perfo_plot(True) # can't see, perfect score for mati!
    confidence_plot() #corr
    confidence_plot(True) #no corr
    type2_perfo_plot_binned()





def block_analysis(model=False):
    
    # BLOCK BY BLOCK
    pre_metacog_switches={0:[], 1:[], 2:[]}
    post_metacog_switches={0:[], 1:[], 2:[]}
    difficulties={0:[], 1:[], 2:[]}
    generosities={0:[], 1:[], 2:[]}
    pre_met_swi_rews={0:[], 1:[], 2:[]}
    post_met_swi_rews={0:[], 1:[], 2:[]}
    
    for condition in set(data.conditions):
        for payrate in set(data.payrates):
            pre_metacog_switches[condition].append(gameAnalyzer.metacog_switches(data.bandit_data[condition][payrate], n_trials=subject_trials, post_metacog=False))
            post_metacog_switches[condition].append(gameAnalyzer.metacog_switches(data.bandit_data[condition][payrate], n_trials=subject_trials, post_metacog=True))
            difficulties[condition].append(1-abs(payrate[1]-payrate[0]))
            generosities[condition].append((payrate[1]+payrate[0])/2)
            pre_met_swi_rews[condition].append(gameAnalyzer.metacog_rewards(data.bandit_data[condition][payrate], n_trials=subject_trials, post_metacog=False))
            post_met_swi_rews[condition].append(gameAnalyzer.metacog_rewards(data.bandit_data[condition][payrate], n_trials=subject_trials, post_metacog=True))

    print pre_metacog_switches
    print post_metacog_switches

    print np.mean(pre_metacog_switches[0])
    print np.mean(pre_metacog_switches[1])
    print np.mean(pre_metacog_switches[2])

    print np.mean(post_metacog_switches[0])
    print np.mean(post_metacog_switches[1])
    print np.mean(post_metacog_switches[2])

    s0=sum(post_metacog_switches[0])
    s1=sum(post_metacog_switches[1])
    print s0, s1


    print pre_met_swi_rews
    print post_met_swi_rews

    print np.mean(post_met_swi_rews[0]), np.mean(post_met_swi_rews[1])

    normdif0=np.array(post_metacog_switches[0])-np.array(post_met_swi_rews[0])
    normdif1=np.array(post_metacog_switches[1])-np.array(post_met_swi_rews[1])

    print normdif0
    print normdif1
    print np.mean(normdif0), np.mean(normdif1)



    if model:

        #MCMC inference for rate difference
        modeldata=np.array([post_metacog_switches[0],post_metacog_switches[1]])
        #modeldata=np.array([post_met_swi_rews[0],post_met_swi_rews[1]]) #this is dubious, but good, nonsignificant
        #modeldata=np.array([normdif0,normdif1]) #this does not work, negative values.. should adapt model for negative reward triggering switch.

        model=pymc.MCMC(rateDifferenceModel.make_model(modeldata, subject_trials))
        model.sample(iter=1000, burn=100, thin=10, progress_bar=False)

        #theta0_m=np.mean(model.trace('theta0')[:],0)    
        #theta1_m=np.mean(model.trace('theta1')[:],0)
        #delta_m=np.mean(model.trace('delta')[:],0)
        #delta_std=np.std(model.trace('delta')[:])
        
        #model.trace('delta')


        # print '\nresults\n{0}, {1}\n dif: {2} +/- {3}'.format(theta0_m, theta1_m, delta_m, delta_std)
        # deltas=model.trace('delta')[:]
        # print 'aproximate pvalue from bayesian inference: {0}'.format(float(sum(deltas<0))/len(deltas))

        # p=0.057
        print 'pvalue from ttest: {0}'.format(stats.ttest_rel(post_metacog_switches[0],post_metacog_switches[1])[1])
        print 'same for rewards (pvalue from ttest): {0}'.format(stats.ttest_rel(post_met_swi_rews[0], post_met_swi_rews[1])[1])
        print '...and subtracted: {0}'.format(stats.ttest_rel(normdif0, normdif1)[1])
        
        deltas=model.trace('delta')[:,:]
        mdeltas=np.mean(deltas,0)
        print 'supermean deltas: {0}'.format(np.mean(mdeltas))
        
        # p=0.058
        print 'pvalue for deltas != 0 from ttest: {0}'.format(stats.ttest_1samp(mdeltas, 0))

        plt.hist(np.mean(deltas,0))
        plt.show()

        utils.plot_and_correlate(difficulties[0],mdeltas) 
        utils.plot_and_correlate(difficulties[0],pre_metacog_switches[0])
        utils.plot_and_correlate(difficulties[0],post_metacog_switches[0])
        utils.plot_and_correlate(difficulties[0],post_metacog_switches[1])
        utils.plot_and_correlate(generosities[0],mdeltas) 
        utils.plot_and_correlate(generosities[0],pre_metacog_switches[0])
        utils.plot_and_correlate(generosities[0],post_metacog_switches[0])
        utils.plot_and_correlate(generosities[0],post_metacog_switches[1])

        utils.plot_and_correlate(generosities[0], difficulties[0])
        fig = plt.figure()
        ax = Axes3D(fig)
        Axes3D.scatter(ax, difficulties[0], generosities[0], mdeltas, cmap=cm.jet)
        Axes3D.plot_trisurf(ax, difficulties[0], generosities[0], mdeltas, cmap=cm.jet)
        plt.show()





def main():


    # ANALYSES
    #global_analysis()

    block_analysis(model=True)

    


if __name__ == '__main__':

 
    main()
