import random
from keras.models import Sequential
from keras.layers import Dense
from keras import losses
from keras.initializers import RandomNormal
import numpy as np
import os

from collections import deque

class Model:

    # aplpha - learning rate, is not used 
    # gamma - how much it will want to have rewards
    def __init__(self, action_num=4, in_size=8, epsilon=0,epsilon_rate=0.9994, gamma=0.2, path_saved_weights='model.h5'):
        self.in_size = in_size
        self.out_size = action_num
        self.model = self.build_model(self.in_size, 14, self.out_size)
        self.compileModel()
        self.epsilon = epsilon
        self.epsilon_rate = epsilon_rate
        self.min_epsilon = 0
        self.gamma=gamma

        self.path_saved_weights = path_saved_weights
        self.load_model(self.path_saved_weights)

    
    
    def compileModel(self):
        self.model.compile(loss=losses.mean_squared_error, optimizer='adam', metrics=['accuracy'])

    def build_model(self, in_size, in_between, out_size):
        model = Sequential()
        model.add(Dense(in_between, activation="sigmoid",kernel_initializer=RandomNormal(stddev=1),
           bias_initializer=RandomNormal(stddev=1), input_dim=in_size))
        model.add(Dense(in_between, activation="sigmoid",kernel_initializer=RandomNormal(stddev=1),
           bias_initializer=RandomNormal(stddev=1)))
        model.add(Dense(out_size, activation="softmax",kernel_initializer=RandomNormal(stddev=1),
           bias_initializer=RandomNormal(stddev=1)))
        return model

    # Trains the model with q-learning algorythm
    # takes the minibatch(of size 32 preferably)
    def train(self, minibatch):

        #print("starts minibatch training")
        
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
            
            # print("xxxxxx ===============")
            # print(state)
            # print(action)
            # print(state_new)
            # print(reward)
            # y_train is now a vector of the size of outoput of network
            # OR  predicted=self.model.predict(state_new)[0] but with checking if it exists
            # I think there should be predicted = [0,0,0,0]
            predicted=self.model.predict(state)[0]
            y_train.append(predicted)
            # only for the action chosen we change value (Bellman equation?)
            if done:
                y_train[i][action]=reward
            else:
                y_train[i][action]=(1-self.gamma)*reward+self.gamma*np.max(self.model.predict(state_new))
                #OR (1-gamma)*reward 
        
        x_train=np.asarray(x_train).reshape(len(minibatch), -1)
        y_train=np.asarray(y_train).reshape(len(minibatch), -1)
        # if(len(minibatch) <= 2):
        #     print("-==-=--=-=-=-=--==-=-=-=-=-=-=-=-=-=-=-=-==")
        #     print(x_train)
        #     print(y_train)
        self.model.fit(x_train,
                        y_train,
                           batch_size=len(minibatch),
                           epochs=2,
                           verbose=2)
        # if(len(minibatch) <= 2):
        #     print(self.model.predict(x_train))
        
        if(len(minibatch) > 2):
            self.save_model(self.path_saved_weights)
    # Predicts for a state from model
    # Returns prediction
    def predict(self, x):
        if (random.random() < self.epsilon):
            toRet = random.randint(0, 3)
            if(x[0][toRet] == 0): 
                print('random Move kills')
            return toRet
        else:
            ret = self.model.predict(x)
            # print('state:')
            # print(x)
            # print("predicted: ")
            # print(ret) 
            toRet = ret.argmax()
            if(x[0][toRet] == 0): 
                print('predicted Move kills')
            return toRet 

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
