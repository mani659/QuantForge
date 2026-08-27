import json
import time

class SupervisorHealthMonitor:
    def __init__(self, ledger_path: str):
        self.ledger_path = ledger_path

    def record_heartbeat(self, data: dict):
        # We append a JSON line
        try:
            with open(self.ledger_path, "a") as f:
                json.dump(data, f)
                f.write("\n")
                f.flush()
        except Exception:
            pass
