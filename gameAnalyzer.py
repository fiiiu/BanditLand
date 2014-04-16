
import BanditGameData
import parameters


def n_switches(bandit_game_data, from_trial=0, until_trial=parameters.n_trials):
    switches=0
    for i in range(from_trial, until_trial-1):
        if bandit_game_data.choices[i+1] != bandit_game_data.choices[i]:
            switches+=1
    #print len(range(from_trial, until_trial-1)) #check amount of comparisons
    return switches


def metacog_switches(bandit_game_data, post_metacog=False):
    if not post_metacog:
        return n_switches(bandit_game_data, from_trial=0, until_trial=parameters.n_trials/2)
    else:
        # here I include the potential switch right after the metacog prompt
        return n_switches(bandit_game_data, from_trial=parameters.n_trials/2-1, until_trial=parameters.n_trials)
