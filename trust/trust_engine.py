class TrustEngine:

    def __init__(self):

        # fake trust table (real research → learnable model later)
        self.channel_trust = {
            0: 0.9,
            1: 0.7,
            2: 0.6,
            3: 0.8,
            4: 0.95,
            5: 0.5,
            6: 0.85,
            7: 0.2,   # suspicious
            8: 0.1,   # very unsafe
            9: 0.75
        }

    def score(self, actions):

        scored = []

        for a in actions:

            trust = self.channel_trust.get(a, 0.5)

            scored.append((a, trust))

        # sort by trust (high → low)
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored