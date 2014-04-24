
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import griddata
import numpy as np
import cPickle


agent='optimal'
agent='successrate'
step=0.14
n_realizations=15
n_trials=16
filename='Input/nswitches_{3}_{0}step_{1}trials_{2}reals.pkl'.format(step, n_trials, n_realizations, agent)

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



print ave_switches


 # griddata and contour.     
xi = np.linspace(min(difficulties),max(difficulties),15)
yi = np.linspace(min(generosities),max(generosities),15)
xi = np.linspace(0,1,15)
yi = np.linspace(0,1,15)

print len(difficulties), len(generosities), len(ave_switches)

zi = griddata(difficulties,generosities,ave_switches,xi,yi,interp='nn')#linear')

#plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
plt.contourf(xi,yi,zi,cmap=cm.jet)#,
             #norm=plt.normalize(vmax=abs(zi).max(), vmin=-abs(zi).max()))

plt.scatter(difficulties, generosities, marker='s', c=ave_switches, s=200, cmap=cm.jet)
plt.colorbar() # draw colorba
plt.xlim([0,1])
plt.ylim([0,1])
plt.show()