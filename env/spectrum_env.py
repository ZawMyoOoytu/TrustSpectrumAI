import numpy as np

class SpectrumEnv:

    def __init__(self):
        self.state_size = 5

    def reset(self):
        return np.random.rand(self.state_size)

    def step(self, action):

        reward = np.random.uniform(0, 1)
        next_state = np.random.rand(self.state_size)

        done = False

        return next_state, reward, done