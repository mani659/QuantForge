"""Manual local diagnostic for the configured QuantForge MT5 terminal."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from broker.mt5_connection import MT5Connection, MT5ConnectionError


def main() -> None:
    """Connect, print verification diagnostics, and always cleanly shut down."""
    connection = MT5Connection()
    print("================================================")
    print("QUANTFORGE MT5 CONNECTION")
    print("================================================")
    try:
        status = connection.connect()
        print("Terminal\nCONNECTED")
        print(f"Terminal Path\n{status.terminal_path}")
        print(f"Broker\n{status.broker}")
        print(f"Account\n{status.account}")
        print(f"Company\n{status.company}")
        print(f"Balance\n{status.balance}")
        print(f"Equity\n{status.equity}")
        print(f"Trade Allowed\n{'YES' if status.trade_allowed else 'NO'}")
        print("Connection\nSUCCESS")
        print("================================================")
    except MT5ConnectionError as error:
        print(f"Connection\nFAILED\n{error}")
        print("================================================")
        raise SystemExit(1) from error
    finally:
        connection.shutdown()


if __name__ == "__main__":
    main()
