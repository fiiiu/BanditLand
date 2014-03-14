
import parameters
import OptimalPlayer
import SuccessRatePlayer
import RandomPlayer
import TextHumanPlayer
import GraphicalHumanPlayer

        
def create_player(player_choice):
    if player_choice==-1:
        return GraphicalHumanPlayer.GraphicalHumanPlayer()
    elif player_choice==0:
        return TextHumanPlayer.TextHumanPlayer()
    elif player_choice==1:
        return RandomPlayer.RandomPlayer()
    elif player_choice==2:
        return SuccessRatePlayer.SuccessRatePlayer()
    elif player_choice==3:
        return OptimalPlayer.OptimalPlayer()


def player_type(player_choice):
    if player_choice==-1:
        return "Graphical Human"
    if player_choice==0:
        return "Text Human"
    elif player_choice==1:
        return "Random"
    elif player_choice==2:
        return "Success Rate"
    elif player_choice==3:
        return "Optimal"

