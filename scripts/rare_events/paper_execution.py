from typing import Dict, Any

class PaperExecutionFirewall:
    def __init__(self, friction: float):
        self.friction = friction
        self.positions = {}
        
    def execute_entry(self, event: Dict[str, Any], quote: Dict[str, Any]) -> Dict[str, Any]:
        """
        No live order execution. Mock paper entry.
        """
        event_id = event['event_id']
        direction = event['direction']
        
        # Modeled entry (assume spread + half friction on entry)
        if direction == "Long":
            entry_price = quote['ask'] + (self.friction / 2.0)
        else:
            entry_price = quote['bid'] - (self.friction / 2.0)
            
        self.positions[event_id] = {
            "entry_price": entry_price,
            "direction": direction,
            "entry_time": quote['utc_timestamp']
        }
        
        return {
            "status": "PAPER_ENTRY_RECORDED",
            "paper_entry_price": entry_price,
            "theoretical_entry": event['theoretical_entry']
        }
        
    def execute_exit(self, event: Dict[str, Any], quote: Dict[str, Any]) -> Dict[str, Any]:
        """
        No live order execution. Mock paper exit.
        """
        event_id = event['event_id']
        if event_id not in self.positions:
            return {"status": "ERROR", "reason": "No position found"}
            
        pos = self.positions.pop(event_id)
        direction = pos['direction']
        entry_price = pos['entry_price']
        
        # Modeled exit
        if direction == "Long":
            exit_price = quote['bid'] - (self.friction / 2.0)
            gross = exit_price - entry_price
        else:
            exit_price = quote['ask'] + (self.friction / 2.0)
            gross = entry_price - exit_price
            
        net_result = gross  # Friction already modeled in prices
        
        return {
            "status": "PAPER_EXIT_RECORDED",
            "paper_entry_price": entry_price,
            "paper_exit_price": exit_price,
            "gross_result": gross,
            "net_result": net_result,
            "modeled_friction": self.friction
        }
