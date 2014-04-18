
import parameters
import OptimalPlayer
import SuccessRatePlayer
import RandomPlayer
import TextHumanPlayer
import GraphicalHumanPlayer

        
def create_player(player_choice, n_trials=None):
    if player_choice==-1:
        return GraphicalHumanPlayer.GraphicalHumanPlayer()
    elif player_choice==0:
        return TextHumanPlayer.TextHumanPlayer()
    elif player_choice==1:
        return RandomPlayer.RandomPlayer()
    elif player_choice==2:
        return SuccessRatePlayer.SuccessRatePlayer()
    elif player_choice==3:
        return OptimalPlayer.OptimalPlayer(n_trials=n_trials)


def player_type(player_choice):
    if player_choice==-1:
        return "GraphicalHuman"
    if player_choice==0:
        return "TextHuman"
    elif player_choice==1:
        return "Random"
    elif player_choice==2:
        return "SuccessRate"
    elif player_choice==3:
        return "Optimal"

