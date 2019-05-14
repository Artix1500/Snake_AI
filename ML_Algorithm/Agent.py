import numpy as np
import random

from Model import Model


class Agent:

    def __init__(self,
                 epsilon=1,
                 epsilon_rate=0.97):

        self.epsilon = epsilon
        self.epsilon_rate = epsilon_rate
        self.min_epsilon = 0.2
        self.model = Model()

    def get_action(self, state):
        output_state = np.asarray(state)
        q_values = self.model.predict(output_state.reshape(1, -1))

        if (random.random() < self.epsilon):
            return random.randint(1, 4)
        else:
            return q_values

    def train(self):
        self.model.train()
        self.decreaseEpsilon()

    def decreaseEpsilon(self):
        self.epsilon = self.epsilon * self.epsilon_rate
        if self.epsilon < self.min_epsilon:
            self.epsilon = self.min_epsilon
