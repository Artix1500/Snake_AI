from game import snake as game
import tensorflow as tf


def trainNetwork(model):
    snak = game.Snake(1,1)
    game_state = snak.display_log()
    print(game_state)


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
