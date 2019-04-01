import sys

sys.path.append('D:\studia\Projekty\ML\Snake_AI')

from game import snake as s
#from game import Game

import tensorflow as tf


def trainNetwork(model):
    #snak = game.Snake(1,1)
    #snak.run_game()
    #game_state = snak.display_log()

    #print(game_state)
    game = s.Game()
    while game.running:
        game.run(3)
        print(game1.game_state)

def buildmodel():
    model = 0
    return model


def playGame():
    model = buildmodel()
    trainNetwork(model)


def main():
    playGame()


if __name__ == "__main__":
    main()
