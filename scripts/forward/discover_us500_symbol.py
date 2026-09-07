"""US500 Symbol Discovery — determines the correct MT5 executable symbol.

This script queries the live MT5 environment via the existing timeout-protected
feed to find the broker symbol for US500.

F-01 FIREWALL: This script does NOT access F-01 data, modify archives,
or inspect economic performance.
"""

import os
import sys
import time

# Add the forward scripts directory to the path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from market_data import MT5MarketFeed, MT5TimeoutMarketFeed
from mt5_timeout_manager import MT5TimeoutManager


def discover_us500_symbol():
    """Try common US500 broker symbols and report which ones are available."""
    # Common S&P 500 symbol variants across brokers
    candidates = [
        "US500",
        "SPX500",
        "SPX500m",
        "US500m",
        "SP500",
        "SP500m",
        "USTECm",  # already known
    ]

    # Try timeout-protected feed first
    manager = MT5TimeoutManager(
        request_timeout=5.0,
        startup_timeout=10.0,
    )
    feed = MT5TimeoutMarketFeed(manager)

    print("Initializing MT5 via timeout-protected feed...")
    if not manager.start():
        print("BLOCKED: MT5 timeout worker failed to start")
        return None

    if not feed.initialize():
        print("BLOCKED: MT5 initialization failed")
        manager.shutdown()
        return None

    print("MT5 CONNECTED")
    info = feed.terminal_info()
    print(f"Broker: {info.get('broker', 'UNKNOWN')}")
    print(f"Server: {info.get('server', 'UNKNOWN')}")
    print()

    # First verify USTECm is available
    ustecm = feed.latest_quote("USTECm")
    print(f"USTECm: {ustecm.get('status', 'UNKNOWN')}")
    if ustecm.get("status") == "DATA_FRESH":
        print(f"  Bid: {ustecm.get('bid')}, Ask: {ustecm.get('ask')}")
    print()

    # Try each candidate symbol
    print("Scanning for US500 equivalents...")
    print("-" * 50)
    found = None
    for sym in candidates:
        if sym == "USTECm":
            continue  # already known
        try:
            result = feed.latest_completed_bar(sym, "M1")
            status = result.get("status", "UNKNOWN")
            if status == "DATA_FRESH":
                print(f"  {sym}: DATA_FRESH")
                print(f"    Time: {result.get('time')}")
                print(f"    OHLC: {result.get('open')} / {result.get('high')} / {result.get('low')} / {result.get('close')}")
                if found is None:
                    found = sym
            else:
                print(f"  {sym}: {status}")
        except Exception as e:
            print(f"  {sym}: ERROR - {e}")

    print("-" * 50)

    if found:
        print(f"\nUS500 EXECUTABLE SYMBOL: {found}")
        print(f"Logical market: US500")
        print(f"Executable symbol: {found}")
    else:
        print("\nUS500 DATA EXTENSION BLOCKED — EXECUTABLE SYMBOL NOT DETERMINISTICALLY ESTABLISHED")

    feed.shutdown()
    manager.shutdown()
    return found


if __name__ == "__main__":
    discover_us500_symbol()
