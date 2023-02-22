# Computer assignment 3
# A code written by Nicole Adamah & Sofia Nilsson

from pokerview import *
from pokermodel import *
import sys

player_1 = "Player 1" # insert name of player one here
player_2 = "Player 2" # insert name of player two here
starting_money = 100 # insert money of choice for the games start

# Lets test it out
app = QApplication(sys.argv)
game = TexasHoldEm([PlayerModel(starting_money, player_1), PlayerModel(starting_money, player_2)])

view = GameView(game)
view.show()

app.exec_()
