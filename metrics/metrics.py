# metrics/metrics.py
class MetricsEngine:
    def __init__(self):
        self.history = []
        self.last_result = {"latency": 20, "throughput": 50, "loss": 0.3}
        self.summary_data = {"avg_latency": 0, "avg_throughput": 0, "avg_loss": 0, "samples": 0}
    
    def get_last(self):
        """နောက်ဆုံး result ကို ပြန်ပေး"""
        return self.last_result
    
    def log(self, result):
        """Result ကို သိမ်းဆည်း"""
        self.last_result = result
        self.history.append(result)
    
    def summary(self):
        """ပျမ်းမျှတွက်ပြီး ပြန်ပေး"""
        if not self.history:
            return self.summary_data
        
        n = len(self.history)
        self.summary_data = {
            "avg_latency": sum(h["latency"] for h in self.history) / n,
            "avg_throughput": sum(h["throughput"] for h in self.history) / n,
            "avg_loss": sum(h["loss"] for h in self.history) / n,
            "samples": n
        }
        return self.summary_data