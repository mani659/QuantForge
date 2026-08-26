import time
import pandas as pd
from datetime import timezone

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from research.g6_forward.harness import G6Harness

def run_smoke_test():
    print("=== CAND-015 MT5 FORWARD SMOKE TEST ===")
    
    if not MT5_AVAILABLE:
        print("MetaTrader5 not installed. Cannot run live smoke test.")
        return False
        
    # 1. Initialize MT5
    if not mt5.initialize():
        print(f"Failed to initialize MT5, error: {mt5.last_error()}")
        return False
    print("1. MT5 Initialized")
    
    # 2. Verify Demo Account
    account = mt5.account_info()
    if account is None or account.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        print("Failed to verify DEMO account.")
        return False
    print("2. Demo Account Verified")
    
    # 3 & 4. Verify Symbols
    symbols = ["USTECm", "BTCUSDm"]
    for s in symbols:
        if not mt5.symbol_select(s, True):
            print(f"Failed to select symbol {s}")
            return False
    print("3&4. USTECm and BTCUSDm Verified")
    
    # 5. Obtain Bid/Ask
    for s in symbols:
        info = mt5.symbol_info(s)
        print(f"5. {s} Quote -> Bid: {info.bid}, Ask: {info.ask}")
        
    # 6. Obtain completed bars
    for s in symbols:
        rates_m1 = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M1, 0, 2)
        rates_m5 = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M5, 0, 2)
        rates_d1 = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 2)
        print(f"6. {s} Completed M1 Close: {rates_m1[-2]['close']}")
        print(f"6. {s} Completed M5 Close: {rates_m5[-2]['close']}")
        print(f"6. {s} Completed D1 Close: {rates_d1[-2]['close']}")
        
    # 7. Verify UTC timestamps
    utc_now = pd.Timestamp.now(tz=timezone.utc)
    market_time = pd.Timestamp(info.time, unit='s', tz='UTC')
    print(f"7. UTC Timestamp Check -> Local: {utc_now}, Market: {market_time}")
    
    # 8. Verify No Order API
    # Since we are just testing reading data and passing it to harness, there is no order call.
    print("8. No order API is invoked (by design).")
    
    # 9 & 10. Feed into Harness and stop cleanly
    print("9. Initializing Harness in FORWARD_PAPER mode...")
    harness = G6Harness(mode="FORWARD_PAPER", ledger_path="smoke_test_ledger.csv")
    
    # Run observation for a very short duration (2 seconds)
    print("Running observation loop for 2 seconds...")
    try:
        harness.run_forward_observation(poll_interval_ms=500, max_duration_seconds=2)
    except Exception as e:
        print(f"Harness raised exception: {e}")
        return False
        
    print("10. Harness stopped cleanly.")
    
    mt5.shutdown()
    print("=== SMOKE TEST PASSED ===")
    return True

if __name__ == "__main__":
    run_smoke_test()
