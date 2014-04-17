

import BanditGame
import numpy

n_optimal_realizations=2

bg=BanditGame.BanditGame()

bg.player_select(3)
opt_average_reward=[]
for i in range(n_optimal_realizations):
    opt_average_reward.append(bg.play())
    bg.reset()
    
#print opt_average_reward
print "Optimal Player average average reward = {0}".format(numpy.mean(opt_average_reward))


bg.player_select(2)
sr_average_reward=[]
for i in range(1000):
    sr_average_reward.append(bg.play())
    bg.reset()
    
#print sr_average_reward
print "Success Rate Player average average reward = {0}".format(numpy.mean(sr_average_reward))


bg.player_select(1)
rnd_average_reward=[]
for i in range(1000):
    rnd_average_reward.append(bg.play())
    bg.reset()
    
#print sr_average_reward
print "Random Player average average reward = {0}".format(numpy.mean(rnd_average_reward))


