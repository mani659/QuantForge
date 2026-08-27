from datetime import datetime
import pytz
from typing import Optional, Dict, Any
from contracts import CAND_024_CONTRACT

class Cand024Engine:
    def __init__(self):
        self.contract = CAND_024_CONTRACT
        self.ny_tz = pytz.timezone('America/New_York')
        self.current_event_id = None
        self.state = "WATCHING"  # WATCHING, EVENT_DETECTED, IN_POSITION, COMPLETED, INVALIDATED
        self.week_high = float('-inf')
        self.morning_high = float('-inf')
        self.open_0800 = None
        self.current_week = None
        
    def evaluate(self, current_time_utc: float, quote: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        dt_utc = datetime.fromtimestamp(current_time_utc, tz=pytz.utc)
        dt_ny = dt_utc.astimezone(self.ny_tz)
        
        # Reset weekly tracking on Monday
        week_num = dt_ny.isocalendar()[1]
        if self.current_week != week_num:
            self.current_week = week_num
            self.week_high = float('-inf')
            self.morning_high = float('-inf')
            self.open_0800 = None
            self.current_event_id = None
            if self.state in ["COMPLETED", "INVALIDATED"]:
                self.state = "WATCHING"
        
        # We only evaluate USATECHIDXUSD
        if quote['symbol'] != "USATECHIDXUSD":
            return None
            
        current_price = (quote['bid'] + quote['ask']) / 2.0
        
        # Track weekly high prior to Friday
        if dt_ny.weekday() < 4:
            if current_price > self.week_high:
                self.week_high = current_price
                
        # On Friday, track morning action
        if dt_ny.weekday() == 4:
            time_str = dt_ny.strftime("%H:%M:%S")
            
            # Record 08:00 open
            if "08:00:00" <= time_str < "12:00:00":
                if self.open_0800 is None and time_str >= "08:00:00":
                    self.open_0800 = current_price
                
                if current_price > self.morning_high:
                    self.morning_high = current_price
            
            # Trigger event at exactly 12:00
            if time_str >= "12:00:00" and self.state == "WATCHING":
                open_1200 = current_price
                
                # Check preconditions
                if self.morning_high > self.week_high and self.open_0800 is not None and open_1200 < self.open_0800:
                    self.current_event_id = f"CAND-024-{dt_ny.strftime('%Y%m%d')}-01"
                    self.state = "EVENT_DETECTED"
                    
                    return {
                        "action": "TRIGGER",
                        "event_id": self.current_event_id,
                        "direction": "Short",
                        "theoretical_entry": current_price,
                        "theoretical_exit_time": "15:45:00",
                        "ny_time": time_str
                    }
                else:
                    self.state = "INVALIDATED"
                    
            # Exit event at exactly 15:45
            if time_str >= "15:45:00" and self.state == "IN_POSITION":
                self.state = "COMPLETED"
                return {
                    "action": "EXIT",
                    "event_id": self.current_event_id,
                    "ny_time": time_str
                }
                
        return None
