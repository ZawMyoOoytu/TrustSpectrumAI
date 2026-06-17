import random
import math

class NetworkSimulator:
    """
    Realistic wireless network simulation layer
    (NS-3 lightweight alternative for Python-only system)
    """

    def __init__(self):
        self.base_noise = 0.2

    def interference(self, action: int, jammer_power: float) -> float:
        # frequency collision simulation
        freq_overlap = random.uniform(0.0, 1.0)

        interference = jammer_power * freq_overlap

        # channel randomness
        fading = random.uniform(0.8, 1.2)

        return interference * fading


    def latency(self, interference: float) -> float:
        base_latency = 10  # ms

        delay = base_latency * (1 + interference * 3)

        jitter = random.uniform(0.0, 5.0)

        return delay + jitter


    def throughput(self, interference: float) -> float:
        base_throughput = 100  # Mbps

        degradation = 1 / (1 + interference * 5)

        noise_penalty = random.uniform(0.85, 1.0)

        return base_throughput * degradation * noise_penalty


    def packet_loss(self, interference: float) -> float:
        loss = 1 - math.exp(-interference * 2)

        return min(max(loss, 0.0), 1.0)


    def step(self, action: int, jammer_power: float):
        """
        Returns realistic network metrics
        """

        interference = self.interference(action, jammer_power)

        latency = self.latency(interference)
        throughput = self.throughput(interference)
        loss = self.packet_loss(interference)

        return {
            "interference": interference,
            "latency": latency,
            "throughput": throughput,
            "loss": loss
        }