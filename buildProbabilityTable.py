import BanditGameData
import gameAnalyzer
import BanditGame
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.mlab import griddata
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cPickle


payrates=[]
difficulties=[]
generosities=[]

#step=0.14 for subjects
#step=0.14
# for d in np.arange(0,1.001,step):
#     for g in np.arange(0,1.001,step):
#         if -d <= 2*g-1 <= d:
#             pa=(1-d)/2+g
#             pb=2*g-pa
#             payrates.append((pa,pb))
#             difficulties.append(d)
#             generosities.append(g)

nsteps=8
step=1./nsteps


for pa in np.arange(0,1.001, step):
    for pb in np.arange(pa, 1.001, step):
        g=(pa+pb)/2
        d=1-abs(pb-pa)
        payrates.append((pa,pb))
        difficulties.append(d)
        generosities.append(g)



print payrates

pas=[ps[0] for ps in payrates]
pbs=[ps[1] for ps in payrates]

print len(payrates)

save_payrates=False
if save_payrates:
    with open('Input/payrates.txt', 'w') as fhandle:
        for payrate in payrates:
            fhandle.write('{0} {1}\n'.format(payrate[0],payrate[1]))

    exit()


#fig = plt.figure()
#ax = Axes3D(fig)
#Axes3D.scatter(ax, pas, pbs, 1, cmap=cm.jet)
#Axes3D.plot_trisurf(ax, difficulties[0], generosities[0], 1, cmap=cm.jet)
#plt.show()


# fig = plt.figure()
# ax = Axes3D(fig)
# Axes3D.scatter(ax, difficulties, generosities, 1, cmap=cm.jet)
# #Axes3D.plot_trisurf(ax, difficulties[0], generosities[0], mdeltas, cmap=cm.jet)
# plt.show()


#exit()

save=False
plots=True

agent='optimal'
agent='successrate'
n_realizations=15
n_trials=20
bgd=BanditGameData.BanditGameData()
ave_switches=[]
std_switches=[]


for payrate in payrates:
    print 'computing payrate {0}'.format(payrate)
    #bg=BanditGame.BanditGame(p_list=payrate, n_trials=n_trials, player_choice=3)
    if agent=='successrate':
        pchoice=2
    elif agent=='optimal':
        pchoice=3
    bg=BanditGame.BanditGame(p_list=payrate, n_trials=n_trials, player_choice=pchoice)
    n_switches=[]
        
    for i in range(n_realizations):
        choices, rewards=bg.play()
        bgd.load(choices,rewards)
        n_switches.append(gameAnalyzer.metacog_switches(bgd, n_trials, post_metacog=True))
        bg.reset()
    
    print n_switches

    ave_switches.append(np.mean(n_switches))
    std_switches.append(np.std(n_switches))


# print ave_switches
# print std_switches

npave=np.array(ave_switches)
npstd=np.array(std_switches)
print npave[np.array(ave_switches)==np.max(ave_switches)], npstd[np.array(ave_switches)==np.max(ave_switches)]


if plots:
    fig = plt.figure()
    ax = Axes3D(fig)
    Axes3D.scatter(ax, difficulties, generosities, ave_switches, cmap=cm.jet)
    Axes3D.plot_trisurf(ax, difficulties, generosities, ave_switches, cmap=cm.jet)



    # griddata and contour.
    xi = np.linspace(min(difficulties)+step,max(difficulties)-step,1.5/step)
    yi = np.linspace(min(generosities)+step,max(generosities)-step,1.5/step)
    zi = griddata(difficulties,generosities,ave_switches,xi,yi,interp='linear')


    #plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    plt.contourf(xi,yi,zi,cmap=cm.jet)#,
                 #norm=plt.normalize(vmax=abs(zi).max(), vmin=-abs(zi).max()))
    plt.colorbar() # draw colorba
    plt.show()

    plt.scatter(difficulties, generosities, marker='s', c=ave_switches, s=500, cmap=cm.coolwarm)
    plt.colorbar()
    plt.show()



filename='Input/nswitches_{3}_{0}step_{1}trials_{2}reals.pkl'.format(step, n_trials, n_realizations, agent)

#write
if save:
    with open(filename, 'wb') as handle:
      cPickle.dump([difficulties, generosities, ave_switches], handle)



# #read
# with open(filename, 'rb') as handle:
#    data = cPickle.load(handle)

# difficulties=data[0]
# generosities=data[1]
# ave_switches=data[2]
# fig = plt.figure()
# ax = Axes3D(fig)
# Axes3D.scatter(ax, difficulties, generosities, ave_switches, cmap=cm.jet)
# Axes3D.plot_trisurf(ax, difficulties, generosities, ave_switches, cmap=cm.jet)
# plt.show()