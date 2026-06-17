import numpy as np
from collections import deque
import random

class FederatedBuffer:
    def __init__(self, max_size=1000):
        self.buffer = deque(maxlen=max_size)

    def add(self, state, action, reward, next_state=None, client_id=0):

        self.buffer.append({
            "state": self._safe(state),
            "action": int(action),
            "reward": float(reward),
            "next_state": self._safe(next_state),
            "client_id": int(client_id)
        })

    def store(self, data):
        self.add(
            data["state"],
            data["action"],
            data["reward"],
            data.get("next_state", None),
            data.get("client_id", 0)
        )

    def sample(self, batch_size):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))

        states = np.array([b["state"] for b in batch], dtype=np.float32)
        actions = np.array([b["action"] for b in batch], dtype=np.int32)
        rewards = np.array([b["reward"] for b in batch], dtype=np.float32)
        next_states = np.array([b["next_state"] for b in batch], dtype=np.float32)
        client_ids = np.array([b["client_id"] for b in batch], dtype=np.int32)

        return states, actions, rewards, next_states, client_ids

    def size(self):
        return len(self.buffer)

    def _safe(self, x):
        if x is None:
            return np.zeros(1, dtype=np.float32)
        if hasattr(x, "tolist"):
            return np.array(x).astype(np.float32)
        return np.array(x, dtype=np.float32)