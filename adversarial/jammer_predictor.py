import random

class JammerPredictor:

    def __init__(self):

        # fake attack probability per channel
        self.attack_map = {
            0: 0.1,
            1: 0.3,
            2: 0.4,
            3: 0.2,
            4: 0.25,
            5: 0.5,
            6: 0.15,
            7: 0.9,   # highly attacked
            8: 0.95,  # very dangerous
            9: 0.35
        }

    def predict(self, action):

        return self.attack_map.get(action, random.uniform(0, 1))