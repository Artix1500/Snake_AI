import random
from keras.models import Sequential
from keras.layers import Dense


class Model:

    def __init__(self, action_num=4, in_size=11):
        self.in_size = in_size
        self.out_size = action_num
        self.model = self.build_model(self.in_size, 4, self.out_size)

    def build_model(self, in_size, in_between, out_size):
        model = Sequential()
        model.add(Dense(in_between, activation="relu", input_dim=in_size))
        model.add(Dense(in_between, activation="relu"))
        model.add(Dense(out_size, activation="relu"))
        return model

    def train(self, n=200, x=[], y=[]):
        for x in range(n):
            self.model.train(x, y)

    # Predicts for a state from model
    # Returns prediction
    def predict(self, x):
        ret = self.model.predict(x)
        # plus 1 because keys in dictionary are between 1 to 4
        return (ret.argmax()) + 1

    # Gets weights for model from file
    # Returns true if success
    def load_model(self):
        return False

    # Saves weights of trained model to file->path is path to that file
    # Returns true if success
    def save_model(self, path):
        return False
