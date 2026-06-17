import hashlib
import json
import time


class BlockchainLogger:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    # -------------------------
    # GENESIS BLOCK
    # -------------------------
    def create_genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "data": "GENESIS",
            "prev_hash": "0"
        }
        genesis["hash"] = self.hash_block(genesis)
        self.chain.append(genesis)

    # -------------------------
    # HASH FUNCTION
    # -------------------------
    def hash_block(self, block):
        block_copy = block.copy()
        block_copy.pop("hash", None)

        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    # -------------------------
    # ADD BLOCK
    # -------------------------
    def add_block(self, data: dict):

        prev_block = self.chain[-1]

        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "prev_hash": prev_block["hash"]
        }

        block["hash"] = self.hash_block(block)
        self.chain.append(block)

    # -------------------------
    # GET CHAIN
    # -------------------------
    def get_chain(self):
        return self.chain