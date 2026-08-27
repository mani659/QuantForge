import json
import os
from typing import Dict, Any

class EventLedger:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                pass

    def record_event(self, record: Dict[str, Any]):
        """
        Record must contain:
        - candidate_id
        - contract_version
        - contract_hash
        - event_id
        - instrument
        - utc_timestamp
        - ny_timestamp
        - event_state
        - source_timestamp
        - event_completion_timestamp (optional)
        - theoretical_entry
        - modeled_paper_entry (optional)
        - bid, ask, spread
        - detection_latency
        - runner_instance_id
        - process_session_id
        - connection_state
        - reason_code
        """
        with open(self.filepath, 'a') as f:
            f.write(json.dumps(record) + '\n')

    def get_all_records(self):
        records = []
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        return records
