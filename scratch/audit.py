import sys
import os

from datetime import datetime, timezone
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from types import MappingProxyType
from boe.risk.specification import PositionSpecification

def main():
    adapter = PaperTradingAdapter(PaperTradingAdapterConfig(broker_name="paper_broker", metadata=MappingProxyType({})))
    
    raw_ticks = [
        {"id": "t1", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.1000},
        {"id": "t2", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc), "close": 1.1010},
        {"id": "t3", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 2, tzinfo=timezone.utc), "close": 1.1020},
        {"id": "t4", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 3, tzinfo=timezone.utc), "close": 1.1030},
        {"id": "t5", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 4, tzinfo=timezone.utc), "close": 1.1040},
    ]

    exposures = [0.02, 0.04, 0.01, -0.02, 0.0]

    for i, (tick, exp) in enumerate(zip(raw_ticks, exposures)):
        print(f"--- TICK {i+1} ---")
        price = tick["close"]
        print(f"Price: {price}")
        print(f"Exposure requested: {exp}")
        
        # update market price
        adapter.account.update_market_price(price)
        print(f"Starting balance: {adapter.account.balance}")
        print(f"Unrealized PnL before exec: {adapter.account.unrealised_pnl}")
        print(f"Equity before exec: {adapter.account.equity}")
        
        cand = adapter.account.open_positions.get("c_1")
        if cand:
            print(f"Existing position vol: {cand['volume']}")
            print(f"Existing entry price: {cand['entry_price']}")
        else:
            print(f"Existing position vol: 0.0")
            print(f"Existing entry price: 0.0")
            
        target_vol = (adapter.account.equity * abs(exp)) / price
        print(f"Target volume: {target_vol}")
        
        res = adapter.account.execute_trade("c_1", exp)
        
        cand = adapter.account.open_positions.get("c_1")
        print(f"Executed action: {res['action']}, vol: {res['volume']}")
        
        print(f"Cumulative realized PnL: {adapter.account.realised_pnl}")
        
        if cand:
            print(f"Remaining pos vol: {cand['volume']}")
            print(f"New average entry: {cand['entry_price']}")
        else:
            print(f"Remaining pos vol: 0.0")
            print(f"New average entry: 0.0")
            
        print(f"Ending balance: {adapter.account.balance}")
        print(f"Ending unrealized PnL: {adapter.account.unrealised_pnl}")
        print(f"Ending equity: {adapter.account.equity}")
        
        print("\n")
        
    print(f"Final Realised PnL: {adapter.account.realised_pnl}")
    print("Closed positions:")
    for cp in adapter.account.closed_positions:
        print(cp)

if __name__ == '__main__':
    main()
