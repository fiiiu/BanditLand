


import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def binned_average(pairs, nbins=10):
    xs=[pair[0] for pair in pairs]
    ys=[pair[1] for pair in pairs]
    start=np.floor(min(xs))
    stop=np.ceil(max(xs)+0.001)
    bins=np.linspace(start,stop,nbins+1)
    inds=np.digitize(xs,bins)#,right=True)
    sums=np.zeros(nbins)
    nums=np.zeros(nbins)
    for i in range(len(ys)):
        sums[inds[i]-1]+=ys[i]
        nums[inds[i]-1]+=1
    bave=np.where(nums>0, sums/nums, 0)
    bcenters=[(bins[i+1]+bins[i])/2 for i in range(len(bins)-1)]
    return bave, bcenters, nums
    


def plot_and_correlate(x, y):
    rtest=stats.pearsonr(x, y)
    print "correlation r:{0}, p:{1}".format(rtest[0],rtest[1])
    plt.plot(x, y, 'o')
    plt.xlim([0,1])
    plt.ylim([0,1.01])
    plt.show()