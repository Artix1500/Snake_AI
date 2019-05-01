import random
from keras.models import Sequential
from keras.layers import Dense

class Model:

    def __init__(self, action_num=4, in_size=9):
        self.in_size = in_size
        self.out_size = action_num
        self.model = self.build_model(self.in_size, 4, self.out_size)

    def build_model(self, in_size, in_between, out_size):
        model = Sequential()
        model.add(Dense(in_between, activation="relu", input_shape=(in_size,)))
        model.add(Dense(in_between, activation="relu"))
        model.add(Dense(out_size, activation="relu"))
        return model

    def train(self, n=200, x=[], y=[]):
        for x in range(n):
            self.model.train(x, y)

    # Predicts for a state from model
    # Returns prediction
    def predict(self, state, reward):
        #return self.model.predict(state)
        return random.randint(1,4)

    # Gets weights for model from file
    # Returns true if success
    def load_model(self):
        return False

    # Saves weights of trained model to file->path is path to that file
    # Returns true if success
    def save_model(self, path):
        return False