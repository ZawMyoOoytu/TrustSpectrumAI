import random

class DigitalTwin:

    def simulate_attack(self, action):
        """
        action-aware adversarial simulation
        """

        base_attack = random.uniform(0.0, 0.3)

        # stronger attack on certain actions
        if action % 2 == 0:
            base_attack += 0.2

        if action in [7, 8, 9]:
            base_attack += 0.3

        return base_attack