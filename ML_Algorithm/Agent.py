import numpy as np
import random
from collections import deque

from Model import Model


class Agent:

    def __init__(self): 
        self.model = Model()
        self.previous_state = None
        self.previous_action = None
        # state, reward, action, first Q value
        self.state_list = deque(maxlen=10000)
        self.predict_counter = 0
        self.Q_first_value= 0
        
    def get_action(self, state, previous_reward):
        # reshape says that it is just one sample
        # -1 means that it will fit the size to make it right
        self.predict_counter += 1
        output_state = np.asarray(state).reshape(1, -1)
        if self.previous_state is not None:
            self.state_list.append((self.previous_state, previous_reward, self.previous_action,self.Q_first_value))
        self.previous_state = output_state
        self.previous_action = self.model.predict(output_state)
        return self.previous_action

    def train(self):
        self.model.train()
        self.model.decreaseEpsilon()
