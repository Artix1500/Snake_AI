import sys

sys.path.append('D:\studia\Projekty\ML\Snake_AI')

# for snake(snaky)
from game import snake as game
import cv2

# for tensor
import numpy as np
import random
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Activation


def build_model(in_size, in_between, out_size):
    model = Sequential()
    model.add(Dense(in_between, activation="relu", input_shape=(in_size,)))
    model.add(Dense(in_between, activation="relu"))
    model.add(Dense(out_size, activation="relu"))
    return model


class Model:

    def __init__(self, action_num=4, in_size=9):
        # if we use square state
        self.in_size = in_size
        self.out_size = action_num
        self.model = build_model(self.in_size, 4, self.out_size)

    # Trains model for n epochs with data: X and Y
    def train(self, n=200, x=[], y=[]):
        for x in [1, n]:
            self.model.train(x, y)

    # Predicts for a state from model
    # Returns prediction
    def predict(self, state):
        #return self.model.predict(state)
        return random.randint(1,4)
    # Gets weights for model from file
    # Returns true if success
    def load_model(self):
        return false

    # Saves weights of trained model to file->path is path to that file
    # Returns true if success
    def save_model(self, path):
        return false


class Agent:

    def __init__(self):
        self.model = Model()

    def get_action(self, state):
        return self.model.predict(state)

    def train(self):
        self.model.train()


def main():
    run_agent = Agent()
    state = []
    game_count = 4
    for x in [0,game_count]:

        main_game = game.Game()
        while main_game.running:
            old_state = state
            state = main_game.run(run_agent.get_action(old_state))


if __name__ == '__main__':
    main()
