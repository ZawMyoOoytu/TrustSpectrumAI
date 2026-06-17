import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class DQN(nn.Module):
    def __init__(self, state_dim=1, action_dim=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:

    def __init__(self):
        self.model = DQN()
        self.target = DQN()
        self.target.load_state_dict(self.model.state_dict())

        self.optim = optim.Adam(self.model.parameters(), lr=0.001)

        self.gamma = 0.95
        self.epsilon = 1.0

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 9)

        state = torch.FloatTensor([state])
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def train(self, batch):
        states, actions, rewards, next_states = batch

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze()

        next_q = self.target(next_states).max(1)[0]

        target = rewards + self.gamma * next_q

        loss = nn.MSELoss()(q_values, target.detach())

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        self.epsilon *= 0.995