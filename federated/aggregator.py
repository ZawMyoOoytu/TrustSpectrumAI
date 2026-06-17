import numpy as np

class FedAvgPlus:
    def aggregate(self, client_updates):
        # client_updates = list of (weight, reward)
        weights = np.array([c[0] for c in client_updates])
        rewards = np.array([c[1] for c in client_updates])

        return {
            "global_reward": float(np.mean(rewards)),
            "confidence": float(np.mean(weights))
        }