import sys

sys.path.append('D:\studia\Projekty\ML\Snake_AI')

# for snake(snaky)
from game import snake as game
import cv2

# for tensor
import numpy as np
import random
from collections import deque


# Based on NIPS 2013
class DQN:
    def __init__(self, ACTIONS):
        self.actions = ACTIONS
        self.initConvNet()
        self.initNN()

    def initConvNet(self):
        print("initConvNet")

    def initNN(self):
        print("initNN")

    def train(self):
        print("TRAIN")

    def initState(self, state):
        print("Initial State")

    def addReplay(self):
        print ("Add Replay")

    def getAction(self):
        idx = random.randrange(self.actions)
        action[idx] = 1
        return action


class agent:
    def run(self):
        model = DQN(4)
        g = game.gameState()
        a_0 = np.array([1, 0, 0, 0])  # init move
        g.frameStep(a_0)  # image_data, reward, done
        model.initState(s_0)
        while True:
            a = model.getAction()
            data1,done = g.frameStep(a)  # image_data, reward, done
            if done:
                sc, ep = g.retScore()
                print(ts, ",", qv, ",", ep, ",", sc)
            else:
                print(ts, ",", qv, ",,")


def main():
    run_agent = agent()
    run_agent.run()


if __name__ == '__main__':
    main()
