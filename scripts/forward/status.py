import os
import sys
import json
from datetime import datetime

def format_time(ts):
    if not ts:
        return "N/A"
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")

def print_status():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    runtime_dir = os.path.join(base_dir, "runtime", "forward")
    supervisor_status_path = os.path.join(runtime_dir, "supervisor", "status.json")
    
    print("\nQUANTFORGE FORWARD STATUS")
    print("=========================")
    
    sup_status = {}
    if os.path.exists(supervisor_status_path):
        try:
            with open(supervisor_status_path, "r") as f:
                sup_status = json.load(f)
        except:
            pass
            
    print(f"\nSupervisor:")
    print(f"{sup_status.get('supervisor_state', 'STOPPED / UNKNOWN')}")
    if sup_status.get('supervisor_state') == 'RUNNING':
        print(f"PID: {sup_status.get('pid', 'N/A')}")
        
    print(f"\nMT5:")
    print(f"{sup_status.get('mt5_connection', 'N/A')}")
    
    print(f"\nBroker:")
    print(f"{sup_status.get('broker', 'N/A')}")
    
    print(f"\nServer:")
    print(f"{sup_status.get('server', 'N/A')}")
    
    print(f"\nLogical Market:")
    print(f"USATECHIDXUSD")
    
    print(f"\nBroker Symbol:")
    print(f"USTECm")
    
    print(f"\nMapping:")
    print(f"MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0")
    
    uptime = sup_status.get("uptime_seconds", 0)
    print(f"\nUptime:")
    print(f"{uptime:.1f} seconds")
    
    for cand in ["CAND-024", "CAND-035"]:
        cand_dir = cand.lower().replace("-", "_")
        cand_status_path = os.path.join(runtime_dir, cand_dir, "status.json")
        print(f"\n{cand}")
        print("-" * len(cand))
        
        c_status = {}
        if os.path.exists(cand_status_path):
            try:
                with open(cand_status_path, "r") as f:
                    c_status = json.load(f)
            except:
                pass
                
        if not c_status:
            print("Status:\nUNKNOWN / FILE MISSING")
            continue
            
        print("Status:")
        print("ACTIVE" if sup_status.get("supervisor_state") == "RUNNING" else "OFFLINE")
        
        contract_hash = c_status.get("contract_hash", "N/A")
        if len(contract_hash) > 8:
            contract_hash = contract_hash[:8]
        print(f"\nCanonical Hash:\n{contract_hash}")
        
        stats = c_status.get("stats", {})
        count = stats.get("captured_count", 0)
        minimum = c_status.get("minimum", 3)
        target = c_status.get("target", 5)
        
        print(f"\nEvents:\n{count} / {minimum} / {target}")
        print(f"\nState:\n{c_status.get('current_state', 'N/A')}")

    cand015_status_path = os.path.join(runtime_dir, "cand_015", "status.json")
    print(f"\nCAND-015")
    print("--------")

    c015_status = {}
    if os.path.exists(cand015_status_path):
        try:
            with open(cand015_status_path, "r") as f:
                c015_status = json.load(f)
        except:
            pass

    if not c015_status:
        print("Status:\nEXTERNAL / PROTECTED")
        print("Note:\nAdapter-based integration. Different contract architecture.")
    else:
        print("Status:")
        print("ACTIVE (ADAPTER)" if sup_status.get("supervisor_state") == "RUNNING" else "OFFLINE")
        print(f"\nArchitectural Note:\n{c015_status.get('architectural_note', 'N/A')}")
        stats = c015_status.get("stats", {})
        count = stats.get("captured_count", 0)
        print(f"\nEvents:\n{count} / 3 / 5")
    print("")
    
if __name__ == "__main__":
    print_status()
