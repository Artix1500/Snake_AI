import random
from keras.models import Sequential
from keras.layers import Dense


class Model:

    # aplpha - learning rate
    # gamma - how much it will want to have rewards
    def __init__(self, action_num=4, in_size=8, epsilon=1,epsilon_rate=0.97, alpha=0.7, gamma=0.9):
        self.in_size = in_size
        self.out_size = action_num
        self.model = self.build_model(self.in_size, 4, self.out_size)
        self.epsilon = epsilon
        self.epsilon_rate = epsilon_rate
        self.min_epsilon = 0.2
        self.alpha= alpha
        self.gamma=gamma

    def build_model(self, in_size, in_between, out_size):
        model = Sequential()
        model.add(Dense(in_between, activation="relu", input_dim=in_size))
        model.add(Dense(in_between, activation="relu"))
        model.add(Dense(out_size, activation="relu"))
        return model

    # Trains the model with q-learning algorythm
    def train(self, batch):
        x_train = []
        y_train = []
            for data_piece in batch:
                # get state from data_piece as the input
                state=data_piece[0]
                x_train.append(state)
                # get the reward
                reward = data_piece[1]
                # get max predicted
                Q_predicted_max = np.max(self.predict(state))
                # Count the new Q
                Q_old = data_piece[3]
                Q_new=(1-alpha)*Q_old + alpha*(reward+gamma*Q_predicted_max)
                
                data.piece[]
        self.model.fit()


    # Predicts for a state from model
    # Returns prediction
    def predict(self, x):
        if (random.random() < self.epsilon):
            return random.randint(1, 4)
        else:
            ret = self.model.predict(x)
            # plus 1 because keys in dictionary are between 1 to 4
            return (ret.argmax()) + 1

    def decreaseEpsilon(self):
        self.epsilon = self.epsilon * self.epsilon_rate
        if self.epsilon < self.min_epsilon:
            self.epsilon = self.min_epsilon

    # Gets weights for model from file
    # Returns true if success
    def load_model(self, filename=None):
        f = ('model.h5' if filename is None else filename)
        self.model.save_weights(f)

    # Saves weights of trained model to file->path is path to that file
    # Returns true if success
    def save_model(self, path):
        self.model.load_weights(path)

