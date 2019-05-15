import numpy as np
import random
from collections import deque

from Model import Model


class Agent:

    def __init__(self): 
        self.model = Model()
        self.previous_state = None
        self.previous_action = None
        # state, reward, action
        # should be state, reward, action, state_new, done
        self.state_list = deque(maxlen=10000)
        self.predict_counter = 0

        self.batch_size = 1024
        self.mini_batch_size = 32

    def get_action(self, state, previous_reward, game_over=False):
        # reshape says that it is just one sample
        # -1 means that it will fit the size to make it right
        self.predict_counter += 1
        if(self.predict_counter  % 1050 == 0):
            self.train()
        output_state = np.asarray(state).reshape(1, -1)
        if self.previous_state is not None:
            self.state_list.append((self.previous_state, previous_reward, self.previous_action))
        if game_over:
            print ("Game over!")
            return
        self.previous_state = output_state
        self.previous_action = self.model.predict(output_state)
        return self.previous_action

    def get_batch():
        return random.sample(list(self.state_list), self.batch_size)

    def train(self):
        batch = self.get_batch()
        for i in range(self.batch_size/self.mini_batch_size):
            self.model.train(batch[i*self.mini_batch_size:(i+1)*self.mini_batch_size])
        self.model.decreaseEpsilon()
