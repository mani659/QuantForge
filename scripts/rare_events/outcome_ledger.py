import json
import os
from typing import Dict, Any

class OutcomeLedger:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                pass

    def record_outcome(self, record: Dict[str, Any]):
        """
        Record must contain:
        - candidate_id
        - contract_version
        - contract_hash
        - event_id
        - paper_entry_timestamp
        - paper_entry_price
        - paper_exit_timestamp
        - paper_exit_price
        - gross_result
        - modeled_friction
        - net_result
        - execution_deviation
        - outcome_status
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
