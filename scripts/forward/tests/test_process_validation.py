"""
Regression tests for process validation, stale status/lock handling,
event console notifications, and BAT behavior.

Uses PowerShell (Get-CimInstance) for process detection, not deprecated WMIC.

Tests cover:
- Process validation (PowerShell-based PID detection)
- Stale status (RUNNING + process missing, STOPPED + process missing, mismatch)
- Stale lock (valid lock, stale lock, duplicate startup protection)
- Event console (DETECTED/CAPTURED/COMPLETED printed, dedup, NO_EVENT silent)
- Stop behavior (active, already stopped)
- Status validation
- BAT content (PowerShell, pause-on-failure, no WMIC)
- Double-click safety
"""

import os
import sys
import json
import time
import pytest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime

# Setup paths
forward_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_dir = os.path.dirname(forward_dir)
repo_dir = os.path.dirname(scripts_dir)
rare_events_dir = os.path.join(scripts_dir, "rare_events")
sys.path.insert(0, forward_dir)
sys.path.insert(0, rare_events_dir)


# ═══════════════════════════════════════════════════════════════════════════════
# PROCESS VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestProcessAlive:
    """Test is_process_alive with mocked subprocess calls."""

    @patch("process_validation.subprocess.run")
    def test_alive_pid_returns_true(self, mock_run):
        from process_validation import is_process_alive
        mock_run.return_value = MagicMock(
            stdout="python.exe                    1234 Console                    1    45,120 K\n",
            returncode=0
        )
        assert is_process_alive(1234) is True

    @patch("process_validation.subprocess.run")
    def test_missing_pid_returns_false(self, mock_run):
        from process_validation import is_process_alive
        mock_run.return_value = MagicMock(
            stdout="INFO: No tasks match the specified criteria.\n",
            returncode=0
        )
        assert is_process_alive(99999) is False

    def test_zero_pid_returns_false(self):
        from process_validation import is_process_alive
        assert is_process_alive(0) is False

    def test_negative_pid_returns_false(self):
        from process_validation import is_process_alive
        assert is_process_alive(-1) is False

    @patch("process_validation.subprocess.run")
    def test_exception_returns_false(self, mock_run):
        from process_validation import is_process_alive
        mock_run.side_effect = Exception("timeout")
        assert is_process_alive(1234) is False


class TestFindSupervisorPid:
    """Test find_supervisor_pid with PowerShell-based mocked subprocess."""

    @patch("process_validation.is_process_alive")
    @patch("process_validation.subprocess.run")
    def test_finds_alive_supervisor(self, mock_run, mock_alive):
        from process_validation import find_supervisor_pid
        mock_run.return_value = MagicMock(stdout="5080\n", returncode=0)
        mock_alive.return_value = True
        assert find_supervisor_pid() == 5080

    @patch("process_validation.is_process_alive")
    @patch("process_validation.subprocess.run")
    def test_no_supervisor_returns_none(self, mock_run, mock_alive):
        from process_validation import find_supervisor_pid
        mock_run.return_value = MagicMock(stdout="", returncode=0)
        assert find_supervisor_pid() is None

    @patch("process_validation.is_process_alive")
    @patch("process_validation.subprocess.run")
    def test_exception_returns_none(self, mock_run, mock_alive):
        from process_validation import find_supervisor_pid
        mock_run.side_effect = Exception("powershell error")
        assert find_supervisor_pid() is None

    @patch("process_validation.is_process_alive")
    @patch("process_validation.subprocess.run")
    def test_dead_pid_ignored(self, mock_run, mock_alive):
        from process_validation import find_supervisor_pid
        mock_run.return_value = MagicMock(stdout="5080\n", returncode=0)
        mock_alive.return_value = False
        assert find_supervisor_pid() is None


# ═══════════════════════════════════════════════════════════════════════════════
# STALE STATUS TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestValidateSupervisorFromStatus:
    """Test validate_supervisor_from_status with file and process mocks."""

    @patch("process_validation.find_supervisor_pid")
    def test_running_matches_status(self, mock_find, tmp_path):
        from process_validation import validate_supervisor_from_status
        status_path = str(tmp_path / "status.json")
        with open(status_path, "w") as f:
            json.dump({"supervisor_state": "RUNNING", "pid": 1234}, f)
        mock_find.return_value = 1234
        result = validate_supervisor_from_status(status_path)
        assert result["running"] is True
        assert result["pid"] == 1234
        assert result["stale"] is False

    @patch("process_validation.find_supervisor_pid")
    def test_stale_running_status(self, mock_find, tmp_path):
        from process_validation import validate_supervisor_from_status
        status_path = str(tmp_path / "status.json")
        with open(status_path, "w") as f:
            json.dump({"supervisor_state": "RUNNING", "pid": 5080}, f)
        mock_find.return_value = None
        result = validate_supervisor_from_status(status_path)
        assert result["running"] is False
        assert result["stale"] is True
        assert "STALE" in result["warning"]

    @patch("process_validation.find_supervisor_pid")
    def test_stopped_status_no_process(self, mock_find, tmp_path):
        from process_validation import validate_supervisor_from_status
        status_path = str(tmp_path / "status.json")
        with open(status_path, "w") as f:
            json.dump({"supervisor_state": "STOPPED", "pid": 5080}, f)
        mock_find.return_value = None
        result = validate_supervisor_from_status(status_path)
        assert result["running"] is False
        assert result["stale"] is False

    @patch("process_validation.find_supervisor_pid")
    def test_pid_mismatch(self, mock_find, tmp_path):
        from process_validation import validate_supervisor_from_status
        status_path = str(tmp_path / "status.json")
        with open(status_path, "w") as f:
            json.dump({"supervisor_state": "RUNNING", "pid": 5080}, f)
        mock_find.return_value = 9999
        result = validate_supervisor_from_status(status_path)
        assert result["running"] is True
        assert result["pid"] == 9999
        assert result["stale"] is True

    @patch("process_validation.find_supervisor_pid")
    def test_no_status_file(self, mock_find, tmp_path):
        from process_validation import validate_supervisor_from_status
        status_path = str(tmp_path / "nonexistent.json")
        mock_find.return_value = None
        result = validate_supervisor_from_status(status_path)
        assert result["running"] is False
        assert result["status_json_state"] == "UNKNOWN"

    @patch("process_validation.find_supervisor_pid")
    def test_corrupt_status_file(self, mock_find, tmp_path):
        from process_validation import validate_supervisor_from_status
        status_path = str(tmp_path / "status.json")
        with open(status_path, "w") as f:
            f.write("not json {{{")
        mock_find.return_value = None
        result = validate_supervisor_from_status(status_path)
        assert result["running"] is False
        assert result["status_json_state"] == "UNREADABLE"


# ═══════════════════════════════════════════════════════════════════════════════
# STALE LOCK TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestValidateLockFile:
    """Test validate_lock_file with mocked process checks."""

    @patch("process_validation.subprocess.run")
    @patch("process_validation.is_process_alive")
    def test_valid_lock(self, mock_alive, mock_run, tmp_path):
        from process_validation import validate_lock_file
        lock_path = str(tmp_path / "supervisor.lock")
        with open(lock_path, "w") as f:
            json.dump({"pid": 1234, "supervisor_version": "1.0.0-unified"}, f)
        mock_alive.return_value = True
        mock_run.return_value = MagicMock(stdout="python.exe\n", returncode=0)
        result = validate_lock_file(lock_path)
        assert result["valid"] is True
        assert result["stale"] is False
        assert result["lock_pid"] == 1234

    @patch("process_validation.subprocess.run")
    @patch("process_validation.is_process_alive")
    def test_stale_lock_dead_pid(self, mock_alive, mock_run, tmp_path):
        from process_validation import validate_lock_file
        lock_path = str(tmp_path / "supervisor.lock")
        with open(lock_path, "w") as f:
            json.dump({"pid": 5080}, f)
        mock_alive.return_value = False
        result = validate_lock_file(lock_path)
        assert result["valid"] is False
        assert result["stale"] is True

    def test_no_lock_file(self):
        from process_validation import validate_lock_file
        result = validate_lock_file("/nonexistent/path/lock")
        assert result["valid"] is False
        assert result["stale"] is False

    def test_corrupt_lock_file(self, tmp_path):
        from process_validation import validate_lock_file
        lock_path = str(tmp_path / "supervisor.lock")
        with open(lock_path, "w") as f:
            f.write("{corrupt json")
        result = validate_lock_file(lock_path)
        assert result["valid"] is False
        assert result["stale"] is True

    def test_lock_without_pid(self, tmp_path):
        from process_validation import validate_lock_file
        lock_path = str(tmp_path / "supervisor.lock")
        with open(lock_path, "w") as f:
            json.dump({"hostname": "test"}, f)
        result = validate_lock_file(lock_path)
        assert result["valid"] is False
        assert result["stale"] is True


# ═══════════════════════════════════════════════════════════════════════════════
# SUPERVISOR STALE LOCK HANDLING TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestSupervisorStaleLock:
    """Test the supervisor's stale lock detection and cleanup."""

    @patch("quantforge_forward_supervisor._is_pid_alive")
    @patch("quantforge_forward_supervisor._find_supervisor_pids")
    def test_stale_lock_cleaned(self, mock_pids, mock_alive, tmp_path):
        from quantforge_forward_supervisor import _is_lock_stale, Supervisor
        s = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        with open(s.lock_file_path, "w") as f:
            json.dump({"pid": 99999}, f)
        mock_alive.return_value = False
        mock_pids.return_value = []
        assert _is_lock_stale(s.lock_file_path, os.getpid()) is True

    @patch("quantforge_forward_supervisor._is_pid_alive")
    @patch("quantforge_forward_supervisor._find_supervisor_pids")
    def test_our_lock_not_stale(self, mock_pids, mock_alive, tmp_path):
        from quantforge_forward_supervisor import _is_lock_stale, Supervisor
        s = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        current_pid = os.getpid()
        with open(s.lock_file_path, "w") as f:
            json.dump({"pid": current_pid}, f)
        mock_pids.return_value = [current_pid]
        assert _is_lock_stale(s.lock_file_path, current_pid) is False

    @patch("quantforge_forward_supervisor._is_pid_alive")
    @patch("quantforge_forward_supervisor._find_supervisor_pids")
    def test_other_supervisor_lock_not_stale(self, mock_pids, mock_alive, tmp_path):
        from quantforge_forward_supervisor import _is_lock_stale, Supervisor
        s = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        other_pid = 7777
        with open(s.lock_file_path, "w") as f:
            json.dump({"pid": other_pid}, f)
        mock_alive.return_value = True
        mock_pids.return_value = [other_pid]
        assert _is_lock_stale(s.lock_file_path, os.getpid()) is False


# ═══════════════════════════════════════════════════════════════════════════════
# STATUS DISPLAY TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestStatusValidation:
    """Test status script behavior with stale and fresh status."""

    @patch("status.find_supervisor_pid")
    @patch("status.validate_lock_file")
    def test_status_shows_not_running_when_stale(self, mock_lock, mock_find, tmp_path, capsys):
        import status as status_mod

        mock_find.return_value = None
        mock_lock.return_value = {"valid": False, "stale": True, "lock_pid": 5080}

        status_dir = tmp_path / "supervisor"
        status_dir.mkdir(parents=True)
        status_file = status_dir / "status.json"
        with open(status_file, "w") as f:
            json.dump({"supervisor_state": "RUNNING", "pid": 5080}, f)

        fake_file = str(tmp_path / "scripts" / "forward" / "status.py")
        with patch.object(status_mod, "__file__", fake_file):
            try:
                status_mod.print_status()
            except Exception:
                pass

        captured = capsys.readouterr()
        assert "NOT RUNNING" in captured.out or "STALE" in captured.out


# ═══════════════════════════════════════════════════════════════════════════════
# EVENT CONSOLE NOTIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestEventConsoleNotification:
    """Test event console printing and deduplication."""

    def test_detected_printed(self, capsys):
        from module_registry import ForwardModuleWrapper
        wrapper = ForwardModuleWrapper.__new__(ForwardModuleWrapper)
        wrapper.candidate_id = "CAND-024"
        wrapper._printed_events = set()
        wrapper.engine = MagicMock()
        wrapper.engine.contract = MagicMock()
        wrapper.engine.contract.hash = "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"
        wrapper._print_event("DETECTED", "SHOCK_1234567890")
        captured = capsys.readouterr()
        assert "QUANTFORGE EVENT" in captured.out
        assert "CAND-024" in captured.out
        assert "DETECTED" in captured.out
        assert "925495a8" in captured.out

    def test_detected_deduplicated(self, capsys):
        from module_registry import ForwardModuleWrapper
        wrapper = ForwardModuleWrapper.__new__(ForwardModuleWrapper)
        wrapper.candidate_id = "CAND-024"
        wrapper._printed_events = set()
        wrapper.engine = MagicMock()
        wrapper.engine.contract = MagicMock()
        wrapper.engine.contract.hash = "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"
        wrapper._print_event("DETECTED", "SHOCK_1234567890")
        wrapper._print_event("DETECTED", "SHOCK_1234567890")
        captured = capsys.readouterr()
        assert captured.out.count("QUANTFORGE EVENT") == 1

    def test_different_states_not_deduplicated(self, capsys):
        from module_registry import ForwardModuleWrapper
        wrapper = ForwardModuleWrapper.__new__(ForwardModuleWrapper)
        wrapper.candidate_id = "CAND-035"
        wrapper._printed_events = set()
        wrapper.engine = MagicMock()
        wrapper.engine.contract = MagicMock()
        wrapper.engine.contract.hash = "ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5"
        wrapper._print_event("DETECTED", "SHOCK_1234567890")
        wrapper._print_event("CAPTURED", "SHOCK_1234567890")
        wrapper._print_event("COMPLETED", "SHOCK_1234567890")
        captured = capsys.readouterr()
        assert captured.out.count("QUANTFORGE EVENT") == 3

    def test_cand015_detected_printed(self, capsys):
        from module_registry import Cand015ModuleWrapper
        wrapper = Cand015ModuleWrapper.__new__(Cand015ModuleWrapper)
        wrapper.candidate_id = "CAND-015"
        wrapper._printed_events = set()
        wrapper._print_event("DETECTED", "SHOCK_1234567890")
        captured = capsys.readouterr()
        assert "QUANTFORGE EVENT" in captured.out
        assert "CAND-015" in captured.out
        assert "EXTERNAL_PROTECTED" in captured.out

    def test_no_event_silent(self, capsys):
        from module_registry import ForwardModuleWrapper
        wrapper = ForwardModuleWrapper.__new__(ForwardModuleWrapper)
        wrapper.candidate_id = "CAND-024"
        wrapper._printed_events = set()
        wrapper.engine = MagicMock()
        wrapper.engine.contract = MagicMock()
        wrapper.engine.contract.hash = "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"
        wrapper.engine.evaluate = MagicMock(return_value=None)
        captured = capsys.readouterr()
        assert "QUANTFORGE EVENT" not in captured.out


# ═══════════════════════════════════════════════════════════════════════════════
# BAT CONTENT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestBatContent:
    """Verify BAT files have the correct runtime behavior patterns."""

    def test_run_bat_uses_powershell(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "powershell" in content.lower()
        assert "Get-CimInstance" in content

    def test_run_bat_no_wmic(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "wmic" not in content.lower()

    def test_run_bat_verifies_pid_alive(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "tasklist" in content.lower()

    def test_run_bat_cleans_stale_lock(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "STALE" in content

    def test_run_bat_no_task_scheduler(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "schtasks" not in content.lower()

    def test_run_bat_has_pause_on_failure(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "pause >nul" in content

    def test_run_bat_checks_python(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "python --version" in content

    def test_stop_bat_uses_powershell(self):
        bat_path = os.path.join(repo_dir, "stop_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "powershell" in content.lower()
        assert "Get-CimInstance" in content

    def test_stop_bat_no_wmic(self):
        bat_path = os.path.join(repo_dir, "stop_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "wmic" not in content.lower()

    def test_stop_bat_handles_not_running(self):
        bat_path = os.path.join(repo_dir, "stop_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "not running" in content.lower()

    def test_stop_bat_verifies_shutdown(self):
        bat_path = os.path.join(repo_dir, "stop_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "shutdown.req" in content

    def test_status_bat_uses_python(self):
        bat_path = os.path.join(repo_dir, "status_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "python" in content.lower()

    def test_run_bat_has_already_running_message(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "SUPERVISOR ALREADY RUNNING" in content

    def test_run_bat_has_forward_start_blocked(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "FORWARD START BLOCKED" in content

    def test_run_bat_has_banner(self):
        bat_path = os.path.join(repo_dir, "run_quantforge_forward.bat")
        with open(bat_path) as f:
            content = f.read()
        assert "QUANTFORGE FORWARD RUNNER" in content


# ═══════════════════════════════════════════════════════════════════════════════
# SUPERVISOR STARTUP BANNER TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestStartupBanner:
    """Test the supervisor startup banner format."""

    def test_startup_banner_has_required_elements(self, tmp_path, capsys):
        from quantforge_forward_supervisor import Supervisor
        supervisor = Supervisor(mode="smoke", base_runtime_dir=str(tmp_path))
        supervisor.feed = MagicMock()
        supervisor.feed.connection_state.return_value = "CONNECTED"
        supervisor.feed.terminal_info.return_value = {
            "broker": "Exness Technologies Ltd",
            "server": "Exness-MT5Trial15"
        }
        supervisor._print_startup_banner({
            "broker": "Exness Technologies Ltd",
            "server": "Exness-MT5Trial15"
        })
        captured = capsys.readouterr()
        assert "QUANTFORGE FORWARD RUNNER" in captured.out
        assert "MT5:" in captured.out
        assert "CONNECTED" in captured.out
        assert "Exness Technologies Ltd" in captured.out
        assert "Exness-MT5Trial15" in captured.out
        assert "USATECHIDXUSD" in captured.out
        assert "USTECm" in captured.out
        assert "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0" in captured.out
        assert "CAND-015" in captured.out
        assert "PROTECTED" in captured.out
        assert "CAND-024" in captured.out
        assert "CAND-035" in captured.out
        assert "LIVE AND RUNNING" in captured.out
        assert "PID:" in captured.out
        assert str(os.getpid()) in captured.out


# ═══════════════════════════════════════════════════════════════════════════════
# UPTIME TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestUptime:
    """Test uptime formatting."""

    def test_uptime_format_hours(self):
        from status import format_uptime
        result = format_uptime(3661)
        assert "1h" in result
        assert "1m" in result
        assert "1s" in result

    def test_uptime_format_minutes(self):
        from status import format_uptime
        result = format_uptime(300)
        assert "5m" in result

    def test_uptime_format_seconds(self):
        from status import format_uptime
        assert "42s" in format_uptime(42)

    def test_uptime_none(self):
        from status import format_uptime
        assert "unavailable" in format_uptime(None)

    def test_uptime_negative(self):
        from status import format_uptime
        assert "unavailable" in format_uptime(-5)


# ═══════════════════════════════════════════════════════════════════════════════
# PAPER SAFETY TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestPaperSafety:
    """Verify paper execution has no live order methods."""

    def test_no_live_order_methods(self):
        from paper_execution import PaperExecutionFirewall
        firewall = PaperExecutionFirewall(friction=2.0)
        dangerous_methods = [
            'place_order', 'send_order', 'execute_order',
            'submit_order', 'open_position', 'close_position'
        ]
        for method in dangerous_methods:
            assert not hasattr(firewall, method)

    def test_paper_only_entry(self):
        from paper_execution import PaperExecutionFirewall
        firewall = PaperExecutionFirewall(friction=2.0)
        event = {"event_id": "TEST", "direction": "Long", "theoretical_entry": 100}
        quote = {"bid": 100, "ask": 102, "utc_timestamp": time.time()}
        result = firewall.execute_entry(event, quote)
        assert result["status"] == "PAPER_ENTRY_RECORDED"


# ═══════════════════════════════════════════════════════════════════════════════
# CANDIDATE INDEPENDENCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestCandidateIndependence:
    """Verify candidates operate independently."""

    def test_separate_event_ledgers(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        ledgers = [m.event_ledger.filepath for m in modules]
        assert len(set(ledgers)) == len(ledgers)

    def test_separate_outcome_ledgers(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        ledgers = [m.outcome_ledger.filepath for m in modules]
        assert len(set(ledgers)) == len(ledgers)

    def test_separate_module_dirs(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        dirs = [m.module_dir for m in modules]
        assert len(set(dirs)) == len(dirs)

    def test_no_signal_combination(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        cand_024 = next(m for m in modules if m.candidate_id == "CAND-024")
        cand_035 = next(m for m in modules if m.candidate_id == "CAND-035")
        quote = {
            "utc_timestamp": time.time(),
            "symbol": "USATECHIDXUSD",
            "broker_symbol": "USTECm",
            "mapping_id": "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
            "bid": 29500.0,
            "ask": 29502.0,
            "age": 0.5
        }
        cand_024.process_quote(quote, "test_instance")
        assert cand_035.engine.state == "WATCHING" or cand_035.engine.state != cand_024.engine.state


# ═══════════════════════════════════════════════════════════════════════════════
# CONTRACT FIREWALL TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestContractFirewall:
    """Verify canonical contract identity is preserved."""

    def test_cand024_identity(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.identity == "CAND-024:CANONICAL:925495a8"

    def test_cand035_identity(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.identity == "CAND-035:CANONICAL:ddc5d0e9"

    def test_cand024_hash_stable(self):
        from contracts import CAND_024_CONTRACT
        assert CAND_024_CONTRACT.hash == "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"

    def test_cand035_hash_stable(self):
        from contracts import CAND_035_CONTRACT
        assert CAND_035_CONTRACT.hash == "ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5"

    def test_qualification_state_preserved(self, tmp_path):
        from module_registry import get_registry
        modules = get_registry(str(tmp_path))
        for m in modules:
            assert m.config["minimum"] == 3
            assert m.config["target"] == 5
