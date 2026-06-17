class PolicyInterpreter:

    def filter(self, actions):
        safe = []
        blocked = []

        for a in actions:
            if a in [7, 8]:   # simulate unsafe actions
                blocked.append(a)
            else:
                safe.append(a)

        return safe, blocked