"""MT5 Worker Process — owns MT5 connection, executes bounded requests.

This module runs in a separate process and communicates with the parent
via multiprocessing Queues. It owns the MT5 connection lifecycle and
executes one request at a time.

PROTOCOL:
  Parent sends request dicts via request_queue.
  Worker responds via result_queue.
  Parent can terminate worker on timeout.

REQUEST ENVELOPE:
  {
    "request_id": str,       # unique per request
    "operation": str,        # one of: "initialize", "connection_state",
                             #         "terminal_info", "latest_quote",
                             #         "latest_completed_bar", "shutdown"
    "symbol": str,           # optional, for quote/bar operations
    "timeframe": str,        # optional, for bar operations ("M1", "M5", etc.)
    "terminal_path": str,    # optional, for initialize operation
  }

RESPONSE ENVELOPE:
  {
    "request_id": str,
    "success": bool,
    "result": dict,          # operation-specific result
    "error": str | None,     # error message if not successful
    "timestamp": float,      # time.time() of response
  }

F-01 FIREWALL:
  This worker does NOT:
  - access data/f01
  - modify study archive
  - modify raw archive
  - ingest bars
  - synthesize M1 bars
  - access protected forward economics
"""
import multiprocessing
import time
import os
import sys
import traceback


# MT5 timeframe constants (must match MetaTrader5 package values)
TIMEFRAME_MAP = {
    "M1": None,   # resolved at runtime from mt5 module
    "M5": None,
    "M15": None,
    "H1": None,
}


def _resolve_timeframes(mt5):
    """Resolve MT5 timeframe constants from the module."""
    return {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "H1": mt5.TIMEFRAME_H1,
    }


def _handle_operation(mt5, operation, params):
    """Execute a single MT5 operation. Returns result dict."""
    if operation == "initialize":
        terminal_path = params.get("terminal_path")
        if terminal_path and os.path.exists(terminal_path):
            ok = mt5.initialize(path=terminal_path)
        else:
            ok = mt5.initialize()
        return {"initialized": ok}

    elif operation == "connection_state":
        terminal_info = mt5.terminal_info()
        if terminal_info is None:
            return {"state": "DISCONNECTED"}
        return {"state": "CONNECTED"}

    elif operation == "terminal_info":
        info = mt5.terminal_info()
        acc = mt5.account_info()
        return {
            "broker": info.company if info else "UNKNOWN",
            "server": acc.server if acc else "UNKNOWN",
            "connected": info.connected if info else False,
        }

    elif operation == "latest_quote":
        symbol = params["symbol"]
        mt5.symbol_select(symbol, True)
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return {"status": "DATA_INDETERMINATE"}
        source_ts = tick.time
        receipt_ts = time.time()
        age = receipt_ts - source_ts
        if age > 60:
            return {"status": "DATA_STALE", "age": age}
        return {
            "status": "DATA_FRESH",
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "source_timestamp": source_ts,
            "receipt_timestamp": receipt_ts,
            "age": age,
        }

    elif operation == "latest_completed_bar":
        symbol = params["symbol"]
        timeframe = params["timeframe"]
        tf_map = _resolve_timeframes(mt5)
        mt5_tf = tf_map.get(timeframe)
        if not mt5_tf:
            return {"status": "DATA_INDETERMINATE"}
        mt5.symbol_select(symbol, True)
        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 1, 1)
        if rates is None or len(rates) == 0:
            return {"status": "DATA_INDETERMINATE"}
        bar = rates[0]
        try:
            volume = int(bar["tick_volume"])
        except Exception:
            volume = 0
        return {
            "status": "DATA_FRESH",
            "symbol": symbol,
            "time": bar["time"],
            "open": bar["open"],
            "high": bar["high"],
            "low": bar["low"],
            "close": bar["close"],
            "volume": volume,
        }

    elif operation == "shutdown":
        mt5.shutdown()
        return {"shutdown": True}

    else:
        return {"error": f"Unknown operation: {operation}"}


def mt5_worker_main(request_queue, result_queue, control_queue, worker_id):
    """Main entry point for the MT5 worker process.

    This function runs in a child process and never returns under normal
    operation (it loops until shutdown or termination).
    """
    import MetaTrader5 as mt5

    initialized = False
    try:
        while True:
            # Check for control messages
            if not control_queue.empty():
                ctrl = control_queue.get_nowait()
                if ctrl == "SHUTDOWN":
                    if initialized:
                        try:
                            mt5.shutdown()
                        except Exception:
                            pass
                    result_queue.put({
                        "request_id": "__control__",
                        "success": True,
                        "result": {"shutdown": True},
                        "error": None,
                        "timestamp": time.time(),
                    })
                    return

            # Process requests
            if not request_queue.empty():
                req = request_queue.get_nowait()
                request_id = req.get("request_id", "unknown")
                operation = req.get("operation", "unknown")
                params = {k: v for k, v in req.items() if k not in ("request_id", "operation")}

                try:
                    # Handle initialize specially to track state
                    if operation == "initialize":
                        result = _handle_operation(mt5, operation, params)
                        initialized = result.get("initialized", False)
                    elif operation == "shutdown":
                        result = _handle_operation(mt5, operation, params)
                        initialized = False
                    else:
                        result = _handle_operation(mt5, operation, params)

                    # Check for operation-level errors
                    error = result.get("error") if isinstance(result, dict) else None

                    result_queue.put({
                        "request_id": request_id,
                        "success": error is None,
                        "result": result,
                        "error": error,
                        "timestamp": time.time(),
                    })
                except Exception as e:
                    result_queue.put({
                        "request_id": request_id,
                        "success": False,
                        "result": None,
                        "error": f"{type(e).__name__}: {e}",
                        "timestamp": time.time(),
                    })
            else:
                # No work — sleep briefly to avoid busy-wait
                time.sleep(0.01)

    except Exception as e:
        # Worker-level exception (should not happen)
        result_queue.put({
            "request_id": "__worker_error__",
            "success": False,
            "result": None,
            "error": f"Worker fatal: {type(e).__name__}: {e}",
            "timestamp": time.time(),
        })
    finally:
        try:
            if initialized:
                mt5.shutdown()
        except Exception:
            pass
