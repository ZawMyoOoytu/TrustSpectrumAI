import numpy as np

class NetworkEnv:
    def __init__(self, simulator):
        self.sim = simulator

        # 🔥 REAL internal state (not dict)
        self.current_load = 0.5
        self.signal_noise_ratio = 1.0
        self.interference_level = 0.2
        self.user_density = 0.3

    def reset(self):
        self.current_load = np.random.uniform(0.3, 0.7)
        self.signal_noise_ratio = np.random.uniform(0.8, 1.2)
        self.interference_level = np.random.uniform(0.1, 0.5)
        self.user_density = np.random.uniform(0.2, 0.6)

        return self._get_obs()

    def step(self, action, jammer_power):

        result = self.sim.step(action, jammer_power)

        # 🔥 update internal dynamics (REAL SYSTEM BEHAVIOR)
        self.current_load += 0.01 * action
        self.signal_noise_ratio -= 0.01 * jammer_power
        self.interference_level += 0.005 * jammer_power
        self.user_density = np.clip(self.user_density + np.random.normal(0, 0.01), 0, 1)

        reward = (
            result["throughput"] / 100
            - result["loss"]
            - result["latency"] / 100
        )

        return self._get_obs(), reward, result

    def _get_obs(self):
        return np.array([
            self.current_load,
            self.signal_noise_ratio,
            self.interference_level,
            self.user_density
        ], dtype=np.float32)