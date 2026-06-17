class NetworkChain:
    def __init__(self):
        self.nodes = []

    def broadcast(self, block):
        for n in self.nodes:
            n.receive(block)

    def consensus(self):
        return "POW-lite consensus ok"