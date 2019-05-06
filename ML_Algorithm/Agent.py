import numpy as np

from Model import Model

class Agent:

    def __init__(self):
        self.model = Model()

    def get_action(self, state):
        output_state = np.asarray(state)
        # reshape says that it is just one sample
        # -1 means that it will fit the size to make it right
        return self.model.predict(output_state.reshape(1, -1))

    def train(self):
        self.model.train()