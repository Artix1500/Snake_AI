import random
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import os

from collections import deque

class Model:

    # aplpha - learning rate, is not used 
    # gamma - how much it will want to have rewards
    def __init__(self, action_num=4, in_size=8, epsilon=1,epsilon_rate=0.97, gamma=0.9, path_saved_weights='model.h5'):
        self.in_size = in_size
        self.out_size = action_num
        self.model = self.build_model(self.in_size, 4, self.out_size)
        self.compileModel()
        self.epsilon = epsilon
        self.epsilon_rate = epsilon_rate
        self.min_epsilon = 0.2
        self.gamma=gamma

        self.path_saved_weights = path_saved_weights
        self.load_model(self.path_saved_weights)

    
    
    def compileModel(self):
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def build_model(self, in_size, in_between, out_size):
        model = Sequential()
        model.add(Dense(in_between, activation="relu", input_dim=in_size))
        model.add(Dense(in_between, activation="relu"))
        model.add(Dense(out_size, activation="relu"))
        return model

    # Trains the model with q-learning algorythm
    # takes the minibatch(of size 32 preferably)
    def train(self, minibatch):

        print("starts minibatch training")
        
        x_train = []
        y_train = []
        
        for i in range(len(minibatch)):
        
            data_piece=minibatch[i]
            # get state from data_piece as the input
            state=data_piece["previous_state"]
            x_train.append(state)
            # get the reward
            reward = data_piece["reward"]
            # get the action
            action = data_piece["action"]
            # not in the deque yet
            state_new = data_piece["next_state"]
            done = data_piece["done"]
            
            # y_train is now a vector of the size of outoput of network
            # OR  predicted=self.model.predict(state_new)[0] but with checking if it exists
            # I think there should be predicted = [0,0,0,0]
            predicted=self.model.predict(state)[0]
            y_train.append(predicted)
            # only for the action chosen we change value (Bellman equation?)
            if done:
                y_train[i][action]=reward
            else:
                y_train[i][action]=reward+self.gamma*np.max(self.model.predict(state_new))
        
        x_train=np.asarray(x_train).reshape(len(minibatch), -1)
        y_train=np.asarray(y_train).reshape(len(minibatch), -1)
                
        print("fit")
        self.model.fit(x_train,
                        y_train,
                           batch_size=len(minibatch),
                           epochs=1)
        print("end of minibatch training")

        self.save_model(self.path_saved_weights)
    # Predicts for a state from model
    # Returns prediction
    def predict(self, x):
        if (random.random() < self.epsilon):
            return random.randint(0, 3)
        else:
            ret = self.model.predict(x)
            print("predicted: ")
            print(ret)
            return (ret.argmax()) 

    def decreaseEpsilon(self):
        self.epsilon = self.epsilon * self.epsilon_rate
        if self.epsilon < self.min_epsilon:
            self.epsilon = self.min_epsilon

    # Gets weights for model from file
    # Returns true if success
    def load_model(self, filename):

        exists = os.path.isfile(filename)
        if exists:
            print("loading model")
            self.model.load_weights(filename)

    # Saves weights of trained model to file->path is path to that file
    # Returns true if success
    def save_model(self, filename='model.h5'):
        print("saving model")
        self.model.save_weights(filename)
