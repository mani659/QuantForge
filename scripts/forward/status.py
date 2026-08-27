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
        
        stats = c_status.get("stats", {})
        count = stats.get("captured_count", 0)
        minimum = c_status.get("minimum", 3)
        target = c_status.get("target", 5)
        
        print(f"\nEvents:\n{count} / {minimum} / {target}")
        print(f"\nDetected:\n{stats.get('detected_count', count)}")
        print(f"\nCaptured:\n{count}")
        print(f"\nCompleted:\n{stats.get('completed_count', 0)}")
        print(f"\nMissed:\n{stats.get('missed_count', 0)}")
        
        print(f"\nLogical Symbol:\nUSATECHIDXUSD")
        print(f"Mapping ID:\n{c_status.get('mapping_id', 'N/A')}")

    print("\nCAND-015")
    print("--------")
    print("Status:\nPROTECTED / EXTERNAL")
    print("\n")
    
if __name__ == "__main__":
    print_status()
