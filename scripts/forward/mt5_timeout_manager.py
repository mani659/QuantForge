"""MT5 Timeout Manager — manages worker lifecycle and enforces hard timeouts.

This module provides the parent-side interface for:
- Spawning/replacing MT5 worker processes
- Dispatching requests with hard timeout enforcement
- Rejecting stale responses via request ID / generation tracking
- Worker health monitoring
- Clean shutdown

HARD TIMEOUT GUARANTEE:
  Every request is dispatched with a deadline. If the worker does not
  respond within the deadline, the worker process is terminated and
  replaced. The parent never waits indefinitely.

STALE RESPONSE PROTECTION:
  Each worker has a generation number. Requests dispatched to generation N
  are rejected if a response arrives from generation N+1 or later.

F-01 FIREWALL:
  This module does NOT access F-01 data, modify archives, or inspect
  economic performance.
"""
import multiprocessing
import time
import os
import sys
from mt5_worker import mt5_worker_main


# Default configuration
DEFAULT_REQUEST_TIMEOUT = 5.0      # seconds per MT5 operation
DEFAULT_WORKER_STARTUP_TIMEOUT = 10.0  # seconds for worker initialization
DEFAULT_MAX_CONSECUTIVE_FAILURES = 5   # before declaring DEGRADED
DEFAULT_CLEANUP_TIMEOUT = 3.0          # seconds for clean shutdown


class MT5TimeoutManager:
    """Manages MT5 worker processes with hard timeout guarantees.

    Usage:
        manager = MT5TimeoutManager()
        manager.start()
        result = manager.execute("latest_quote", symbol="USTECm", timeout=5.0)
        manager.shutdown()
    """

    def __init__(
        self,
        request_timeout=DEFAULT_REQUEST_TIMEOUT,
        startup_timeout=DEFAULT_WORKER_STARTUP_TIMEOUT,
        max_consecutive_failures=DEFAULT_MAX_CONSECUTIVE_FAILURES,
        cleanup_timeout=DEFAULT_CLEANUP_TIMEOUT,
    ):
        self.request_timeout = request_timeout
        self.startup_timeout = startup_timeout
        self.max_consecutive_failures = max_consecutive_failures
        self.cleanup_timeout = cleanup_timeout

        # Worker state
        self._worker = None
        self._request_queue = None
        self._result_queue = None
        self._control_queue = None
        self._generation = 0
        self._worker_id = None

        # Health tracking
        self._consecutive_failures = 0
        self._total_timeouts = 0
        self._total_requests = 0
        self._total_successes = 0
        self._last_request_time = 0.0
        self._last_success_time = 0.0
        self._last_failure_time = 0.0

    @property
    def is_started(self):
        """Whether the manager has a live worker."""
        return (
            self._worker is not None
            and self._worker.is_alive()
        )

    @property
    def health_state(self):
        """Current health state string."""
        if not self.is_started:
            return "UNINITIALIZED"
        if self._consecutive_failures >= self.max_consecutive_failures:
            return "DEGRADED"
        return "HEALTHY"

    @property
    def stats(self):
        """Return current statistics."""
        return {
            "generation": self._generation,
            "consecutive_failures": self._consecutive_failures,
            "total_timeouts": self._total_timeouts,
            "total_requests": self._total_requests,
            "total_successes": self._total_successes,
            "health_state": self.health_state,
            "worker_alive": self.is_started,
        }

    def start(self, terminal_path=None):
        """Start a new worker process.

        Args:
            terminal_path: Optional MT5 terminal path for initialization.

        Returns:
            True if worker started and initialized successfully.
        """
        if self._worker is not None:
            self._terminate_worker()

        self._generation += 1
        self._worker_id = f"mt5_worker_gen{self._generation}"
        self._request_queue = multiprocessing.Queue()
        self._result_queue = multiprocessing.Queue()
        self._control_queue = multiprocessing.Queue()

        self._worker = multiprocessing.Process(
            target=mt5_worker_main,
            args=(
                self._request_queue,
                self._result_queue,
                self._control_queue,
                self._worker_id,
            ),
            daemon=True,
        )
        self._worker.start()

        # Wait for worker to initialize
        init_result = self._wait_for_response(
            request_id="__init__",
            operation="initialize",
            params={"terminal_path": terminal_path},
            timeout=self.startup_timeout,
        )

        if init_result and init_result.get("success"):
            self._consecutive_failures = 0
            return True
        else:
            self._terminate_worker()
            return False

    def execute(self, operation, timeout=None, **params):
        """Execute an MT5 operation with hard timeout.

        Args:
            operation: MT5 operation name (e.g., "latest_quote").
            timeout: Override default request timeout.
            **params: Operation parameters.

        Returns:
            dict with keys: success, result, error, timeout, elapsed
        """
        if not self.is_started:
            return {
                "success": False,
                "result": None,
                "error": "Worker not started",
                "timeout": False,
                "elapsed": 0.0,
            }

        timeout = timeout or self.request_timeout
        request_id = f"req_{self._generation}_{self._total_requests}"
        self._total_requests += 1
        self._last_request_time = time.time()

        # Dispatch request
        request = {
            "request_id": request_id,
            "operation": operation,
            **params,
        }
        self._request_queue.put(request)

        # Wait for response with timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                msg = self._result_queue.get(timeout=0.05)
                elapsed = time.time() - start_time

                # Check generation — reject stale responses
                msg_id = msg.get("request_id", "")
                if msg_id.startswith(f"req_{self._generation}_") or msg_id == "__init__":
                    # Valid response from current generation
                    if msg.get("success"):
                        self._consecutive_failures = 0
                        self._total_successes += 1
                        self._last_success_time = time.time()
                    else:
                        self._consecutive_failures += 1
                        self._last_failure_time = time.time()

                    return {
                        "success": msg.get("success", False),
                        "result": msg.get("result"),
                        "error": msg.get("error"),
                        "timeout": False,
                        "elapsed": elapsed,
                    }
                # else: stale response from old generation, discard
            except Exception:
                continue

        # Timeout — terminate worker
        self._total_timeouts += 1
        self._consecutive_failures += 1
        self._last_failure_time = time.time()
        self._terminate_worker()

        # Attempt restart if under failure limit
        if self._consecutive_failures < self.max_consecutive_failures:
            self._restart_worker()

        return {
            "success": False,
            "result": None,
            "error": f"Timeout after {timeout}s",
            "timeout": True,
            "elapsed": timeout,
        }

    def _wait_for_response(self, request_id, operation, params, timeout):
        """Send a request and wait for its specific response."""
        request = {
            "request_id": request_id,
            "operation": operation,
            **params,
        }
        self._request_queue.put(request)

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                msg = self._result_queue.get(timeout=0.05)
                if msg.get("request_id") == request_id:
                    return msg
            except Exception:
                continue
        return None

    def _terminate_worker(self):
        """Terminate the worker process cleanly."""
        if self._worker is None:
            return

        if self._worker.is_alive():
            # Try clean shutdown first
            try:
                self._control_queue.put("SHUTDOWN")
                self._worker.join(timeout=self.cleanup_timeout)
            except Exception:
                pass

            # Force terminate if still alive
            if self._worker.is_alive():
                self._worker.terminate()
                self._worker.join(timeout=2.0)

            # Last resort: kill
            if self._worker.is_alive():
                self._worker.kill()
                self._worker.join(timeout=1.0)

        self._worker = None

    def _restart_worker(self):
        """Restart the worker after a failure."""
        self._terminate_worker()
        self._generation += 1
        self._worker_id = f"mt5_worker_gen{self._generation}"
        self._request_queue = multiprocessing.Queue()
        self._result_queue = multiprocessing.Queue()
        self._control_queue = multiprocessing.Queue()

        self._worker = multiprocessing.Process(
            target=mt5_worker_main,
            args=(
                self._request_queue,
                self._result_queue,
                self._control_queue,
                self._worker_id,
            ),
            daemon=True,
        )
        self._worker.start()

        # Wait for initialization
        init_result = self._wait_for_response(
            request_id="__init__",
            operation="initialize",
            params={},
            timeout=self.startup_timeout,
        )

        if not init_result or not init_result.get("success"):
            self._terminate_worker()

    def shutdown(self):
        """Shutdown the manager and worker cleanly."""
        if self._worker is not None and self._worker.is_alive():
            try:
                self._control_queue.put("SHUTDOWN")
                self._worker.join(timeout=self.cleanup_timeout)
            except Exception:
                pass

            if self._worker.is_alive():
                self._worker.terminate()
                self._worker.join(timeout=2.0)

            if self._worker.is_alive():
                self._worker.kill()
                self._worker.join(timeout=1.0)

        self._worker = None
