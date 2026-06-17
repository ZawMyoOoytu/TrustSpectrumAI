class MetaOptimizer:
    def __init__(self):
        self.alpha = 0.5
        self.history = []

    # ✅ THIS IS REQUIRED BY main.py
    def update(self, reward):
        self.history.append(reward)

        if len(self.history) >= 5:
            avg = sum(self.history[-5:]) / 5

            if avg < 0.4:
                self.alpha += 0.05
            else:
                self.alpha -= 0.02

        # clamp value (IMPORTANT for stability)
        self.alpha = max(0.1, min(1.0, self.alpha))

        return self.alpha