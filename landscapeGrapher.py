
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cPickle



step=0.05
n_realizations=20
n_trials=10
filename='Input/nswitches_successrate_{0}step_{1}trials_{2}reals.pkl'.format(step, n_trials, n_realizations)

# #write
# with open(filename, 'wb') as handle:
#   cPickle.dump([difficulties, generosities, ave_switches], handle)



#read
with open(filename, 'rb') as handle:
   data = cPickle.load(handle)

difficulties=data[0]
generosities=data[1]
ave_switches=data[2]
fig = plt.figure()
ax = Axes3D(fig)
Axes3D.scatter(ax, difficulties, generosities, ave_switches, cmap=cm.jet)
Axes3D.plot_trisurf(ax, difficulties, generosities, ave_switches, cmap=cm.jet)
plt.show()