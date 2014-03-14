

import OptimalPlayer
import SuccessRatePlayer

op=OptimalPlayer.OptimalPlayer()
srp=SuccessRatePlayer.SuccessRatePlayer()

experience=[[11,1],[10,1]]

print op.expected_reward(2,experience[0], experience[1])
print srp.choice_worths(experience[0], experience[1])

