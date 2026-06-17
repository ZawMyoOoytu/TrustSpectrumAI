class RewardFusion:
    def compute(self, reward, trust, threat):
        return float(
            0.5 * reward +
            0.3 * trust -
            0.2 * threat
        )