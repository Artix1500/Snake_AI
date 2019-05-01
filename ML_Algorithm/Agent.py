from Model import Model

class Agent:

    def __init__(self):
        self.model = Model()

    def get_action(self, state, reward):
        return self.model.predict(state, reward)

    def train(self):
        self.model.train()