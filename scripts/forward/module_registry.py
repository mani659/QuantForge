import os
import sys
import json
import time

# Ensure scripts/rare_events path is accessible for frozen modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
rare_events_dir = os.path.join(parent_dir, "rare_events")
sys.path.insert(0, rare_events_dir)

from cand_024_engine import Cand024Engine
from cand_035_engine import Cand035Engine
from event_ledger import EventLedger
from outcome_ledger import OutcomeLedger
from paper_execution import PaperExecutionFirewall

class ForwardModuleWrapper:
    def __init__(self, candidate_id, engine, config, base_runtime_dir):
        self.candidate_id = candidate_id
        self.engine = engine
        self.config = config
        self.module_dir = os.path.join(base_runtime_dir, f"cand_{candidate_id.split('-')[1].lower()}")
        os.makedirs(self.module_dir, exist_ok=True)
        
        self.event_ledger = EventLedger(os.path.join(self.module_dir, "event_ledger.jsonl"))
        self.outcome_ledger = OutcomeLedger(os.path.join(self.module_dir, "outcome_ledger.jsonl"))
        self.paper = PaperExecutionFirewall(friction=2.0)
        
        self.status_file = os.path.join(self.module_dir, "status.json")
        self.stats = {
            "captured_count": 0,
            "missed_count": 0,
            "invalidated_count": 0,
            "completed_count": 0,
            "last_event_timestamp": 0,
            "last_evaluation_timestamp": 0
        }
        self.load_stats()
        
    def load_stats(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r") as f:
                    data = json.load(f)
                    self.stats.update(data.get("stats", {}))
            except Exception:
                pass
                
    def save_stats(self):
        contract = self.engine.contract
        data = {
            "module_id": self.candidate_id,
            "contract_hash": contract.hash,
            "mapping_id": self.config["mapping_id"],
            "current_event_count": self.stats["captured_count"],
            "minimum": self.config["minimum"],
            "target": self.config["target"],
            "stats": self.stats,
            "current_state": self.engine.state,
            "last_write": time.time()
        }
        temp_file = self.status_file + ".tmp"
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_file, self.status_file)
        
    def process_quote(self, quote, instance_id):
        self.stats["last_evaluation_timestamp"] = quote["utc_timestamp"]
        try:
            event = self.engine.evaluate(quote["utc_timestamp"], quote)
            if event:
                self.stats["last_event_timestamp"] = quote["utc_timestamp"]
                contract = self.engine.contract
                
                if event['action'] == "TRIGGER":
                    self.event_ledger.record_event({
                        "candidate_id": contract.candidate_id,
                        "contract_version": contract.version,
                        "contract_hash": contract.hash,
                        "event_id": event['event_id'],
                        "instrument": quote['symbol'],
                        "utc_timestamp": quote['utc_timestamp'],
                        "ny_timestamp": event['ny_time'],
                        "event_state": "EVENT_DETECTED",
                        "theoretical_entry": event['theoretical_entry'],
                        "runner_instance_id": instance_id
                    })
                    
                    paper_res = self.paper.execute_entry(event, quote)
                    
                    if paper_res['status'] == "PAPER_ENTRY_RECORDED":
                        self.engine.state = "IN_POSITION"
                        self.stats["captured_count"] += 1
                        self.event_ledger.record_event({
                            "candidate_id": contract.candidate_id,
                            "event_id": event['event_id'],
                            "event_state": "PAPER_IN_POSITION",
                            "modeled_paper_entry": paper_res['paper_entry_price'],
                            "utc_timestamp": quote['utc_timestamp']
                        })
                        
                elif event['action'] == "EXIT":
                    paper_res = self.paper.execute_exit(event, quote)
                    if paper_res['status'] == "PAPER_EXIT_RECORDED":
                        self.stats["completed_count"] += 1
                        self.outcome_ledger.record_outcome({
                            "candidate_id": contract.candidate_id,
                            "contract_version": contract.version,
                            "contract_hash": contract.hash,
                            "event_id": event['event_id'],
                            "paper_entry_price": paper_res['paper_entry_price'],
                            "paper_exit_price": paper_res['paper_exit_price'],
                            "gross_result": paper_res['gross_result'],
                            "net_result": paper_res['net_result'],
                            "modeled_friction": paper_res['modeled_friction'],
                            "outcome_status": "COMPLETED"
                        })
                        
            self.save_stats()
            return True
        except Exception as e:
            # Module isolation: an error here won't crash the supervisor
            print(f"[{self.candidate_id}] Evaluation error: {e}")
            return False

def get_registry(base_runtime_dir):
    modules = []
    
    # CAND-024
    config_24 = {
        "enabled": True,
        "logical_symbol": "USATECHIDXUSD",
        "broker_symbol": "USTECm",
        "mapping_id": "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
        "minimum": 3,
        "target": 5
    }
    if config_24["enabled"]:
        modules.append(ForwardModuleWrapper("CAND-024", Cand024Engine(), config_24, base_runtime_dir))
        
    # CAND-035
    config_35 = {
        "enabled": True,
        "logical_symbol": "USATECHIDXUSD",
        "broker_symbol": "USTECm",
        "mapping_id": "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
        "minimum": 3,
        "target": 5
    }
    if config_35["enabled"]:
        modules.append(ForwardModuleWrapper("CAND-035", Cand035Engine(), config_35, base_runtime_dir))
        
    return modules
