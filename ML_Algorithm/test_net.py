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
        for x in range(n):
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


def main():
    model = Model(action_num=2, in_size=2)
    X=[1,2]
    model.
if __name__ == '__main__':
    main()
