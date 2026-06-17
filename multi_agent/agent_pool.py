import random

class AgentPool:
    def __init__(self, n_agents=3):
        self.n_agents = n_agents

    # ✅ THIS IS THE FUNCTION YOU ARE CALLING
    def propose(self):
        proposals = []
        for _ in range(self.n_agents):
            proposals.append(random.sample(range(10), 5))
        return proposals

    def vote(self, scored_list):
        score_map = {}

        for ranking in scored_list:
            for item in ranking:
                a = item[0]
                score = item[1]
                score_map[a] = score_map.get(a, 0) + score

        return max(score_map.items(), key=lambda x: x[1])[0]