from datetime import datetime
import calendar
import pytz
from typing import Optional, Dict, Any
from contracts import CAND_035_CONTRACT

class Cand035Engine:
    def __init__(self):
        self.contract = CAND_035_CONTRACT
        self.ny_tz = pytz.timezone('America/New_York')
        self.current_event_id = None
        self.state = "WATCHING"
        self.open_0930 = None
        self.current_month = None
        
    def _is_last_trading_day(self, dt_ny: datetime) -> bool:
        # Simplified for now. Should account for holidays in a real scenario.
        # But we assume last weekday of the month.
        last_day = calendar.monthrange(dt_ny.year, dt_ny.month)[1]
        last_date = datetime(dt_ny.year, dt_ny.month, last_day)
        if last_date.weekday() >= 5: # Sat or Sun
            last_date = datetime(dt_ny.year, dt_ny.month, last_day - (last_date.weekday() - 4))
        return dt_ny.date() == last_date.date()

    def evaluate(self, current_time_utc: float, quote: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        dt_utc = datetime.fromtimestamp(current_time_utc, tz=pytz.utc)
        dt_ny = dt_utc.astimezone(self.ny_tz)
        
        # Reset monthly tracking
        if self.current_month != dt_ny.month:
            self.current_month = dt_ny.month
            self.open_0930 = None
            self.current_event_id = None
            if self.state in ["COMPLETED", "INVALIDATED"]:
                self.state = "WATCHING"
                
        if quote['symbol'] != "USATECHIDXUSD":
            return None
            
        current_price = (quote['bid'] + quote['ask']) / 2.0
        time_str = dt_ny.strftime("%H:%M:%S")
        
        # Must be last trading day of the month
        if self._is_last_trading_day(dt_ny):
            if "09:30:00" <= time_str < "15:00:00" and self.open_0930 is None:
                self.open_0930 = current_price
                
            if time_str >= "15:00:00" and self.state == "WATCHING":
                open_1500 = current_price
                if self.open_0930 is not None and open_1500 > self.open_0930:
                    self.current_event_id = f"CAND-035-{dt_ny.strftime('%Y%m%d')}-01"
                    self.state = "EVENT_DETECTED"
                    
                    return {
                        "action": "TRIGGER",
                        "event_id": self.current_event_id,
                        "direction": "Long",
                        "theoretical_entry": current_price,
                        "theoretical_exit_time": "16:00:00",
                        "ny_time": time_str
                    }
                else:
                    self.state = "INVALIDATED"
                    
            if time_str >= "16:00:00" and self.state == "IN_POSITION":
                self.state = "COMPLETED"
                return {
                    "action": "EXIT",
                    "event_id": self.current_event_id,
                    "ny_time": time_str
                }
                
        return None
