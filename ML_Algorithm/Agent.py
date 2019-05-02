import numpy as np

from Model import Model

class Agent:

    def __init__(self):
        self.model = Model()

    def get_action(self, state):
        output_state = np.asarray(state)
        print(output_state)
        return self.model.predict(output_state)

    def train(self):
        self.model.train()