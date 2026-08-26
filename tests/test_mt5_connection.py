import os
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from broker.mt5_connection import ConnectionStatus, MT5Connection, MT5ConnectionError


class FakeMT5:
    def __init__(self, account: int = 10000001) -> None:
        self.account = account
        self.initialize_calls = []
        self.shutdown_calls = 0

    def initialize(self, path: str) -> bool:
        self.initialize_calls.append(path)
        return True

    @staticmethod
    def terminal_info() -> SimpleNamespace:
        return SimpleNamespace(company="MetaTrader5", build=5200)

    def account_info(self) -> SimpleNamespace:
        return SimpleNamespace(
            login=self.account,
            company="MetaTrader5",
            currency="USD",
            balance=10000.0,
            equity=9950.0,
            trade_allowed=True,
        )

    def shutdown(self) -> None:
        self.shutdown_calls += 1


class TestMT5Connection(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.terminal_path = Path(self.temp_directory.name) / "terminal64.exe"
        self.terminal_path.touch()

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_initialization_and_connection_status(self) -> None:
        mt5 = FakeMT5()
        connection = MT5Connection(self.terminal_path, mt5_module=mt5)
        status = connection.connect()
        self.assertTrue(status.connected)
        self.assertEqual(mt5.initialize_calls, [str(self.terminal_path)])
        self.assertEqual(status.account, 10000001)
        self.assertEqual(status.broker, "MetaTrader5")
        self.assertEqual(status.terminal_build, "5200")
        self.assertEqual(
            set(status.to_dict()),
            {
                "connected", "terminal_path", "broker", "account", "company", "currency",
                "balance", "equity", "trade_allowed", "terminal_build", "adapter_version",
            },
        )
        connection.shutdown()
        self.assertEqual(mt5.shutdown_calls, 1)

    def test_account_mismatch_is_rejected_and_shutdown(self) -> None:
        mt5 = FakeMT5(account=123456)
        connection = MT5Connection(
            self.terminal_path, expected_account=10000001, mt5_module=mt5
        )
        with self.assertRaisesRegex(MT5ConnectionError, "account mismatch"):
            connection.connect()
        self.assertEqual(mt5.shutdown_calls, 1)

    def test_missing_configuration_is_rejected(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"QF_MT5_TERMINAL_PATH": "", "QF_MT5_EXPECTED_ACCOUNT": ""},
        ):
            connection = MT5Connection(mt5_module=FakeMT5())
            with self.assertRaisesRegex(MT5ConnectionError, "No MT5 terminal path"):
                connection.connect()

    def test_environment_configuration_is_honored(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "QF_MT5_TERMINAL_PATH": str(self.terminal_path),
                "QF_MT5_EXPECTED_ACCOUNT": "10000001",
            },
        ):
            mt5 = FakeMT5()
            connection = MT5Connection(mt5_module=mt5)
            status = connection.connect()
            self.assertTrue(status.connected)
            self.assertEqual(status.account, 10000001)
            self.assertEqual(status.terminal_path, str(self.terminal_path))

    def test_connection_status_is_immutable(self) -> None:
        status = ConnectionStatus(
            connected=True,
            terminal_path="terminal64.exe",
            broker="MetaTrader5",
            account=10000001,
            company="MetaTrader5",
            currency="USD",
            balance=10000.0,
            equity=9950.0,
            trade_allowed=True,
            terminal_build="5200",
        )
        with self.assertRaises(FrozenInstanceError):
            status.connected = False

    def test_missing_terminal_is_rejected(self) -> None:
        missing_path = self.terminal_path.parent / "missing.exe"
        connection = MT5Connection(missing_path, mt5_module=FakeMT5())
        with self.assertRaisesRegex(MT5ConnectionError, "not found"):
            connection.connect()


if __name__ == "__main__":
    unittest.main()
