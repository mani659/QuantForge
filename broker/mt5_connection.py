"""Local MT5 terminal connectivity verification for QuantForge v1.1."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


def _terminal_path_from_env() -> Optional[Path]:
    """Returns the MT5 terminal path from QF_MT5_TERMINAL_PATH, or None."""
    raw = os.getenv("QF_MT5_TERMINAL_PATH")
    return Path(raw) if raw else None


def _expected_account_from_env() -> Optional[int]:
    """Returns the expected MT5 account login from QF_MT5_EXPECTED_ACCOUNT, or None."""
    raw = os.getenv("QF_MT5_EXPECTED_ACCOUNT")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


class MT5ConnectionError(RuntimeError):
    """Raised when the configured MT5 terminal cannot be safely verified."""


@dataclass(frozen=True)
class ConnectionStatus:
    """Immutable verified state of the configured MT5 terminal connection."""

    connected: bool
    terminal_path: str
    broker: str
    account: int
    company: str
    currency: str
    balance: float
    equity: float
    trade_allowed: bool
    terminal_build: str
    adapter_version: str = "1.1.0"

    def to_dict(self) -> dict[str, Any]:
        """Returns the serializable ConnectionStatus schema."""
        return {
            "connected": self.connected,
            "terminal_path": self.terminal_path,
            "broker": self.broker,
            "account": self.account,
            "company": self.company,
            "currency": self.currency,
            "balance": self.balance,
            "equity": self.equity,
            "trade_allowed": self.trade_allowed,
            "terminal_build": self.terminal_build,
            "adapter_version": self.adapter_version,
        }


class MT5Connection:
    """Initializes and verifies one locally configured MT5 terminal session.

    The terminal path and expected account login are sourced from the
    environment variables ``QF_MT5_TERMINAL_PATH`` and
    ``QF_MT5_EXPECTED_ACCOUNT``, or passed explicitly to the constructor.
    No account identifier, broker name, or local path is hardcoded.
    """

    def __init__(
        self,
        terminal_path: Path | str | None = None,
        expected_account: int | None = None,
        mt5_module: Optional[Any] = None,
    ) -> None:
        self.terminal_path = (
            Path(terminal_path) if terminal_path is not None else _terminal_path_from_env()
        )
        self.expected_account = (
            expected_account
            if expected_account is not None
            else _expected_account_from_env()
        )
        self._mt5_module = mt5_module
        self._initialized = False

    def connect(self) -> ConnectionStatus:
        """Initializes the terminal and returns a verified immutable status object."""
        if self.terminal_path is None:
            raise MT5ConnectionError(
                "No MT5 terminal path configured. "
                "Set QF_MT5_TERMINAL_PATH or pass terminal_path explicitly."
            )
        if not self.terminal_path.is_file():
            raise MT5ConnectionError(
                f"MT5 terminal executable was not found: {self.terminal_path}"
            )

        mt5 = self._get_mt5_module()
        if not mt5.initialize(path=str(self.terminal_path)):
            raise MT5ConnectionError("MT5 initialization failed.")
        self._initialized = True

        try:
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                raise MT5ConnectionError("MT5 terminal is not connected.")

            account_info = mt5.account_info()
            if account_info is None:
                raise MT5ConnectionError("MT5 account information is unavailable.")
            if (
                self.expected_account is not None
                and account_info.login != self.expected_account
            ):
                raise MT5ConnectionError(
                    f"MT5 account mismatch: expected {self.expected_account}, "
                    f"received {account_info.login}."
                )

            company = str(getattr(account_info, "company", "") or getattr(terminal_info, "company", ""))
            broker = company or str(getattr(account_info, "server", ""))
            return ConnectionStatus(
                connected=True,
                terminal_path=str(self.terminal_path),
                broker=broker,
                account=int(account_info.login),
                company=company,
                currency=str(getattr(account_info, "currency", "")),
                balance=float(getattr(account_info, "balance", 0.0)),
                equity=float(getattr(account_info, "equity", 0.0)),
                trade_allowed=bool(getattr(account_info, "trade_allowed", False)),
                terminal_build=str(getattr(terminal_info, "build", "")),
            )
        except Exception:
            self.shutdown()
            raise

    def shutdown(self) -> None:
        """Cleanly closes a session initialized by this connection manager."""
        if self._initialized:
            self._get_mt5_module().shutdown()
            self._initialized = False

    def _get_mt5_module(self) -> Any:
        """Lazily imports MetaTrader5 so the project remains testable without it."""
        if self._mt5_module is not None:
            return self._mt5_module
        try:
            import MetaTrader5 as mt5
        except ImportError as error:
            raise MT5ConnectionError(
                "MetaTrader5 package is not installed. Install it before connecting."
            ) from error
        self._mt5_module = mt5
        return mt5
