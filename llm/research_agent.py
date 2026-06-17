class ResearchAgent:
    def propose_experiment(self):
        return {
            "change_trust_weight": 0.1,
            "change_threat_scale": 0.2
        }

    def analyze(self, logs):
        return "increase trust sensitivity"