import time
import json
import os
from typing import Dict, Any

class HealthMonitor:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()
        self.start_time = time.time()
        self.disconnect_count = 0
        self.reconnect_count = 0
        self.current_outage_start = None

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                pass

    def record_heartbeat(self, runner_id: str, connection_state: str, 
                         last_quote_ts: float, cand_states: Dict[str, str]):
        uptime = time.time() - self.start_time
        
        outage_duration = 0
        if connection_state == "DISCONNECTED" and self.current_outage_start:
            outage_duration = time.time() - self.current_outage_start

        record = {
            "utc_timestamp": time.time(),
            "runner_instance_id": runner_id,
            "uptime_seconds": uptime,
            "connection_state": connection_state,
            "last_quote_timestamp": last_quote_ts,
            "candidate_states": cand_states,
            "disconnect_count": self.disconnect_count,
            "reconnect_count": self.reconnect_count,
            "current_outage_duration": outage_duration
        }

        with open(self.filepath, 'a') as f:
            f.write(json.dumps(record) + '\n')

    def mark_disconnect(self):
        self.disconnect_count += 1
        self.current_outage_start = time.time()

    def mark_reconnect(self):
        self.reconnect_count += 1
        self.current_outage_start = None
