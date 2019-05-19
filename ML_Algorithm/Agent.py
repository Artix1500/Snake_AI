import numpy as np
import random
from collections import deque

from Model import Model


class Agent:

    def __init__(self, playWithoutTrainingCount=1050): 
        
        # you can add path to save the model here
        self.model = Model()

        self.previous_state = None
        self.previous_action = None

        self.state_list = deque(maxlen=10000)
        self.predict_counter = 0

        self.batch_size = 0
        self.mini_batch_size = 0

        self.playWithoutTrainingCount = playWithoutTrainingCount

    

    def get_action(self, state, previous_reward, game_over=False):
        self.predict_counter += 1

        self.batch_size+=1
        #if(self.predict_counter  % self.playWithoutTrainingCount == 0):
        #    self.train()
        if self.previous_state is not None:
            self.add_to_state_list(self.previous_state, previous_reward,self.previous_action, state, game_over)
        if game_over:
            print ("Game over!")
            # if game has ended the next_state is None
            self.add_to_state_list(self.previous_state, previous_reward,self.previous_action, None, game_over)
            self.mini_batch_size= min(32, max(1,(int)(self.batch_size/4)))
            self.train()
            self.mini_batch_size=0
            self.batch_size=0
            return
        
        # state in next iteration becomes previous_state
        self.previous_state = state
        # get the move prediction from state
        self.previous_action = self.model.predict(np.asarray(state).reshape(1, -1))
        return self.previous_action

    def add_to_state_list(self, previous_state, previous_reward, previous_action, state_new, done):
        self.state_list.append({'previous_state':np.asarray(previous_state).reshape(1, -1), \
                                'reward': previous_reward, \
                                'action': previous_action, \
                                'next_state': np.asarray(state_new).reshape(1, -1), \
                                'done': done})

    def get_batch(self):
        return random.sample(list(self.state_list), self.batch_size)

    def train(self):
        if self.batch_size>2:
            batch = self.get_batch()
            for i in range((int)(self.batch_size/self.mini_batch_size)):
               self.model.train(batch[i*self.mini_batch_size:(i+1)*self.mini_batch_size])
            self.model.decreaseEpsilon()
