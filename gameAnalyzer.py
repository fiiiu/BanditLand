
import BanditGameData


def n_switches(bandit_game_data, from_trial, until_trial):
    switches=0
    for i in range(from_trial, until_trial-1):
        if bandit_game_data.choices[i+1] != bandit_game_data.choices[i]:
            switches+=1
    #print len(range(from_trial, until_trial-1)) #check amount of comparisons
    return switches


def metacog_switches(bandit_game_data, n_trials, post_metacog=False):
    if not post_metacog:
        return n_switches(bandit_game_data, from_trial=0, until_trial=n_trials/2)
    else:
        # here I include the potential switch right after the metacog prompt
        return n_switches(bandit_game_data, from_trial=n_trials/2-1, until_trial=n_trials)

def metacog_rewards(bandit_game_data, n_trials, post_metacog=False):
    if not post_metacog:
        return n_rewards(bandit_game_data, from_trial=0, until_trial=n_trials/2-1)
    else:
        # count the pre-metacog reward which might prompt first switch, exclude last.
        return n_rewards(bandit_game_data, from_trial=n_trials/2-1, until_trial=n_trials-1)


def n_rewards(bandit_game_data, from_trial, until_trial):
    return sum(bandit_game_data.rewards[from_trial:until_trial])


def p_estimates_at_report(bandit_game_data, n_trials):
    wins=[0,0]
    plays=[0,0]
    for i in range(n_trials/2):
        wins[bandit_game_data.choices[i]]+=bandit_game_data.rewards[i]
        plays[bandit_game_data.choices[i]]+=1
    if plays[0]!=0 and plays[1]!=0:
        return (float(wins[0])/plays[0],float(wins[1])/plays[1])    
    else:
        print 'cannot compute estimates, only one machine played. FAKING'
        return (0.5,-1)
