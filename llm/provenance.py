import hashlib
import json

class DecisionProvenance:
    def hash_reason(self, state, action, explanation):
        payload = {
            "state": state,
            "action": action,
            "explanation": explanation
        }

        return hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()